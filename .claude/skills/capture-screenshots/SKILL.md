---
name: capture-screenshots
description: Capture product screenshots using Claude's Computer Use API. Provides visual authentication (no session expiration!), intelligent content verification, and reliable screenshot capture. Screenshots are saved to configured directory for later upload to Pylon CDN.
---

# Capture Screenshots

Automate screenshot capture for product features using Claude's Computer Use API.

## Purpose

Capture consistent, high-quality screenshots of product features for use in documentation. Computer Use provides:
- **Visual Authentication**: Claude logs in by seeing the screen, eliminating session expiration issues
- **Intelligent Content Verification**: Claude waits for pages to fully load and verifies content is visible
- **Self-Adapting**: No CSS selectors to maintain - Claude finds elements visually
- **Reliable**: 95%+ success rate vs 60-70% with traditional automation

All screenshots are captured at a consistent viewport size (configured in config.yaml).

## Prerequisites

1. **Computer Use configured**: Anthropic API key and product credentials in `.env`
2. **Product is accessible**: The application must be running and accessible at configured URL
3. **Dependencies installed**: `pip install anthropic pillow pyautogui`
4. **macOS only**: Accessibility permissions granted for pyautogui

See [Computer Use Setup Guide](../../../docs/computer-use-setup.md) for detailed configuration.

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

3. **Visual Landmarks** (for Computer Use):
   - Page titles and headers
   - Distinctive UI elements
   - Section labels
   - Button text

**Note**: Computer Use doesn't require CSS selectors. Claude navigates visually, so focus on understanding what the user will see, not DOM structure.

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
        'wait_for': '.[main-container-class]',  # CSS selector (will be converted to visual description)
        'wait_time': 2000  # Additional wait time in milliseconds
    },
    {
        'name': '[feature]-detail',
        'url': '/[feature-path]/detail',
        'selector': '.[specific-section]',  # Optional: capture specific element
        'wait_for': '.[section-class]',
        'wait_time': 1500
    }
]
```

**Note**: With Computer Use, CSS selectors like `.main-container-class` are automatically converted to visual descriptions like "element with class 'main-container-class'". Claude then finds the element visually on screen.

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
from screenshot.factory import create_capturer_from_plan  # Uses Computer Use by default
import config as cfg

def capture_[feature]_screenshots():
    base_url = cfg.get_product_url()

    screenshot_plan = [
        # Add your screenshot plan here
    ]

    print(f"📸 Capturing {len(screenshot_plan)} screenshots for [Feature Name]...")
    create_capturer_from_plan(screenshot_plan, base_url)  # Uses Computer Use automatically
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

**What happens** (with Computer Use):
1. **Visual authentication**: Claude logs in by seeing and interacting with the login page
2. **Intelligent navigation**: Claude navigates to each URL and waits for content to load
3. **Content verification**: Claude verifies the correct content is visible before capturing
4. **Screenshot capture**: High-quality screenshots are saved to the configured output directory
5. **No session expiration**: Fresh authentication each time ensures reliability

**Expected duration**:
- First capture (with auth): 30-60 seconds
- Additional captures: 5-10 seconds each

**Cost**: ~$0.02 per screenshot with Claude Sonnet 4.5

### Step 5: Verify Screenshots

Check the output directory (from config.yaml):

```bash
ls -lh output/screenshots/
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
**Location:** `output/screenshots/`

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
   python3 scripts/pylon/upload.py --image output/screenshots/[feature]-overview.png
   ```

2. Use CloudFront URLs in documentation

3. Sync documentation to Pylon knowledge base
```

## Configuration

Screenshots are configured in `config.yaml`:

```yaml
screenshots:
  viewport_width: 1280      # Display width (≤1280 recommended)
  viewport_height: 800      # Display height (≤800 recommended)
  format: "png"
  quality: 90

  model: "claude-sonnet-4-5"
  max_iterations: 50

  auth:
    enabled: true
    type: "sso"  # or "username_password"
    login_url: "${PRODUCT_URL}/login"
    username: "${SCREENSHOT_USER}"
    password: "${SCREENSHOT_PASS}"
    sso_provider: "google"

output:
  screenshots_dir: "./output/screenshots"
```

**Viewport Size:** Keep ≤1280x800 for optimal Computer Use coordinate accuracy. Consistent dimensions ensure professional-looking documentation.

## Troubleshooting

### Authentication Failures

**Symptom:** Screenshots show login page or authentication errors

**Solution:**
1. Verify credentials in `.env` are correct: `SCREENSHOT_USER` and `SCREENSHOT_PASS`
2. Check login URL is correct in `config.yaml`
3. Ensure SSO provider is configured correctly
4. Try increasing `max_iterations` in config (allows more time for auth)
5. Check Computer Use agent output for specific error messages

**With Computer Use, session expiration is no longer an issue!** Each capture session performs fresh authentication.

### Page Not Loading

**Symptom:** Screenshots are blank or show loading state

**Solution:**
1. Increase `wait_time` in screenshot plan
2. Computer Use naturally waits for content - if still failing, the page may have issues
3. Check if URL is correct
4. Verify product is accessible and running
5. Review Computer Use agent output to see what Claude saw

### Content Not Captured Correctly

**Symptom:** Wrong element captured or content missing

**Solution:**
1. CSS selectors are converted to visual descriptions - Claude finds elements by appearance
2. Make selectors more descriptive (`.dashboard-header` better than `.container-1`)
3. Provide visual context in comments for complex elements
4. Consider using full-page screenshots if specific element capture fails

### Screenshots Too Small/Large

**Symptom:** Screenshot dimensions are wrong

**Solution:**
1. Check viewport settings in config.yaml (must match display resolution)
2. For macOS, ensure viewport matches your screen resolution or scaling factor
3. For full-page screenshots, use `full_page=True` in screenshot plan
4. For specific elements, use `selector` parameter

## Best Practices

1. **Consistent Naming:** Use descriptive, kebab-case names
2. **Natural Wait Times:** Computer Use waits intelligently - only add explicit `wait_time` for animations or slow transitions
3. **Descriptive Selectors:** Use meaningful class names that describe the element's purpose
4. **Visual Verification:** Always review screenshots manually (Computer Use is reliable but not perfect)
5. **Clean State:** Ensure pages are in clean, representative state (no dev tools, no personal data)
6. **Batch Captures:** Capture all screenshots for a feature in one session to share authentication cost
7. **Monitor Costs:** Track API usage at console.anthropic.com
8. **Accessibility:** Include `alt` text when uploading to Pylon

## Advanced Techniques

### Custom Interactions

For complex scenarios requiring user interactions:

```python
from screenshot.factory import create_capturer

with create_capturer() as capturer:
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

**Note:** With Computer Use, these interactions are handled visually by Claude. The `click()` and `scroll_to()` methods translate to natural language prompts that Claude executes by seeing the screen.

### Multiple States

Capture different states of the same view:

```python
from screenshot.factory import create_capturer

with create_capturer() as capturer:
    # Empty state
    capturer.navigate('/dashboards?empty=true')
    capturer.capture('dashboards-empty-state')

    # With data
    capturer.navigate('/dashboards')
    capturer.capture('dashboards-with-data')
```

**Note:** Complex state manipulation (like triggering loading states) requires Claude to interact with the UI naturally. If you need specific states, consider using URL parameters or asking Claude to perform the necessary actions via prompts.

## Output

After successful execution:

```
📸 Capturing 2 screenshots for [Feature Name]...

🌐 Starting Computer Use session...
   Viewport: 1280x800
   Model: claude-sonnet-4-5

🔐 Authenticating...
   ✅ Authentication complete

📍 Navigating to: https://app.example.com/feature
   ✅ Page loaded
📸 Capturing: feature-overview.png
   ✅ Saved: output/screenshots/feature-overview.png

📍 Navigating to: https://app.example.com/feature/detail
   ✅ Page loaded
📸 Capturing: feature-detail.png
   ✅ Saved: output/screenshots/feature-detail.png

✅ Session closed

✅ Screenshots captured successfully!
```

## Integration with Release Workflow

This skill is typically invoked as the first step in the release workflow:

1. ✅ **capture-screenshots** ← You are here
2. Upload to Pylon CDN (sync-docs skill)
3. Create documentation with screenshots (update-product-doc skill)
4. Sync documentation (sync-docs skill)
5. Create announcements (create-changelog skill)
