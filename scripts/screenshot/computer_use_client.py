"""
Computer Use API Client

This module provides the core client for interacting with Claude's Computer Use API.
It manages the agent loop: sending tasks to Claude, receiving tool use requests,
executing actions, and returning results.
"""

import anthropic
import base64
import io
import time
from typing import Dict, List, Any, Optional
from PIL import Image


class ComputerUseClient:
    """
    Manages Computer Use API interactions and agent loop

    The agent loop works as follows:
    1. Send task prompt to Claude with Computer Use tool available
    2. Claude analyzes and requests tool actions (screenshot, click, type, etc.)
    3. Execute requested actions via ComputerUseTool
    4. Send results back to Claude
    5. Repeat until task complete or max iterations reached
    """

    def __init__(
        self,
        api_key: str,
        model: str = "claude-sonnet-4-5",
        display_width: int = 1280,
        display_height: int = 800,
    ):
        """
        Initialize Computer Use client

        Args:
            api_key: Anthropic API key
            model: Claude model to use (sonnet-4-5 recommended for cost/quality)
            display_width: Display width in pixels (≤1280 recommended)
            display_height: Display height in pixels (≤800 recommended)
        """
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.display_width = display_width
        self.display_height = display_height
        self.beta_header = "computer-use-2025-01-24"

        # Tool executor will be set by the capturer
        self.tool_executor = None

    def set_tool_executor(self, executor):
        """Set the tool executor instance"""
        self.tool_executor = executor

    async def execute_task(
        self,
        task_prompt: str,
        system_prompt: Optional[str] = None,
        max_iterations: int = 50,
        verbose: bool = True,
    ) -> Dict[str, Any]:
        """
        Execute a task using the agent loop

        Args:
            task_prompt: The task for Claude to perform
            system_prompt: Optional system prompt with instructions/credentials
            max_iterations: Maximum agent loop iterations
            verbose: Print progress messages

        Returns:
            Dict containing:
                - messages: Full conversation history
                - screenshots: List of base64 screenshots captured
                - iterations: Number of iterations used
                - success: Whether task completed successfully

        Raises:
            MaxIterationsError: If max iterations exceeded
            ToolExecutorError: If tool executor not set or fails
        """
        if not self.tool_executor:
            raise RuntimeError("Tool executor not set. Call set_tool_executor() first.")

        # Build initial messages
        messages = [
            {"role": "user", "content": task_prompt}
        ]

        # Default system prompt if none provided
        if system_prompt is None:
            system_prompt = self._build_default_system_prompt()

        screenshots = []
        iterations = 0

        while iterations < max_iterations:
            iterations += 1

            if verbose:
                print(f"   🔄 Agent loop iteration {iterations}/{max_iterations}")

            try:
                # Call Claude API with Computer Use tool
                response = self.client.beta.messages.create(
                    model=self.model,
                    max_tokens=4096,
                    messages=messages,
                    tools=self._build_tool_config(),
                    system=system_prompt,
                    betas=[self.beta_header],
                )
            except Exception as e:
                print(f"   ❌ API error: {e}")
                raise

            # Add Claude's response to conversation
            messages.append({
                "role": "assistant",
                "content": response.content
            })

            # Process tool use requests
            tool_results = []
            has_tool_use = False

            for block in response.content:
                if block.type == "tool_use":
                    has_tool_use = True
                    action = block.input.get("action", "unknown")

                    if verbose:
                        print(f"   🔧 Tool: {action}")

                    # Execute the tool action
                    try:
                        result = await self.tool_executor.execute_action(
                            action=action,
                            params=block.input
                        )

                        # Store screenshots
                        if action == "screenshot" and result:
                            screenshots.append(result)

                        # Format result for Claude
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result if isinstance(result, (str, list)) else str(result)
                        })

                    except Exception as e:
                        print(f"   ❌ Tool execution error: {e}")
                        # Send error back to Claude
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": f"Error: {str(e)}",
                            "is_error": True
                        })

                elif block.type == "text" and verbose:
                    # Print Claude's thinking
                    if block.text.strip():
                        print(f"   💭 Claude: {block.text[:100]}...")

            # If no tool use, task is complete
            if not has_tool_use:
                if verbose:
                    print(f"   ✅ Task completed in {iterations} iterations")

                return {
                    "messages": messages,
                    "screenshots": screenshots,
                    "iterations": iterations,
                    "success": True
                }

            # Add tool results to conversation
            messages.append({
                "role": "user",
                "content": tool_results
            })

        # Max iterations reached
        print(f"   ⚠️  Max iterations ({max_iterations}) reached")
        return {
            "messages": messages,
            "screenshots": screenshots,
            "iterations": iterations,
            "success": False
        }

    def _build_tool_config(self) -> List[Dict]:
        """Build Computer Use tool configuration"""
        return [{
            "type": "computer_20250124",
            "name": "computer",
            "display_width_px": self.display_width,
            "display_height_px": self.display_height,
            "display_number": 1,
        }]

    def _build_default_system_prompt(self) -> str:
        """Build default system prompt for Computer Use"""
        return """You are an AI assistant with computer control capabilities for capturing product screenshots.

IMPORTANT INSTRUCTIONS:
1. After each action, take a screenshot to verify the outcome
2. Explicitly evaluate if you've achieved the desired result
3. If something isn't working, try alternative approaches
4. Be systematic and methodical
5. Wait for pages to fully load before capturing screenshots
6. Verify that content is visible and correct before confirming success

When navigating web pages:
- Wait for visual confirmation that pages have loaded
- Look for specific content or UI elements mentioned in the task
- If you see loading indicators, wait for them to disappear
- Take screenshots to confirm each step was successful

For authentication:
- Carefully handle any credentials provided
- Verify successful login by checking for authenticated UI elements
- Wait for post-login redirects to complete
"""

    @staticmethod
    def screenshot_to_base64(screenshot_bytes: bytes) -> str:
        """
        Convert screenshot bytes to base64-encoded PNG

        Args:
            screenshot_bytes: Raw screenshot image bytes

        Returns:
            Base64-encoded PNG string with data URI prefix
        """
        try:
            img = Image.open(io.BytesIO(screenshot_bytes))
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            base64_data = base64.b64encode(buffered.getvalue()).decode()
            return f"data:image/png;base64,{base64_data}"
        except Exception as e:
            raise RuntimeError(f"Failed to convert screenshot to base64: {e}")

    @staticmethod
    def base64_to_bytes(base64_data: str) -> bytes:
        """
        Convert base64-encoded image to bytes

        Args:
            base64_data: Base64 string (with or without data URI prefix)

        Returns:
            Raw image bytes
        """
        # Remove data URI prefix if present
        if base64_data.startswith("data:image"):
            base64_data = base64_data.split(",")[1]

        return base64.b64decode(base64_data)


class MaxIterationsError(Exception):
    """Raised when agent loop exceeds maximum iterations"""
    pass


class ToolExecutorError(Exception):
    """Raised when tool executor fails"""
    pass
