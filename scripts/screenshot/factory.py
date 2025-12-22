"""
Screenshot Capturer Factory

This module provides a factory function for creating screenshot capturers.
Uses Claude's Computer Use API for intelligent, reliable screenshot capture.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from screenshot.base import ScreenshotCapturerBase


def create_capturer(**kwargs) -> ScreenshotCapturerBase:
    """
    Factory function to create screenshot capturer

    Creates a Computer Use-based screenshot capturer with intelligent
    authentication, visual navigation, and reliable content capture.

    Args:
        **kwargs: Additional arguments passed to capturer constructor
            - auth_credentials: Optional dict with authentication details
            - viewport_width: Display width in pixels
            - viewport_height: Display height in pixels
            - output_dir: Directory to save screenshots
            - api_key: Anthropic API key
            - model: Claude model to use

    Returns:
        ComputerUseScreenshotCapturer: Configured screenshot capturer instance

    Raises:
        ImportError: If Computer Use dependencies are not available

    Examples:
        # Use with defaults from config
        with create_capturer() as capturer:
            capturer.navigate("https://example.com")
            capturer.capture("screenshot.png")

        # Override specific settings
        with create_capturer(viewport_width=1920, viewport_height=1080) as capturer:
            capturer.navigate("https://example.com")
            capturer.capture("screenshot.png")
    """
    try:
        from screenshot.computer_use_capture import ComputerUseScreenshotCapturer
        return ComputerUseScreenshotCapturer(**kwargs)
    except ImportError as e:
        raise ImportError(
            "Computer Use implementation requires additional dependencies. "
            "Install with: pip install anthropic pillow pyautogui pyotp aiohttp\n"
            f"Original error: {e}"
        )


def create_capturer_from_plan(plan: list, base_url: str):
    """
    Create capturer and execute screenshot plan

    Convenience function that creates a Computer Use capturer and executes
    a screenshot plan (list of URLs and capture instructions).

    Args:
        plan: List of screenshot plan dicts with:
            - name: Screenshot filename (without extension)
            - url: URL path to navigate to (relative to base_url)
            - wait_for: Optional CSS selector to wait for (converted to visual description)
            - wait_time: Optional additional wait time in milliseconds
            - selector: Optional CSS selector to capture specific element
            - scroll_to: Optional CSS selector to scroll to
            - full_page: Optional boolean for full-page capture
        base_url: Base URL for the application

    Example:
        plan = [
            {'name': 'dashboard', 'url': '/dashboard', 'wait_for': '.main-content'},
            {'name': 'settings', 'url': '/settings', 'wait_time': 2000},
        ]
        create_capturer_from_plan(plan, 'https://app.example.com')
    """
    with create_capturer() as capturer:
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


# Export main functions
__all__ = [
    'create_capturer',
    'create_capturer_from_plan',
    'ScreenshotCapturerBase',
]
