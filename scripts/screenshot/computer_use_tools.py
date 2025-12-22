"""
Computer Use Tool Executor

This module executes Computer Use tool actions on the desktop.
It translates Claude's action requests (screenshot, click, type, etc.)
into actual desktop automation operations.
"""

import time
import base64
import io
import os
import platform
from typing import Dict, Any, Optional
from PIL import ImageGrab, Image


# Try to import pyautogui for desktop automation
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    print("⚠️  Warning: pyautogui not available. Install with: pip install pyautogui")


class ComputerUseTool:
    """
    Executes Computer Use tool actions

    This class handles the execution of actions requested by Claude through
    the Computer Use API, such as taking screenshots, clicking, typing, etc.
    """

    def __init__(self, display_width: int = 1280, display_height: int = 800):
        """
        Initialize tool executor

        Args:
            display_width: Target display width in pixels
            display_height: Target display height in pixels
        """
        self.display_width = display_width
        self.display_height = display_height

        # Check if pyautogui is available
        if not PYAUTOGUI_AVAILABLE:
            print("⚠️  Desktop automation disabled. Many actions will fail.")

        # Disable pyautogui failsafe for automation
        if PYAUTOGUI_AVAILABLE:
            pyautogui.FAILSAFE = False

    async def execute_action(self, action: str, params: Dict[str, Any]) -> Any:
        """
        Execute a Computer Use action

        Args:
            action: Action name (screenshot, left_click, type, key, etc.)
            params: Action parameters

        Returns:
            Action result (varies by action type)

        Raises:
            ValueError: If action is unknown
            RuntimeError: If action execution fails
        """
        action_map = {
            "screenshot": self._screenshot,
            "left_click": self._click,
            "type": self._type_text,
            "key": self._press_key,
            "mouse_move": self._mouse_move,
            "scroll": self._scroll,
            "wait": self._wait,
            "right_click": self._right_click,
            "double_click": self._double_click,
            "left_click_drag": self._click_drag,
        }

        handler = action_map.get(action)
        if not handler:
            raise ValueError(f"Unknown action: {action}")

        try:
            return await handler(params)
        except Exception as e:
            raise RuntimeError(f"Failed to execute {action}: {e}")

    async def _screenshot(self, params: Dict[str, Any]) -> str:
        """
        Capture screenshot and return as base64

        Args:
            params: Empty dict (screenshot takes no parameters)

        Returns:
            Base64-encoded PNG with data URI prefix
        """
        try:
            # Capture the screen
            screenshot = ImageGrab.grab()

            # Resize to target dimensions if needed
            if screenshot.size != (self.display_width, self.display_height):
                screenshot = screenshot.resize(
                    (self.display_width, self.display_height),
                    Image.LANCZOS
                )

            # Convert to base64
            buffer = io.BytesIO()
            screenshot.save(buffer, format="PNG")
            base64_data = base64.b64encode(buffer.getvalue()).decode()

            return f"data:image/png;base64,{base64_data}"

        except Exception as e:
            raise RuntimeError(f"Screenshot capture failed: {e}")

    async def _click(self, params: Dict[str, Any]) -> str:
        """
        Perform mouse click at coordinates

        Args:
            params: Dict with 'coordinate' key containing [x, y] list

        Returns:
            Success message
        """
        if not PYAUTOGUI_AVAILABLE:
            return "Click simulated (pyautogui not available)"

        coordinate = params.get("coordinate", [])
        if len(coordinate) != 2:
            raise ValueError(f"Invalid coordinate: {coordinate}")

        x, y = coordinate

        # Scale coordinates if needed
        x_scaled, y_scaled = self._scale_coordinates(x, y)

        # Perform click
        pyautogui.click(x_scaled, y_scaled)

        # Small delay to allow UI to update
        time.sleep(0.3)

        return f"Clicked at ({x}, {y})"

    async def _type_text(self, params: Dict[str, Any]) -> str:
        """
        Type text using keyboard

        Args:
            params: Dict with 'text' key containing string to type

        Returns:
            Success message
        """
        if not PYAUTOGUI_AVAILABLE:
            return "Text typing simulated (pyautogui not available)"

        text = params.get("text", "")
        if not text:
            raise ValueError("No text provided to type")

        # Type the text
        pyautogui.write(text, interval=0.05)  # Small delay between keystrokes

        return f"Typed: {text[:50]}{'...' if len(text) > 50 else ''}"

    async def _press_key(self, params: Dict[str, Any]) -> str:
        """
        Press keyboard key or key combination

        Args:
            params: Dict with 'key' containing key name or combination

        Returns:
            Success message
        """
        if not PYAUTOGUI_AVAILABLE:
            return "Key press simulated (pyautogui not available)"

        key = params.get("key", "")
        if not key:
            raise ValueError("No key provided")

        # Handle key combinations (e.g., "ctrl+s", "cmd+c")
        if '+' in key:
            keys = key.split('+')
            pyautogui.hotkey(*keys)
        else:
            pyautogui.press(key)

        return f"Pressed key: {key}"

    async def _mouse_move(self, params: Dict[str, Any]) -> str:
        """
        Move mouse to coordinates

        Args:
            params: Dict with 'coordinate' key containing [x, y] list

        Returns:
            Success message
        """
        if not PYAUTOGUI_AVAILABLE:
            return "Mouse move simulated (pyautogui not available)"

        coordinate = params.get("coordinate", [])
        if len(coordinate) != 2:
            raise ValueError(f"Invalid coordinate: {coordinate}")

        x, y = coordinate
        x_scaled, y_scaled = self._scale_coordinates(x, y)

        pyautogui.moveTo(x_scaled, y_scaled, duration=0.2)

        return f"Moved mouse to ({x}, {y})"

    async def _scroll(self, params: Dict[str, Any]) -> str:
        """
        Scroll at given position

        Args:
            params: Dict with:
                - coordinate: [x, y] position to scroll at
                - scroll_direction: 'up' or 'down'
                - scroll_amount: number of scroll units (default: 3)

        Returns:
            Success message
        """
        if not PYAUTOGUI_AVAILABLE:
            return "Scroll simulated (pyautogui not available)"

        coordinate = params.get("coordinate", [self.display_width // 2, self.display_height // 2])
        direction = params.get("scroll_direction", "down")
        amount = params.get("scroll_amount", 3)

        x, y = coordinate
        x_scaled, y_scaled = self._scale_coordinates(x, y)

        # Move mouse to position first
        pyautogui.moveTo(x_scaled, y_scaled, duration=0.1)

        # Scroll (negative for down, positive for up)
        scroll_amount = -amount if direction == "down" else amount
        pyautogui.scroll(scroll_amount * 100)  # Multiply for noticeable effect

        return f"Scrolled {direction} by {amount}"

    async def _wait(self, params: Dict[str, Any]) -> str:
        """
        Wait for specified duration

        Args:
            params: Dict with 'wait_duration_ms' key (milliseconds)

        Returns:
            Success message
        """
        duration_ms = params.get("wait_duration_ms", 1000)
        duration_s = duration_ms / 1000.0

        time.sleep(duration_s)

        return f"Waited {duration_s}s"

    async def _right_click(self, params: Dict[str, Any]) -> str:
        """
        Perform right mouse click at coordinates

        Args:
            params: Dict with 'coordinate' key containing [x, y] list

        Returns:
            Success message
        """
        if not PYAUTOGUI_AVAILABLE:
            return "Right click simulated (pyautogui not available)"

        coordinate = params.get("coordinate", [])
        if len(coordinate) != 2:
            raise ValueError(f"Invalid coordinate: {coordinate}")

        x, y = coordinate
        x_scaled, y_scaled = self._scale_coordinates(x, y)

        pyautogui.rightClick(x_scaled, y_scaled)
        time.sleep(0.3)

        return f"Right clicked at ({x}, {y})"

    async def _double_click(self, params: Dict[str, Any]) -> str:
        """
        Perform double click at coordinates

        Args:
            params: Dict with 'coordinate' key containing [x, y] list

        Returns:
            Success message
        """
        if not PYAUTOGUI_AVAILABLE:
            return "Double click simulated (pyautogui not available)"

        coordinate = params.get("coordinate", [])
        if len(coordinate) != 2:
            raise ValueError(f"Invalid coordinate: {coordinate}")

        x, y = coordinate
        x_scaled, y_scaled = self._scale_coordinates(x, y)

        pyautogui.doubleClick(x_scaled, y_scaled)
        time.sleep(0.3)

        return f"Double clicked at ({x}, {y})"

    async def _click_drag(self, params: Dict[str, Any]) -> str:
        """
        Click and drag between two coordinates

        Args:
            params: Dict with:
                - coordinate: [x1, y1] start position
                - coordinate: [x2, y2] end position (in some implementations)

        Returns:
            Success message
        """
        if not PYAUTOGUI_AVAILABLE:
            return "Click drag simulated (pyautogui not available)"

        # This is a simplified implementation
        # Full implementation would need both start and end coordinates
        coordinate = params.get("coordinate", [])
        if len(coordinate) != 2:
            raise ValueError(f"Invalid coordinate: {coordinate}")

        x, y = coordinate
        x_scaled, y_scaled = self._scale_coordinates(x, y)

        # Simple drag (would need enhancement for full drag support)
        pyautogui.drag(x_scaled, y_scaled, duration=0.5)

        return f"Dragged to ({x}, {y})"

    def _scale_coordinates(self, x: int, y: int) -> tuple:
        """
        Scale coordinates from Claude's display size to actual screen size

        Args:
            x: X coordinate from Claude
            y: Y coordinate from Claude

        Returns:
            Tuple of (scaled_x, scaled_y)
        """
        if not PYAUTOGUI_AVAILABLE:
            return (x, y)

        # Get actual screen size
        screen_width, screen_height = pyautogui.size()

        # Calculate scale factors
        scale_x = screen_width / self.display_width
        scale_y = screen_height / self.display_height

        # Scale coordinates
        scaled_x = int(x * scale_x)
        scaled_y = int(y * scale_y)

        # Ensure coordinates are within bounds
        scaled_x = max(0, min(scaled_x, screen_width - 1))
        scaled_y = max(0, min(scaled_y, screen_height - 1))

        return (scaled_x, scaled_y)
