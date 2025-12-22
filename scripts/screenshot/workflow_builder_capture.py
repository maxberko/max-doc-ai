#!/usr/bin/env python3
"""
Capture screenshots for Workflow Builder feature
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from screenshot.factory import create_capturer_from_plan
import config as cfg

def capture_workflow_builder_screenshots():
    """Capture screenshots for the Workflow Builder feature"""
    base_url = cfg.get_product_url()

    screenshot_plan = [
        {
            'name': 'workflow-builder-overview',
            'url': '/workflows',
            'wait_for': '.workflow-list',
            'wait_time': 2000,
            'description': 'Main workflows list page'
        },
        {
            'name': 'workflow-builder-canvas',
            'url': '/workflows/new',
            'wait_for': '.workflow-canvas',
            'wait_time': 2500,
            'description': 'Workflow canvas editor interface'
        },
        {
            'name': 'workflow-builder-triggers',
            'url': '/workflows/new',
            'wait_for': '.triggers-panel',
            'selector': '.triggers-panel',
            'wait_time': 2000,
            'description': 'Available triggers panel'
        },
        {
            'name': 'workflow-builder-actions',
            'url': '/workflows/new',
            'wait_for': '.actions-panel',
            'selector': '.actions-panel',
            'wait_time': 2000,
            'description': 'Available actions panel'
        },
        {
            'name': 'workflow-builder-test',
            'url': '/workflows/new',
            'wait_for': '.test-workflow-button',
            'wait_time': 2000,
            'description': 'Test workflow interface'
        }
    ]

    print(f"📸 Capturing {len(screenshot_plan)} screenshots for Workflow Builder...")
    create_capturer_from_plan(screenshot_plan, base_url)
    print("✅ Screenshots captured successfully!")

if __name__ == '__main__':
    capture_workflow_builder_screenshots()
