"""
Gemini Computer Use Client

This module provides an adapter for Google's Gemini models to mimic the
Computer Use API interface utilized by max-doc-ai.
"""

import os
import time
import base64
import io
import asyncio
from typing import Dict, List, Any, Optional
from PIL import Image
import google.generativeai as genai
from google.generativeai.types import content_types
from google.protobuf import struct_pb2

class GeminiComputerUseClient:
    """
    Adapter for Gemini to support Computer Use tasks.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gemini-2.5-flash",
        display_width: int = 1280,
        display_height: int = 800,
    ):
        """
        Initialize Gemini client
        """
        genai.configure(api_key=api_key)
        self.model_name = model
        self.display_width = display_width
        self.display_height = display_height
        self.tool_executor = None
        
        # Initialize the model with tools
        # We map the "computer" tool actions to a single function for simplicity
        self.tools_def = [
            {
                "function_declarations": [
                    {
                        "name": "perform_action",
                        "description": "Perform an action on the computer screen (click, type, scroll, screenshot, etc).",
                        "parameters": {
                            "type": "OBJECT",
                            "properties": {
                                "action": {
                                    "type": "STRING",
                                    "description": "The action to perform.",
                                    "enum": ["screenshot", "left_click", "type", "key", "mouse_move", "scroll", "wait", "right_click", "double_click", "left_click_drag"]
                                },
                                "coordinate": {
                                    "type": "ARRAY",
                                    "items": {"type": "INTEGER"},
                                    "description": "The [x, y] coordinates for the action (required for click, mouse_move, right_click, double_click, left_click_drag)."
                                },
                                "text": {
                                    "type": "STRING",
                                    "description": "The text to type (required for type action)."
                                },
                                "key": {
                                    "type": "STRING",
                                    "description": "The key or combination to press (required for key action)."
                                },
                                "wait_duration_ms": {
                                    "type": "INTEGER",
                                    "description": "Duration to wait in milliseconds (for wait action)."
                                },
                                "scroll_direction": {
                                    "type": "STRING",
                                    "enum": ["up", "down"],
                                    "description": "Direction to scroll."
                                },
                                "scroll_amount": {
                                    "type": "INTEGER",
                                    "description": "Amount to scroll."
                                }
                            },
                            "required": ["action"]
                        }
                    }
                ]
            }
        ]
        
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            tools=self.tools_def
        )

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
        """
        if not self.tool_executor:
            raise RuntimeError("Tool executor not set.")

        chat = self.model.start_chat(history=[])
        
        # Initial prompt including system instructions as the first user message context
        full_prompt = f"""
{system_prompt or ''}

TASK: {task_prompt}

You have access to a 'perform_action' tool to interact with the computer.
ALWAYS take a screenshot after an action to verify the result.
Stop when the task is complete.
"""
        
        messages = [] # Keep local history for return value
        screenshots = []
        iterations = 0
        success = False
        
        current_input = full_prompt
        
        # Take an initial screenshot to give context
        try:
            initial_screen_b64 = await self.tool_executor.execute_action("screenshot", {})
            # Remove data prefix
            if initial_screen_b64.startswith("data:"):
                initial_screen_b64 = initial_screen_b64.split(",")[1]
            
            initial_image = Image.open(io.BytesIO(base64.b64decode(initial_screen_b64)))
            current_parts = [current_input, initial_image]
            screenshots.append(initial_screen_b64) # Store simplified
        except Exception as e:
            if verbose: print(f"Warning: Initial screenshot failed: {e}")
            current_parts = [current_input]

        while iterations < max_iterations:
            iterations += 1
            if verbose:
                print(f"   🔄 Gemini Agent loop iteration {iterations}/{max_iterations}")

            try:
                response = chat.send_message(current_parts)
                # Handle responses that are purely function calls (no text)
                try:
                    text_content = response.text
                except ValueError:
                    text_content = "" # Function call only
                
                messages.append({"role": "model", "content": text_content})
            except Exception as e:
                print(f"   ❌ API error: {e}")
                raise

            # Process function calls
            function_calls = []
            for part in response.parts:
                if fn := part.function_call:
                    function_calls.append(fn)

            if not function_calls:
                # No tool use, assume task completion or question
                if verbose:
                     print(f"   💭 Gemini: {response.text}")
                     print(f"   ✅ Task likely completed (no tool use)")
                success = True # Assume success if it stops calling tools
                break

            # Execute tools
            tool_outputs = []
            has_screenshot = False
            
            for fc in function_calls:
                if fc.name == "perform_action":
                    args = dict(fc.args)
                    action = args.get("action")
                    if verbose: print(f"   🔧 Tool: {action} {args}")
                    
                    try:
                        # Clean args for tool executor (it expects specific keys)
                        # coordinate is repeated by protobuf to list
                        if 'coordinate' in args:
                            args['coordinate'] = list(args['coordinate'])
                            
                        result = await self.tool_executor.execute_action(action, args)
                        
                        # Handle screenshot result (special handling for Gemini vision)
                        if action == "screenshot":
                            has_screenshot = True
                            if result.startswith("data:"):
                                b64_data = result.split(",")[1]
                            else:
                                b64_data = result
                            
                            img = Image.open(io.BytesIO(base64.b64decode(b64_data)))
                            # We send the image object to Gemini
                            tool_outputs.append({
                                "function_response": {
                                    "name": "perform_action",
                                    "response": {"result": "Screenshot captured (image attached)"}
                                }
                            })
                            # We will attach the image to the NEXT user message parts
                            # But wait, send_message_response needs to match function_calls
                            # We can't easily mix text/images in function_response in simple chat?
                            # Actually with send_message we provide a list of parts.
                            
                            screenshots.append(result)
                        else:
                            tool_outputs.append({
                                "function_response": {
                                    "name": "perform_action",
                                    "response": {"result": str(result)}
                                }
                            })

                    except Exception as e:
                        print(f"   ❌ Tool execution error: {e}")
                        tool_outputs.append({
                            "function_response": {
                                "name": "perform_action",
                                "response": {"error": str(e)}
                            }
                        })

            # Prepare next input
            # If we had function calls, we must send function responses
            # For the screenshot, we want to provide the visual context.
            
            # Construct the response parts
            response_parts = []
            for output in tool_outputs:
                response_parts.append(output)
            
            # If we took a screenshot, we should append it to the context, 
            # but in the chat.send_message flow with function calling, 
            # we typically respond with the function output.
            # To get the vision capability, we might need to send a follow-up 
            # user message "Here is the screen now: [Image]"?
            # Or can we include the image in the function response? 
            # Gemini documentation says function response is JSON.
            
            # Strategy: Send function responses using the chat object (which handles history).
            # Then, if there was a screenshot, send a new USER message with the image.
            
            # WAIT: chat.send_message accepts 'parts'.
            # We must reply to the function call first.
            try:
                chat.send_message(response_parts)
                # messages.append({"role": "function", "content": ...}) 
            except Exception as e:
                 print(f"   ❌ Error sending function response: {e}")
                 raise

            # Now, if we have a new state (screenshot), we need to show it to the model
            # for the NEXT turn.
            if has_screenshot:
                # We need to grab the last screenshot captured
                last_shot_b64 = screenshots[-1]
                if last_shot_b64.startswith("data:"):
                    last_shot_b64 = last_shot_b64.split(",")[1]
                img = Image.open(io.BytesIO(base64.b64decode(last_shot_b64)))
                
                # We manually trigger the next turn with the image
                current_parts = ["Here is the screen after the action:", img]
            else:
                # Just prompt to continue
                current_parts = ["Action completed. Ensure you verify the result. What is the next step?"]
            
        return {
            "messages": messages,
            "screenshots": screenshots,
            "iterations": iterations,
            "success": success
        }

