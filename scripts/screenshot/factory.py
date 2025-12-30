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


def create_capturer(provider: str = 'computer_use', **kwargs) -> ScreenshotCapturerBase:
    """
    Factory function to create screenshot capturer

    Args:
        provider: 'computer_use' or 'playwright'
        **kwargs: Additional arguments passed to capturer constructor
    """
    if provider == 'playwright':
        from screenshot.capture import ScreenshotCapturer
        return ScreenshotCapturer(**kwargs)
    
    try:
        from screenshot.computer_use_capture import ComputerUseScreenshotCapturer
        return ComputerUseScreenshotCapturer(**kwargs)
    except ImportError as e:
        raise ImportError(
            "Computer Use implementation requires additional dependencies. "
            "Install with: pip install anthropic pillow pyautogui pyotp aiohttp\n"
            f"Original error: {e}"
        )


def create_capturer_from_plan(plan: list, base_url: str, provider: str = 'computer_use'):
    """
    Create capturer and execute screenshot plan

    Args:
        plan: List of screenshot plan dicts
        base_url: Base URL for the application
        provider: 'computer_use' or 'playwright'
    """
    with create_capturer(provider=provider) as capturer:
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
