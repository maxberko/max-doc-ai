"""
Computer Use Screenshot Capturer

This module provides screenshot capture using Claude's Computer Use API.
It replaces Playwright's DOM-based automation with visual recognition and
autonomous navigation, solving authentication and reliability issues.
"""

import os
import sys
import time
import asyncio
from pathlib import Path
from typing import Optional, Dict, Callable

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from screenshot.base import ScreenshotCapturerBase
from screenshot.computer_use_client import ComputerUseClient
from screenshot.computer_use_tools import ComputerUseTool

try:
    import config as cfg
except ImportError:
    cfg = None


class ComputerUseScreenshotCapturer(ScreenshotCapturerBase):
    """
    Computer Use-based screenshot capturer

    Uses Claude's Computer Use API for visual navigation and screenshot capture.
    Solves Playwright problems with:
    - Authentication (visual login, no session management)
    - Reliability (Claude waits for content naturally)
    - Maintenance (no CSS selectors to update)
    """

    def __init__(
        self,
        auth_credentials: Optional[Dict] = None,
        viewport_width: Optional[int] = None,
        viewport_height: Optional[int] = None,
        output_dir: Optional[str] = None,
        api_key: Optional[str] = None,
        model: str = "claude-sonnet-4-5"
    ):
        """
        Initialize Computer Use screenshot capturer

        Args:
            auth_credentials: Dict with authentication details (optional)
            viewport_width: Display width in pixels (default: from config or 1280)
            viewport_height: Display height in pixels (default: from config or 800)
            output_dir: Directory to save screenshots (default: from config)
            api_key: Anthropic API key (default: from env or config)
            model: Claude model to use (default: claude-sonnet-4-5)
        """
        # Load from config if available
        if cfg:
            try:
                screenshot_config = cfg.get_screenshot_config()

                self.viewport_width = viewport_width or screenshot_config.get('viewport_width', 1280)
                self.viewport_height = viewport_height or screenshot_config.get('viewport_height', 800)
                self.output_dir = output_dir or screenshot_config.get('output_dir', './output/screenshots')

                # API configuration
                self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY') or screenshot_config.get('api_key')
                self.model = model or screenshot_config.get('model', 'claude-sonnet-4-5')

                # Auth config
                if auth_credentials is None:
                    auth_config = screenshot_config.get('auth', {})
                    if auth_config.get('enabled'):
                        self.auth_credentials = {
                            'enabled': True,
                            'type': auth_config.get('type', 'username_password'),
                            'login_url': auth_config.get('login_url'),
                            'username': os.getenv('SCREENSHOT_USER') or auth_config.get('username'),
                            'password': os.getenv('SCREENSHOT_PASS') or auth_config.get('password'),
                            'sso_provider': auth_config.get('sso_provider'),
                        }
                    else:
                        self.auth_credentials = None
                else:
                    self.auth_credentials = auth_credentials

            except Exception as e:
                print(f"⚠️  Could not load config: {e}. Using defaults.")
                self._set_defaults(viewport_width, viewport_height, output_dir, api_key, model, auth_credentials)
        else:
            self._set_defaults(viewport_width, viewport_height, output_dir, api_key, model, auth_credentials)

        # Initialize Computer Use components
        self.client = ComputerUseClient(
            api_key=self.api_key,
            model=self.model,
            display_width=self.viewport_width,
            display_height=self.viewport_height
        )

        self.tool_executor = ComputerUseTool(
            display_width=self.viewport_width,
            display_height=self.viewport_height
        )

        # Connect client and executor
        self.client.set_tool_executor(self.tool_executor)

        # Session state
        self.session_active = False
        self.current_url = None
        self.authenticated = False

    def _set_defaults(self, viewport_width, viewport_height, output_dir, api_key, model, auth_credentials):
        """Set default values when config is not available"""
        self.viewport_width = viewport_width or 1280
        self.viewport_height = viewport_height or 800
        self.output_dir = output_dir or './output/screenshots'
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        self.model = model or 'claude-sonnet-4-5'
        self.auth_credentials = auth_credentials

    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()

    def start(self):
        """Start session with optional authentication"""
        print("🌐 Starting Computer Use session...")
        print(f"   Viewport: {self.viewport_width}x{self.viewport_height}")
        print(f"   Model: {self.model}")

        # Authenticate if credentials provided
        if self.auth_credentials and self.auth_credentials.get('enabled'):
            self._authenticate()
            self.authenticated = True

        self.session_active = True
        print("   ✅ Session ready\n")

    def stop(self):
        """Stop session"""
        self.session_active = False
        self.authenticated = False
        print("\n✅ Session closed")

    def _authenticate(self):
        """Authenticate using Computer Use visual navigation"""
        print("🔐 Authenticating...")

        auth_prompt = self._build_auth_prompt()
        system_prompt = self._build_auth_system_prompt()

        try:
            result = asyncio.run(self.client.execute_task(
                task_prompt=auth_prompt,
                system_prompt=system_prompt,
                max_iterations=25,
                verbose=True
            ))

            if result.get('success'):
                print("   ✅ Authentication complete")
            else:
                print("   ⚠️  Authentication may have failed (max iterations reached)")

        except Exception as e:
            print(f"   ❌ Authentication error: {e}")
            raise RuntimeError(f"Authentication failed: {e}")

    def _build_auth_prompt(self) -> str:
        """Build authentication task prompt"""
        auth = self.auth_credentials
        login_url = auth.get('login_url', 'the application login page')

        prompt = f"""Log in to {login_url}.

Steps to follow:
1. Navigate to the login page
2. Identify the login form visually
3. Enter the provided credentials
4. Submit the form (click login button or press Enter)
5. Wait for authentication to complete (look for dashboard, profile, or authenticated UI)
6. Take a screenshot to verify you're logged in

IMPORTANT:
- Wait for each page to fully load before proceeding
- Look for visual confirmation of successful login
- If you see SSO options, click the appropriate provider button first
- Verify you're on an authenticated page before completing
"""

        if auth.get('type') == 'sso' and auth.get('sso_provider'):
            prompt += f"\nNote: Use {auth['sso_provider']} SSO sign-in if available."

        return prompt

    def _build_auth_system_prompt(self) -> str:
        """Build system prompt with credentials"""
        auth = self.auth_credentials

        system_prompt = f"""You are authenticating to a web application to capture screenshots.

<robot_credentials>
  <username>{auth.get('username')}</username>
  <password>{auth.get('password')}</password>
</robot_credentials>

CRITICAL INSTRUCTIONS:
- Be extremely careful with the credentials
- Only use them for the authentication process
- Wait for visual confirmation at each step
- Do not proceed until you see the authenticated interface
- Take screenshots to verify progress
"""

        return system_prompt

    def navigate(self, url: str, wait_for: str = 'networkidle', timeout: int = 30000):
        """
        Navigate to URL using Computer Use

        Args:
            url: URL to navigate to
            wait_for: Ignored (Computer Use handles waiting naturally)
            timeout: Ignored (Computer Use uses max_iterations)
        """
        print(f"📍 Navigating to: {url}")

        prompt = f"""Navigate to {url} in the web browser.

Steps:
1. Click on the browser address bar
2. Type the URL: {url}
3. Press Enter
4. Wait for the page to fully load (look for content, no loading spinners)
5. Take a screenshot to verify the page loaded correctly

IMPORTANT: Wait until you see the actual page content before confirming success.
"""

        try:
            result = asyncio.run(self.client.execute_task(
                task_prompt=prompt,
                max_iterations=15,
                verbose=False
            ))

            if result.get('success'):
                self.current_url = url
                print(f"   ✅ Page loaded")
            else:
                print(f"   ⚠️  Page may not have loaded fully")

        except Exception as e:
            print(f"   ❌ Navigation error: {e}")
            raise RuntimeError(f"Navigation failed: {e}")

    def wait_for_selector(self, selector: str, timeout: int = 10000):
        """
        Wait for element to appear (Computer Use adaptation)

        Args:
            selector: CSS selector (will be converted to visual description)
            timeout: Ignored (Computer Use uses max_iterations)
        """
        print(f"   ⏳ Waiting for: {selector}")

        visual_description = self._selector_to_description(selector)

        prompt = f"""Check if the following UI element is visible on screen:
{visual_description}

Steps:
1. Take a screenshot
2. Look for the element
3. If not visible, wait 2 seconds and check again
4. Repeat until found or after checking 5 times

Confirm when you see the element.
"""

        try:
            asyncio.run(self.client.execute_task(
                task_prompt=prompt,
                max_iterations=8,
                verbose=False
            ))
        except Exception as e:
            print(f"   ⚠️  Element may not have appeared: {e}")

    def click(self, selector: str):
        """
        Click element by selector

        Args:
            selector: CSS selector or visual description
        """
        print(f"   🖱️  Clicking: {selector}")

        visual_description = self._selector_to_description(selector)

        prompt = f"""Find and click on the following UI element:
{visual_description}

Steps:
1. Take a screenshot to see the current state
2. Locate the element visually
3. Click on it
4. Wait briefly for any UI updates
5. Take another screenshot to confirm the action

Verify the click had the expected effect.
"""

        try:
            asyncio.run(self.client.execute_task(
                task_prompt=prompt,
                max_iterations=8,
                verbose=False
            ))
        except Exception as e:
            print(f"   ❌ Click error: {e}")
            raise RuntimeError(f"Click failed: {e}")

    def wait(self, milliseconds: int):
        """
        Wait for specified time

        Args:
            milliseconds: Time to wait in milliseconds
        """
        time.sleep(milliseconds / 1000.0)

    def scroll_to(self, selector: str):
        """
        Scroll to element

        Args:
            selector: CSS selector or visual description
        """
        print(f"   📜 Scrolling to: {selector}")

        visual_description = self._selector_to_description(selector)

        prompt = f"""Scroll the page to make the following element visible:
{visual_description}

Steps:
1. Take a screenshot to see current scroll position
2. Identify if the element is already visible
3. If not, scroll down until you see it
4. Take a screenshot to confirm element is visible
"""

        try:
            asyncio.run(self.client.execute_task(
                task_prompt=prompt,
                max_iterations=10,
                verbose=False
            ))
        except Exception as e:
            print(f"   ⚠️  Scroll may not have completed: {e}")

    def capture(
        self,
        filename: str,
        selector: Optional[str] = None,
        full_page: bool = False
    ) -> str:
        """
        Capture screenshot

        Args:
            filename: Output filename (without extension)
            selector: CSS selector to capture specific element (optional)
            full_page: Capture full scrollable page (optional)

        Returns:
            Path to saved screenshot
        """
        print(f"📸 Capturing: {filename}")

        # Build prompt based on parameters
        if selector:
            visual_description = self._selector_to_description(selector)
            prompt = f"""Take a screenshot showing the following element:
{visual_description}

Ensure the element is visible and centered in the viewport if possible.
"""
        elif full_page:
            prompt = """Capture the full page content.

If the page is longer than the viewport:
1. Scroll to the top
2. Take multiple screenshots while scrolling down
3. I will use the final complete screenshot

Otherwise, just take a single screenshot of the current viewport.
"""
        else:
            prompt = """Take a screenshot of the current viewport.

Ensure the page is fully loaded and shows the content clearly.
"""

        try:
            result = asyncio.run(self.client.execute_task(
                task_prompt=prompt,
                max_iterations=10,
                verbose=False
            ))

            # Get the last screenshot from the result
            screenshots = result.get('screenshots', [])
            if not screenshots:
                raise RuntimeError("No screenshot was captured")

            # Save screenshot
            output_path = self._save_screenshot(screenshots[-1], filename)
            print(f"   ✅ Saved: {output_path}")

            return output_path

        except Exception as e:
            print(f"   ❌ Capture error: {e}")
            raise RuntimeError(f"Screenshot capture failed: {e}")

    def run_workflow(self, workflow: Callable):
        """
        Run custom workflow

        Args:
            workflow: Function that receives this capturer instance

        Note: For Computer Use, workflows are defined as prompts rather
        than direct API calls. This method allows custom prompt-based workflows.
        """
        workflow(self)

    def _save_screenshot(self, base64_data: str, filename: str) -> str:
        """
        Save base64 screenshot to file

        Args:
            base64_data: Base64-encoded PNG (with or without data URI)
            filename: Output filename (without extension)

        Returns:
            Path to saved file
        """
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

        # Add .png extension if not present
        if not filename.endswith('.png'):
            filename += '.png'

        output_path = os.path.join(self.output_dir, filename)

        # Remove data URI prefix if present
        if base64_data.startswith("data:image"):
            base64_data = base64_data.split(",")[1]

        # Decode and save
        import base64
        image_data = base64.b64decode(base64_data)

        with open(output_path, 'wb') as f:
            f.write(image_data)

        return output_path

    def _selector_to_description(self, selector: str) -> str:
        """
        Convert CSS selector to visual description

        Args:
            selector: CSS selector string

        Returns:
            Human-readable visual description
        """
        # Handle common selector patterns
        if selector.startswith('.'):
            class_name = selector[1:].replace('-', ' ').replace('_', ' ')
            return f"Element with class '{selector[1:]}' (likely a {class_name} component)"
        elif selector.startswith('#'):
            id_name = selector[1:].replace('-', ' ').replace('_', ' ')
            return f"Element with id '{selector[1:]}' (likely the {id_name} section)"
        elif selector == 'button':
            return "A button element"
        elif selector == 'input':
            return "An input field"
        elif selector == 'a':
            return "A link"
        else:
            # Generic description
            tag_match = selector.split('[')[0].split('.')[0].split('#')[0]
            return f"Element matching selector '{selector}' (tag: {tag_match})"
