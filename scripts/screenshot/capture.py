"""
Generic screenshot capture framework using Playwright

This module provides a reusable framework for capturing screenshots
of web applications with authentication support.
"""

import os
import json
from playwright.sync_api import sync_playwright, Page, BrowserContext
from pathlib import Path
from typing import Optional, Dict, Callable
import sys

# Add parent directory to path for config import
sys.path.insert(0, str(Path(__file__).parent.parent))
import config as cfg
from screenshot.base import ScreenshotCapturerBase


class ScreenshotCapturer(ScreenshotCapturerBase):
    """Generic screenshot capture framework"""

    def __init__(
        self,
        auth_session_file: Optional[str] = None,
        viewport_width: Optional[int] = None,
        viewport_height: Optional[int] = None,
        output_dir: Optional[str] = None,
        headless: bool = True
    ):
        """
        Initialize screenshot capturer

        Args:
            auth_session_file: Path to saved auth session (default: from config)
            viewport_width: Browser viewport width (default: from config)
            viewport_height: Browser viewport height (default: from config)
            output_dir: Directory to save screenshots (default: from config)
            headless: Run browser in headless mode (default: True)
        """
        try:
            config = cfg.get_screenshot_config()
            self.auth_session_file = auth_session_file or config['auth_session_file']
            self.viewport_width = viewport_width or config['viewport_width']
            self.viewport_height = viewport_height or config['viewport_height']
            self.output_dir = output_dir or config['output_dir']
        except:
            # Fallback defaults if config not available
            self.auth_session_file = auth_session_file or './scripts/auth_session.json'
            self.viewport_width = viewport_width or 1470
            self.viewport_height = viewport_height or 840
            self.output_dir = output_dir or './demo/docs/product_documentation/screenshots'

        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()

    def start(self):
        """Start browser with authentication"""
        print(f"🌐 Starting browser...")
        print(f"   Viewport: {self.viewport_width}x{self.viewport_height}")
        print(f"   Headless: {self.headless}")

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)

        # Load authentication session if available
        storage_state = None
        if os.path.exists(self.auth_session_file):
            print(f"   Loading auth session: {self.auth_session_file}")
            with open(self.auth_session_file, 'r') as f:
                storage_state = json.load(f)
        else:
            print(f"   ⚠️  No auth session found: {self.auth_session_file}")
            print(f"      Screenshots may fail if authentication is required")
            print(f"      Run auth_manager.py first to save a session")

        # Create browser context with auth
        self.context = self.browser.new_context(
            viewport={'width': self.viewport_width, 'height': self.viewport_height},
            storage_state=storage_state
        )

        self.page = self.context.new_page()
        print("   ✅ Browser ready\n")

    def stop(self):
        """Stop browser"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        print("\n✅ Browser closed")

    def navigate(self, url: str, wait_for: str = 'networkidle', timeout: int = 30000):
        """
        Navigate to a URL

        Args:
            url: URL to navigate to
            wait_for: Wait for condition ('load', 'networkidle', 'domcontentloaded')
            timeout: Timeout in milliseconds
        """
        print(f"📍 Navigating to: {url}")
        self.page.goto(url, wait_until=wait_for, timeout=timeout)
        print(f"   ✅ Page loaded")

    def wait_for_selector(self, selector: str, timeout: int = 10000):
        """
        Wait for an element to appear

        Args:
            selector: CSS selector
            timeout: Timeout in milliseconds
        """
        print(f"   ⏳ Waiting for: {selector}")
        self.page.wait_for_selector(selector, timeout=timeout)

    def click(self, selector: str):
        """
        Click an element

        Args:
            selector: CSS selector
        """
        print(f"   🖱️  Clicking: {selector}")
        self.page.click(selector)

    def wait(self, milliseconds: int):
        """
        Wait for a specified time

        Args:
            milliseconds: Time to wait in milliseconds
        """
        self.page.wait_for_timeout(milliseconds)

    def scroll_to(self, selector: str):
        """
        Scroll to an element

        Args:
            selector: CSS selector
        """
        self.page.evaluate(f'''
            document.querySelector("{selector}").scrollIntoView({{
                behavior: "smooth",
                block: "center"
            }})
        ''')
        self.wait(500)  # Wait for scroll to complete

    def capture(
        self,
        filename: str,
        selector: Optional[str] = None,
        full_page: bool = False
    ) -> str:
        """
        Capture a screenshot

        Args:
            filename: Output filename (without extension)
            selector: CSS selector to capture specific element (optional)
            full_page: Capture full scrollable page (default: False)

        Returns:
            Path to saved screenshot
        """
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

        # Add .png extension if not present
        if not filename.endswith('.png'):
            filename += '.png'

        output_path = os.path.join(self.output_dir, filename)

        print(f"📸 Capturing: {filename}")

        if selector:
            # Capture specific element
            element = self.page.query_selector(selector)
            if element:
                element.screenshot(path=output_path)
            else:
                print(f"   ⚠️  Element not found: {selector}")
                print(f"   Capturing full page instead")
                self.page.screenshot(path=output_path, full_page=full_page)
        else:
            # Capture full page or viewport
            self.page.screenshot(path=output_path, full_page=full_page)

        print(f"   ✅ Saved: {output_path}")
        return output_path

    def run_workflow(self, workflow: Callable[[Page], None]):
        """
        Run a custom workflow function

        The workflow function receives the Playwright page object
        and can perform any operations.

        Args:
            workflow: Function that takes a Page object

        Example:
            def my_workflow(page):
                page.goto('https://example.com')
                page.click('button')
                page.screenshot(path='result.png')

            capturer.run_workflow(my_workflow)
        """
        workflow(self.page)


def capture_screenshots_from_plan(plan: list, base_url: str, implementation="auto"):
    """
    Capture screenshots based on a plan

    NOTE: This function now supports multiple implementations (Playwright, Computer Use).
    It's recommended to use screenshot.factory.create_capturer_from_plan() for new code.

    Args:
        plan: List of screenshot plan dicts with 'name', 'url', 'selector' (optional), etc.
        base_url: Base URL for the application
        implementation: "auto" (from config), "playwright", or "computer_use"

    Example plan:
        [
            {
                'name': 'dashboard-overview',
                'url': '/dashboard',
                'wait_for': '.dashboard-container',
                'wait_time': 2000
            },
            {
                'name': 'settings-page',
                'url': '/settings',
                'selector': '.settings-panel',
                'full_page': True
            }
        ]
    """
    # For backward compatibility, use factory if not "auto" or if config specifies Computer Use
    if implementation != "auto":
        from screenshot.factory import create_capturer
        capturer_instance = create_capturer(implementation=implementation)
    else:
        # Check config to see if we should use factory
        try:
            config = cfg.get_screenshot_config()
            if config.get('implementation') == 'computer_use':
                from screenshot.factory import create_capturer
                capturer_instance = create_capturer(implementation="computer_use")
            else:
                capturer_instance = ScreenshotCapturer()
        except:
            capturer_instance = ScreenshotCapturer()

    with capturer_instance as capturer:
        for item in plan:
            name = item['name']
            url = base_url + item.get('url', '')

            # Navigate
            capturer.navigate(url)

            # Wait for specific element if specified
            if 'wait_for' in item:
                capturer.wait_for_selector(item['wait_for'])

            # Additional wait time
            if 'wait_time' in item:
                capturer.wait(item['wait_time'])

            # Scroll to element if specified
            if 'scroll_to' in item:
                capturer.scroll_to(item['scroll_to'])

            # Capture
            capturer.capture(
                filename=name,
                selector=item.get('selector'),
                full_page=item.get('full_page', False)
            )

    print(f"\n✅ Captured {len(plan)} screenshots")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Generic screenshot capture tool'
    )
    parser.add_argument(
        'url',
        help='URL to capture'
    )
    parser.add_argument(
        '--output',
        help='Output filename',
        required=True
    )
    parser.add_argument(
        '--selector',
        help='CSS selector to capture specific element'
    )
    parser.add_argument(
        '--full-page',
        action='store_true',
        help='Capture full scrollable page'
    )
    parser.add_argument(
        '--no-headless',
        action='store_true',
        help='Show browser window'
    )

    args = parser.parse_args()

    with ScreenshotCapturer(headless=not args.no_headless) as capturer:
        capturer.navigate(args.url)
        capturer.wait(2000)  # Wait for page to stabilize
        capturer.capture(
            filename=args.output,
            selector=args.selector,
            full_page=args.full_page
        )
