#!/usr/bin/env python3
"""
Authentication Session Manager for max-doc-AI

⚠️ DEPRECATED: This script is no longer needed with Computer Use API.
   Computer Use handles authentication automatically via visual login.
   This file is kept only for backward compatibility with legacy Playwright code.

This script opens your product's login page, lets you log in manually via SSO,
then saves your authenticated session cookies for automated screenshot capture.

Usage:
    python3 auth_manager.py
"""

from playwright.sync_api import sync_playwright
import json
import sys
from pathlib import Path

# Add scripts directory to path for config import
sys.path.insert(0, str(Path(__file__).parent))
import config as cfg


def save_auth_session(login_url=None, timeout_seconds=120):
    """
    Open browser, let user log in manually, save session cookies

    Args:
        login_url: URL to navigate to for login (default: from config.yaml)
        timeout_seconds: How long to wait for user to complete login (default: 120)
    """
    # Get config
    try:
        config = cfg.get_config()
        product_name = config['product']['name']
        if login_url is None:
            login_url = config['product']['url']
        auth_file = config['screenshots']['auth_session_file']
        viewport = {
            'width': config['screenshots']['viewport_width'],
            'height': config['screenshots']['viewport_height']
        }
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        print("   Please ensure config.yaml is set up correctly")
        return

    print(f"🔐 {product_name} Authentication Session Saver")
    print("=" * 80)
    print()
    print(f"This will open {product_name} in a browser window.")
    print("Please log in using your authentication method (SSO, username/password, etc.).")
    print("Once you're logged in and see the main dashboard/app, this script will")
    print("automatically save your session.")
    print()
    print("Opening browser in 2 seconds...")

    import time
    time.sleep(2)

    with sync_playwright() as p:
        # Launch visible browser
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport=viewport)
        page = context.new_page()

        # Navigate to login page
        print(f"\n🌐 Opening: {login_url}")
        page.goto(login_url)

        print()
        print("=" * 80)
        print("✋ Please log in manually now...")
        print("=" * 80)
        print()
        print("Steps:")
        print("  1. Complete your authentication flow")
        print(f"  2. Wait until you see the {product_name} dashboard/main app")
        print()
        print(f"⏰ You have {timeout_seconds} seconds to complete the login...")
        print("   The script will automatically save your session after that.")
        print()

        # Wait for user to log in manually
        countdown_interval = 10 if timeout_seconds >= 60 else 5
        for i in range(timeout_seconds, 0, -countdown_interval):
            print(f"   ⏳ {i} seconds remaining...")
            time.sleep(countdown_interval)

        # Wait a moment for any final redirects
        page.wait_for_timeout(2000)

        # Get current URL to verify login
        current_url = page.url
        print(f"\n📍 Current URL: {current_url}")

        # Check if login was successful (basic heuristic - user may need to adjust)
        logged_in = (
            current_url != login_url and
            not any(x in current_url.lower() for x in ['login', 'signin', 'auth', 'sso'])
        )

        if logged_in:
            print("   ✅ Looks like you're logged in!")

            # Save cookies and storage state
            cookies = context.cookies()
            storage_state = context.storage_state()

            # Ensure directory exists
            auth_path = Path(auth_file)
            auth_path.parent.mkdir(parents=True, exist_ok=True)

            # Save to file
            with open(auth_file, 'w') as f:
                json.dump(storage_state, f, indent=2)

            print(f"\n✅ Session saved to: {auth_file}")
            print(f"   Saved {len(cookies)} cookies")
            print()
            print("=" * 80)
            print("✅ AUTHENTICATION COMPLETE!")
            print("=" * 80)
            print()
            print("Your authenticated session has been saved.")
            print("The screenshot automation will now be able to access your application")
            print("without requiring manual login each time.")
            print()
            print("Note: Session cookies typically expire after a few hours or days.")
            print("If screenshots start failing, re-run this script to refresh the session.")
            print()

        else:
            print("   ⚠️  You don't appear to be logged in yet")
            print("   The session may not have been saved correctly")
            print()
            print("   Tips:")
            print("   - Make sure you completed the full authentication flow")
            print("   - Try running the script again with more time")
            print(f"   - Check if {login_url} is the correct login URL")

        browser.close()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Save authentication session for screenshot automation'
    )
    parser.add_argument(
        '--url',
        help='Login URL (default: from config.yaml)',
        default=None
    )
    parser.add_argument(
        '--timeout',
        help='Timeout in seconds (default: 120)',
        type=int,
        default=120
    )

    args = parser.parse_args()

    # Print deprecation warning
    print("\n" + "=" * 80)
    print("⚠️  DEPRECATION WARNING")
    print("=" * 80)
    print()
    print("This auth_manager.py script is DEPRECATED and no longer needed.")
    print()
    print("max-doc-AI now uses Claude's Computer Use API for screenshot capture,")
    print("which handles authentication automatically via visual login.")
    print()
    print("To configure authentication for Computer Use:")
    print("  1. Set SCREENSHOT_USER and SCREENSHOT_PASS in your .env file")
    print("  2. Configure auth settings in config.yaml under screenshots.auth")
    print("  3. Run your screenshot capture script - authentication is automatic!")
    print()
    print("See docs/computer-use-setup.md for details.")
    print()
    print("This script is kept only for legacy Playwright compatibility.")
    print("=" * 80)
    print()

    # Ask user if they want to continue
    response = input("Continue anyway? (y/N): ").strip().lower()
    if response != 'y':
        print("\n❌ Aborted. Please use Computer Use API instead.")
        sys.exit(0)

    print()

    save_auth_session(login_url=args.url, timeout_seconds=args.timeout)
