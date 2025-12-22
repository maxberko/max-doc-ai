---
name: capture-screenshots
description: Capture product screenshots using Playwright automation. Authenticates using saved session, navigates to specified URLs, and captures screenshots at consistent viewport size. Screenshots are saved to configured directory for later upload to Pylon CDN.
---

# Capture Screenshots

Automate screenshot capture for product features using Playwright browser automation.

## Purpose

Capture consistent, high-quality screenshots of product features for use in documentation. All screenshots are captured at the same viewport size (configured in config.yaml) to ensure visual consistency across documentation.

## Prerequisites

1. **Authentication session saved**: Run `python3 scripts/auth_manager.py` first to save login session
2. **Product is accessible**: The application must be running and accessible at configured URL
3. **Playwright installed**: `pip install playwright && playwright install chromium`

## Input

The user will provide:

1. **Feature name**: e.g., "Dashboards", "Workflow Automation", "Integration Hub"
2. **Category**: Which documentation category (features, integrations, getting-started)
3. **URLs/pages to capture**: Specific pages or views to screenshot
4. **Optional context**: Specific elements to capture, interactions needed

## Process

### Step 1: Research Feature UI

Use the Task tool to explore the codebase and understand:

1. **Routes and URLs**: Where is this feature accessed?
   - Look for route definitions, page components
   - Check navigation menus and links
   - Find the base URL path

2. **UI Structure**: What does the interface look like?
   - Main views and layouts
   - Key components and sections
   - Interactive elements (buttons, forms, modals)

3. **CSS Selectors**: What selectors can we use?
   - Component class names
   - Container IDs
   - Semantic HTML elements

**Example exploration:**
```
Task: Explore
Find all routes and components for the [feature name] feature.
Look for page components, route definitions, and main UI views.
```

### Step 2: Plan Screenshot Capture

Based on your research, create a screenshot plan:

```python
screenshot_plan = [
    {
        'name': '[feature]-overview',
        'url': '/[feature-path]',
        'wait_for': '.[main-container-class]',
        'wait_time': 2000
    },
    {
        'name': '[feature]-detail',
        'url': '/[feature-path]/detail',
        'selector': '.[specific-section]',
        'wait_for': '.[section-class]',
        'wait_time': 1500
    }
]
```

**Naming convention:**
- Use kebab-case: `feature-name-view.png`
- Be descriptive: `dashboards-overview.png`, `dashboards-metrics-panel.png`
- Keep it consistent: `[feature]-[view].png`

### Step 3: Create Capture Script

Create a Python script in `scripts/screenshot/` for this feature:

```python
#!/usr/bin/env python3
"""
Capture screenshots for [Feature Name]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from screenshot.capture import capture_screenshots_from_plan
import config as cfg

def capture_[feature]_screenshots():
    base_url = cfg.get_product_url()

    screenshot_plan = [
        # Add your screenshot plan here
    ]

    print(f"📸 Capturing {len(screenshot_plan)} screenshots for [Feature Name]...")
    capture_screenshots_from_plan(screenshot_plan, base_url)
    print("✅ Screenshots captured successfully!")

if __name__ == '__main__':
    capture_[feature]_screenshots()
```

### Step 4: Execute Screenshot Capture

Run the capture script:

```bash
cd /path/to/max-doc-ai
python3 scripts/screenshot/[feature]_capture.py
```

The script will:
1. Load authentication session
2. Open browser (headless by default)
3. Navigate to each URL
4. Wait for page to load
5. Capture screenshot
6. Save to configured output directory

### Step 5: Verify Screenshots

Check the output directory (from config.yaml):

```bash
ls -lh demo/docs/product_documentation/screenshots/
```

**Verify:**
- ✅ All expected screenshots are present
- ✅ File sizes are reasonable (not too small = failed capture)
- ✅ Filenames follow naming convention
- ✅ Screenshots show the correct content (open and review visually)

### Step 6: Document Screenshot Metadata

Create a summary of captured screenshots:

```markdown
## Screenshots Captured for [Feature Name]

**Total:** [X] screenshots
**Location:** `demo/docs/product_documentation/screenshots/`

### Screenshot List:

1. **[feature]-overview.png**
   - Description: Main overview of [feature]
   - Size: [width]x[height]
   - Shows: [what is visible]

2. **[feature]-detail.png**
   - Description: Detailed view of [specific section]
   - Size: [width]x[height]
   - Shows: [what is visible]

[... continue for all screenshots ...]

### Next Steps:

1. Upload screenshots to Pylon CDN:
   ```bash
   python3 scripts/pylon/upload.py --image demo/docs/product_documentation/screenshots/[feature]-overview.png
   ```

2. Use CloudFront URLs in documentation

3. Sync documentation to Pylon knowledge base
```

## Configuration

Screenshots are configured in `config.yaml`:

```yaml
screenshots:
  viewport_width: 1470      # Browser width
  viewport_height: 840      # Browser height
  output_dir: "./demo/docs/product_documentation/screenshots"
  auth_session_file: "./scripts/auth_session.json"
  format: "png"
  quality: 90
```

**Viewport Size:** Using a consistent viewport ensures all screenshots have the same dimensions, which looks more professional in documentation.

## Troubleshooting

### Authentication Failures

**Symptom:** Screenshots show login page instead of actual feature

**Solution:**
1. Run `python3 scripts/auth_manager.py` to save a fresh session
2. Verify the auth session file exists
3. Check if session cookies have expired (typically 2-4 hours)

### Page Not Loading

**Symptom:** Screenshots are blank or show loading state

**Solution:**
1. Increase `wait_time` in screenshot plan
2. Use more specific `wait_for` selector
3. Check if URL is correct
4. Try running in non-headless mode to see what's happening:
   ```python
   with ScreenshotCapturer(headless=False) as capturer:
       # ... your code
   ```

### Element Not Found

**Symptom:** Error about selector not found

**Solution:**
1. Inspect the page to verify correct CSS selector
2. Element might be dynamically loaded - increase wait time
3. Element might be in iframe - need different approach
4. Try using a more general selector

### Screenshots Too Small/Large

**Symptom:** Screenshot dimensions are wrong

**Solution:**
1. Check viewport settings in config.yaml
2. For full-page screenshots, use `full_page=True`
3. For specific elements, use `selector` parameter

## Best Practices

1. **Consistent Naming:** Use descriptive, kebab-case names
2. **Appropriate Wait Times:** Give pages time to fully render (1500-2000ms typical)
3. **Specific Selectors:** Use `wait_for` to ensure content is loaded
4. **Visual Verification:** Always review screenshots manually
5. **Clean State:** Ensure pages are in clean, representative state (no dev tools, no personal data)
6. **Accessibility:** Include `alt` text when uploading to Pylon

## Advanced Techniques

### Custom Interactions

For complex scenarios requiring user interactions:

```python
with ScreenshotCapturer(headless=False) as capturer:
    capturer.navigate('https://app.example.com/feature')

    # Click to open modal
    capturer.click('.open-modal-button')
    capturer.wait(1000)

    # Capture modal
    capturer.capture('feature-modal', selector='.modal-container')

    # Scroll to specific section
    capturer.scroll_to('.metrics-section')
    capturer.wait(500)

    # Capture after scroll
    capturer.capture('feature-metrics')
```

### Multiple States

Capture different states of the same view:

```python
# Empty state
capturer.navigate('/dashboards?empty=true')
capturer.capture('dashboards-empty-state')

# With data
capturer.navigate('/dashboards')
capturer.capture('dashboards-with-data')

# Loading state (tricky - need to be fast)
capturer.page.evaluate('window.showLoadingState()')
capturer.capture('dashboards-loading')
```

## Output

After successful execution:

```
📸 Capturing screenshots for [Feature Name]...

🌐 Starting browser...
   Viewport: 1470x840
   Headless: True
   Loading auth session: ./scripts/auth_session.json
   ✅ Browser ready

📍 Navigating to: https://app.example.com/feature
   ✅ Page loaded
📸 Capturing: feature-overview.png
   ✅ Saved: demo/docs/product_documentation/screenshots/feature-overview.png

📍 Navigating to: https://app.example.com/feature/detail
   ✅ Page loaded
📸 Capturing: feature-detail.png
   ✅ Saved: demo/docs/product_documentation/screenshots/feature-detail.png

✅ Browser closed

✅ Captured 2 screenshots for [Feature Name]
```

## Integration with Release Workflow

This skill is typically invoked as the first step in the release workflow:

1. ✅ **capture-screenshots** ← You are here
2. Upload to Pylon CDN (sync-docs skill)
3. Create documentation with screenshots (update-product-doc skill)
4. Sync documentation (sync-docs skill)
5. Create announcements (create-changelog skill)
