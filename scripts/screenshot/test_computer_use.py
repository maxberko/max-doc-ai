#!/usr/bin/env python3
"""
Computer Use Test Suite

Comprehensive test script to verify Computer Use implementation is working correctly.
This tests all components: dependencies, configuration, API connectivity, and screenshot capture.
"""

import sys
import os
from pathlib import Path
import asyncio

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Test results tracking
test_results = []


def test(name):
    """Decorator to track test results"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                test_results.append((name, True, None))
                print(f"✅ {name}")
                return result
            except Exception as e:
                test_results.append((name, False, str(e)))
                print(f"❌ {name}")
                print(f"   Error: {e}")
                return None
        return wrapper
    return decorator


def print_header(title):
    """Print section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


@test("Dependencies installed")
def test_dependencies():
    """Test that all required dependencies are installed"""
    required_modules = [
        'anthropic',
        'PIL',  # Pillow
        'pyautogui',
        'pyotp',
        'aiohttp'
    ]

    missing = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)

    if missing:
        raise RuntimeError(f"Missing modules: {', '.join(missing)}")

    return True


@test("Configuration loaded")
def test_configuration():
    """Test that configuration loads correctly"""
    import config as cfg

    # Test basic config loading
    config = cfg.get_config()

    # Test screenshot config
    screenshot_config = cfg.get_screenshot_config()

    # Check implementation is set
    impl = screenshot_config.get('implementation')
    if impl not in ['computer_use', 'playwright']:
        raise ValueError(f"Invalid implementation: {impl}")

    # If Computer Use, check for computer_use config
    if impl == 'computer_use':
        cu_config = cfg.get_computer_use_config()
        if not cu_config:
            raise ValueError("Computer Use implementation selected but no config found")

    print(f"   Implementation: {impl}")
    return True


@test("Anthropic API key configured")
def test_api_key():
    """Test that Anthropic API key is set and accessible"""
    import config as cfg
    from dotenv import load_dotenv

    load_dotenv()

    api_key = cfg.get_anthropic_api_key()

    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set in .env or config.yaml")

    if not api_key.startswith('sk-ant-'):
        raise ValueError(f"Invalid API key format: {api_key[:10]}...")

    print(f"   API key: {api_key[:15]}...")
    return True


@test("Anthropic API connectivity")
def test_api_connectivity():
    """Test that we can connect to Anthropic API"""
    import anthropic
    import config as cfg

    api_key = cfg.get_anthropic_api_key()
    client = anthropic.Anthropic(api_key=api_key)

    # Make a simple API call
    response = client.messages.create(
        model='claude-sonnet-4-5',
        max_tokens=10,
        messages=[{'role': 'user', 'content': 'Hi'}]
    )

    print(f"   Model: {response.model}")
    print(f"   Response: {response.content[0].text[:30]}...")
    return True


@test("Desktop automation available")
def test_desktop_automation():
    """Test that desktop automation (pyautogui) works"""
    import pyautogui

    # Test getting screen size
    width, height = pyautogui.size()
    print(f"   Screen size: {width}x{height}")

    # Test getting mouse position (doesn't move mouse)
    x, y = pyautogui.position()
    print(f"   Mouse position: ({x}, {y})")

    return True


@test("Screenshot capture tool")
def test_screenshot_tool():
    """Test basic screenshot capture tool"""
    from screenshot.computer_use_tools import ComputerUseTool

    async def capture_test():
        tool = ComputerUseTool(display_width=1280, display_height=800)

        # Capture a screenshot
        screenshot = await tool._screenshot({})

        # Verify it's a base64 string
        if not isinstance(screenshot, str):
            raise TypeError(f"Expected string, got {type(screenshot)}")

        if not screenshot.startswith('data:image/png;base64,'):
            raise ValueError("Screenshot doesn't have correct data URI format")

        # Check length (should be substantial)
        if len(screenshot) < 1000:
            raise ValueError(f"Screenshot too small: {len(screenshot)} chars")

        print(f"   Screenshot size: {len(screenshot)} chars")
        return screenshot

    screenshot = asyncio.run(capture_test())
    return screenshot


@test("Computer Use client initialization")
def test_client_init():
    """Test Computer Use client initializes correctly"""
    import config as cfg
    from screenshot.computer_use_client import ComputerUseClient

    api_key = cfg.get_anthropic_api_key()

    client = ComputerUseClient(
        api_key=api_key,
        model='claude-sonnet-4-5',
        display_width=1280,
        display_height=800
    )

    print(f"   Model: {client.model}")
    print(f"   Display: {client.display_width}x{client.display_height}")

    return client


@test("Factory pattern works")
def test_factory():
    """Test that factory pattern can create Computer Use capturer"""
    from screenshot.factory import create_capturer

    # Try to create Computer Use capturer
    try:
        capturer = create_capturer(implementation="computer_use")
        print(f"   Capturer type: {type(capturer).__name__}")
        return capturer
    except Exception as e:
        raise RuntimeError(f"Failed to create Computer Use capturer: {e}")


@test("Configuration credentials present")
def test_credentials():
    """Test that authentication credentials are configured"""
    import config as cfg
    from dotenv import load_dotenv

    load_dotenv()

    screenshot_config = cfg.get_screenshot_config()

    # Only test if Computer Use is configured
    if screenshot_config.get('implementation') != 'computer_use':
        print("   Skipped (not using Computer Use)")
        return True

    cu_config = cfg.get_computer_use_config()
    auth_config = cu_config.get('auth', {})

    if not auth_config.get('enabled'):
        print("   Authentication disabled in config")
        return True

    # Check for username and password in environment
    username = os.getenv('SCREENSHOT_USER')
    password = os.getenv('SCREENSHOT_PASS')

    if not username:
        raise ValueError("SCREENSHOT_USER not set in .env")

    if not password:
        raise ValueError("SCREENSHOT_PASS not set in .env")

    print(f"   Username: {username}")
    print(f"   Password: {'*' * len(password)}")

    return True


def test_simple_screenshot_capture():
    """Optional: Test full screenshot capture (slow)"""
    print("\n⏳ Optional: Full screenshot capture test")
    print("   This will take 5-10 seconds and move your mouse...")

    response = input("   Run full test? (y/N): ").strip().lower()

    if response != 'y':
        print("   Skipped")
        return None

    print("\n   Starting capture test...")

    from screenshot.factory import create_capturer
    import tempfile

    try:
        # Create temporary output directory
        with tempfile.TemporaryDirectory() as tmpdir:
            with create_capturer(
                implementation="computer_use",
                output_dir=tmpdir
            ) as capturer:
                # Simple test: just take a screenshot of current screen
                output_path = capturer.capture(
                    filename="test-screenshot",
                    full_page=False
                )

                # Verify file was created
                if not os.path.exists(output_path):
                    raise RuntimeError(f"Screenshot not saved: {output_path}")

                # Check file size
                size = os.path.getsize(output_path)
                if size < 1000:
                    raise RuntimeError(f"Screenshot too small: {size} bytes")

                print(f"   ✅ Screenshot saved: {size} bytes")
                print(f"   Path: {output_path}")

                return True

    except Exception as e:
        print(f"   ❌ Capture test failed: {e}")
        return False


def print_summary():
    """Print test summary"""
    print_header("Test Summary")

    passed = sum(1 for _, success, _ in test_results if success)
    failed = sum(1 for _, success, _ in test_results if not success)
    total = len(test_results)

    print(f"Total tests: {total}")
    print(f"Passed: {passed} ✅")
    print(f"Failed: {failed} {'❌' if failed > 0 else ''}\n")

    if failed > 0:
        print("Failed tests:")
        for name, success, error in test_results:
            if not success:
                print(f"  ❌ {name}")
                print(f"     {error}\n")

    return failed == 0


def print_next_steps(all_passed):
    """Print next steps based on test results"""
    print_header("Next Steps")

    if all_passed:
        print("✅ All tests passed! Computer Use is ready to use.\n")
        print("Try capturing screenshots:")
        print("  python3 scripts/screenshot/demo_capture.py\n")
        print("Or run a release workflow:")
        print("  @claude Create a release for the [Feature Name] feature\n")
    else:
        print("❌ Some tests failed. Fix the issues above, then run this test again.\n")
        print("Common fixes:")
        print("  • Install missing dependencies: pip install -r requirements.txt")
        print("  • Set up .env file: cp .env.example .env")
        print("  • Configure config.yaml: cp config.example.yaml config.yaml")
        print("  • Grant accessibility permissions (macOS)\n")
        print("See the setup guide for help:")
        print("  docs/computer-use-setup.md\n")


def main():
    """Run all tests"""
    print("🧪 Computer Use Test Suite")
    print("=" * 60)

    # Test 1: Dependencies
    print_header("Testing Dependencies")
    test_dependencies()

    # Test 2: Configuration
    print_header("Testing Configuration")
    test_configuration()
    test_api_key()
    test_credentials()

    # Test 3: API Connectivity
    print_header("Testing API Connectivity")
    test_api_connectivity()

    # Test 4: Desktop Automation
    print_header("Testing Desktop Automation")
    test_desktop_automation()
    test_screenshot_tool()

    # Test 5: Computer Use Components
    print_header("Testing Computer Use Components")
    test_client_init()
    test_factory()

    # Print summary
    all_passed = print_summary()

    # Optional: Full screenshot capture test
    # test_simple_screenshot_capture()

    # Next steps
    print_next_steps(all_passed)

    # Exit code
    sys.exit(0 if all_passed else 1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
