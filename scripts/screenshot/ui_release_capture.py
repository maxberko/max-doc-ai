#!/usr/bin/env python3
"""
Capture screenshots for Release UI Feature
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from screenshot.factory import create_capturer
import config as cfg

def capture_release_ui_screenshots():
    """Capture screenshots for the new Release UI feature"""

    # For local development, UI runs on localhost:3000
    base_url = "http://localhost:3000"

    screenshot_plan = [
        {
            'name': 'release-ui-home',
            'url': '/',
            'description': 'Home page with Create New Release card',
            'wait_time': 2000
        },
        {
            'name': 'release-ui-wizard-step1',
            'url': '/releases/new',
            'description': 'Release wizard - Step 1: Feature Description',
            'wait_time': 2000
        },
        {
            'name': 'release-ui-wizard-step2',
            'url': '/releases/new',
            'description': 'Release wizard - Step 2: Code Location (after clicking Next)',
            'wait_time': 1500,
            'interaction': 'fill_and_next'  # Fill step 1 and click Next
        },
        {
            'name': 'release-ui-wizard-step3',
            'url': '/releases/new',
            'description': 'Release wizard - Step 3: Release Date',
            'wait_time': 1500,
            'interaction': 'navigate_to_step3'  # Fill steps 1-2 and click Next twice
        },
        {
            'name': 'release-ui-wizard-step4',
            'url': '/releases/new',
            'description': 'Release wizard - Step 4: Review & Confirm',
            'wait_time': 1500,
            'interaction': 'navigate_to_step4'  # Fill all steps and reach review
        },
        {
            'name': 'release-ui-progress-active',
            'url': '/releases/[dynamic]',
            'description': 'Release execution in progress with chat and progress tracker',
            'wait_time': 3000,
            'interaction': 'start_release'  # Complete wizard and start execution
        }
    ]

    print(f"📸 Capturing {len(screenshot_plan)} screenshots for Release UI...")
    print(f"   Base URL: {base_url}")
    print(f"   Output: {cfg.get_screenshot_config()['output_dir']}")
    print()

    with create_capturer() as capturer:
        # Screenshot 1: Home page
        print("=" * 60)
        capturer.navigate(f"{base_url}/")
        capturer.wait(2000)
        capturer.capture('release-ui-home')
        print()

        # Screenshot 2: Wizard Step 1
        print("=" * 60)
        capturer.navigate(f"{base_url}/releases/new")
        capturer.wait(2000)
        capturer.capture('release-ui-wizard-step1')
        print()

        # Screenshot 3: Wizard Step 2 (need to interact)
        print("=" * 60)
        print("🔄 Filling Step 1 and navigating to Step 2...")
        # Fill the textarea
        capturer.click('textarea[placeholder*="describe"]')
        capturer.wait(500)

        # Type feature description using Computer Use
        prompt = """Type the following text into the focused textarea:
"New UI for generating releases without using the terminal. Includes a wizard, progress tracker, and chat interface."

Then click the "Next" button to proceed to step 2.

Wait for step 2 to appear before taking a screenshot.
"""
        import asyncio
        asyncio.run(capturer.client.execute_task(
            task_prompt=prompt,
            max_iterations=10,
            verbose=False
        ))

        capturer.wait(1000)
        capturer.capture('release-ui-wizard-step2')
        print()

        # Screenshot 4: Wizard Step 3
        print("=" * 60)
        print("🔄 Filling Step 2 and navigating to Step 3...")
        # Select "Current codebase" option and click Next
        prompt = """Click on the "Current codebase" option/button.
Then click the "Next" button to proceed to step 3.

Wait for step 3 (Release Date) to appear before taking a screenshot.
"""
        asyncio.run(capturer.client.execute_task(
            task_prompt=prompt,
            max_iterations=10,
            verbose=False
        ))

        capturer.wait(1000)
        capturer.capture('release-ui-wizard-step3')
        print()

        # Screenshot 5: Wizard Step 4 (Review)
        print("=" * 60)
        print("🔄 Selecting date and navigating to Step 4...")
        # Select "Today" and click Next
        prompt = """Click on the "Today" option/button for the release date.
Then click the "Next" button to proceed to step 4 (Review).

Wait for step 4 (Review & Confirm) to appear before taking a screenshot.
"""
        asyncio.run(capturer.client.execute_task(
            task_prompt=prompt,
            max_iterations=10,
            verbose=False
        ))

        capturer.wait(1000)
        capturer.capture('release-ui-wizard-step4')
        print()

        # Screenshot 6: Execution in progress
        print("=" * 60)
        print("🔄 Starting release execution...")
        # Click "Start Release" button
        prompt = """Click the "Start Release" or "Create Release" button to begin execution.

This will navigate to a new page showing:
- A chat interface on the left
- A progress tracker on the right

Wait for the execution page to load and show active progress before taking a screenshot.
This may take 5-10 seconds.
"""
        asyncio.run(capturer.client.execute_task(
            task_prompt=prompt,
            max_iterations=15,
            verbose=False
        ))

        capturer.wait(3000)  # Wait for execution to show progress
        capturer.capture('release-ui-progress-active')
        print()

    print("=" * 60)
    print("✅ All screenshots captured successfully!")
    print()
    print("📁 Screenshots saved to:")
    print(f"   {cfg.get_screenshot_config()['output_dir']}")
    print()
    print("🔍 Review the screenshots:")
    print(f"   open {cfg.get_screenshot_config()['output_dir']}")

if __name__ == '__main__':
    capture_release_ui_screenshots()
