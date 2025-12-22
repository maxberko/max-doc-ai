#!/usr/bin/env python3
"""
Demo screenshot capture for FlowState product

This is an example script showing how to use the screenshot capture framework
for your product. Customize this for your own application.

NOTE: This script assumes you have a running FlowState demo application.
If you don't have one, you'll need to mock screenshots or use placeholders.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
import config as cfg
from screenshot.factory import create_capturer, create_capturer_from_plan


def capture_flowstate_screenshots(base_url: str = None):
    """
    Capture screenshots for FlowState demo product

    Args:
        base_url: Base URL for FlowState app (default: from config)
    """
    if base_url is None:
        try:
            base_url = cfg.get_product_url()
        except:
            base_url = 'https://app.flowstate.example.com'

    print("=" * 60)
    print("📸 FlowState Screenshot Capture")
    print("=" * 60)
    print(f"\nBase URL: {base_url}")
    print()

    # Define screenshot plan
    # Each item specifies what to capture and how
    screenshot_plan = [
        # Dashboard screenshots
        {
            'name': 'dashboards-overview',
            'url': '/dashboards',
            'wait_for': '.dashboard-grid',
            'wait_time': 2000,
            'full_page': False
        },
        {
            'name': 'dashboards-metrics',
            'url': '/dashboards',
            'selector': '.metrics-panel',
            'wait_for': '.metrics-panel',
            'wait_time': 1000
        },
        {
            'name': 'dashboards-customization',
            'url': '/dashboards/customize',
            'wait_for': '.customize-panel',
            'wait_time': 1500
        },

        # Automation/Workflow screenshots
        {
            'name': 'automation-builder',
            'url': '/workflows/new',
            'wait_for': '.workflow-canvas',
            'wait_time': 2000
        },
        {
            'name': 'automation-triggers',
            'url': '/workflows/new',
            'selector': '.triggers-panel',
            'wait_for': '.triggers-panel',
            'wait_time': 1000
        },
        {
            'name': 'automation-actions',
            'url': '/workflows/new',
            'selector': '.actions-panel',
            'wait_for': '.actions-panel',
            'wait_time': 1000
        },

        # Integrations screenshots
        {
            'name': 'integrations-marketplace',
            'url': '/integrations',
            'wait_for': '.integrations-grid',
            'wait_time': 2000,
            'full_page': True
        },
        {
            'name': 'integrations-connected',
            'url': '/integrations/connected',
            'wait_for': '.connected-integrations',
            'wait_time': 1000
        },
        {
            'name': 'integrations-configuration',
            'url': '/integrations/slack/config',
            'wait_for': '.config-form',
            'wait_time': 1500
        }
    ]

    print(f"📋 Screenshot plan: {len(screenshot_plan)} screenshots")
    print()

    # Capture screenshots based on plan
    # Uses implementation from config (Computer Use or Playwright)
    try:
        create_capturer_from_plan(screenshot_plan, base_url)

        print("\n" + "=" * 60)
        print("✅ FlowState screenshots captured successfully!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("  1. Review screenshots in: demo/docs/product_documentation/screenshots/")
        print("  2. Upload to Pylon CDN:")
        print("     python3 scripts/pylon/upload.py --image <screenshot.png>")
        print("  3. Update documentation with Pylon URLs")
        print("  4. Sync documentation:")
        print("     python3 scripts/pylon/sync.py --file <doc.md> --key <key> --title <title> --slug <slug> --collection <collection>")
        print()

    except Exception as e:
        print(f"\n❌ Error capturing screenshots: {e}")
        print("\nTroubleshooting:")
        print("  • Is the FlowState app running at the correct URL?")
        print("  • Have you saved an authentication session?")
        print("    Run: python3 scripts/auth_manager.py")
        print("  • Do the CSS selectors match your app's structure?")
        print("    Update the screenshot_plan in this script if needed")
        sys.exit(1)


def capture_custom_workflow():
    """
    Example: Capture screenshots using custom workflow

    This shows how to write a custom capture workflow for more complex scenarios.
    """
    print("\n" + "=" * 60)
    print("📸 Custom Workflow Example")
    print("=" * 60 + "\n")

    # Use factory to create capturer (reads implementation from config)
    with create_capturer() as capturer:
        # 1. Navigate to dashboard
        capturer.navigate('https://app.flowstate.example.com/dashboards')
        capturer.wait_for_selector('.dashboard-grid')
        capturer.wait(2000)

        # 2. Capture overview
        capturer.capture('custom-dashboard-overview')

        # 3. Click on a specific dashboard
        capturer.click('.dashboard-card:first-child')
        capturer.wait(1500)

        # 4. Capture detailed view
        capturer.capture('custom-dashboard-detail')

        # 5. Interact with a specific element
        capturer.scroll_to('.metrics-section')
        capturer.wait(500)

        # 6. Capture after interaction
        capturer.capture('custom-dashboard-metrics', selector='.metrics-section')

        print("\n✅ Custom workflow completed")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Capture screenshots for FlowState demo'
    )
    parser.add_argument(
        '--url',
        help='Base URL for FlowState app (default: from config)',
        default=None
    )
    parser.add_argument(
        '--custom-workflow',
        action='store_true',
        help='Run custom workflow example instead'
    )

    args = parser.parse_args()

    if args.custom_workflow:
        capture_custom_workflow()
    else:
        capture_flowstate_screenshots(base_url=args.url)
