"""
Base interface for screenshot capturers

This module defines the abstract base class that all screenshot
capture implementations must inherit from (Playwright, Computer Use, etc.)
"""

from abc import ABC, abstractmethod
from typing import Optional, Callable


class ScreenshotCapturerBase(ABC):
    """Abstract base class for screenshot capture implementations"""

    @abstractmethod
    def __enter__(self):
        """Context manager entry"""
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        pass

    @abstractmethod
    def start(self):
        """Start the capture session (initialize browser, authenticate, etc.)"""
        pass

    @abstractmethod
    def stop(self):
        """Stop the capture session and clean up resources"""
        pass

    @abstractmethod
    def navigate(self, url: str, wait_for: str = 'networkidle', timeout: int = 30000):
        """
        Navigate to a URL

        Args:
            url: URL to navigate to
            wait_for: Wait condition ('load', 'networkidle', 'domcontentloaded')
            timeout: Timeout in milliseconds
        """
        pass

    @abstractmethod
    def wait_for_selector(self, selector: str, timeout: int = 10000):
        """
        Wait for an element to appear

        Args:
            selector: CSS selector (implementation may convert to visual description)
            timeout: Timeout in milliseconds
        """
        pass

    @abstractmethod
    def click(self, selector: str):
        """
        Click an element

        Args:
            selector: CSS selector or visual description
        """
        pass

    @abstractmethod
    def wait(self, milliseconds: int):
        """
        Wait for a specified time

        Args:
            milliseconds: Time to wait in milliseconds
        """
        pass

    @abstractmethod
    def scroll_to(self, selector: str):
        """
        Scroll to an element

        Args:
            selector: CSS selector or visual description
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def run_workflow(self, workflow: Callable):
        """
        Run a custom workflow function

        The workflow function receives implementation-specific page/context objects
        and can perform any operations.

        Args:
            workflow: Function that performs custom actions
        """
        pass
