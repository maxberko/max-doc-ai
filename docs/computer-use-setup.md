# Computer Use Setup Guide

This guide walks you through setting up Claude's Computer Use API for screenshot capture in max-doc-AI.

## Why Computer Use?

Computer Use solves the main problems with Playwright:
- ✅ **No more authentication failures**: Visual login eliminates session expiration
- ✅ **Reliable content capture**: Claude waits naturally for pages to load
- ✅ **Self-adapting**: No CSS selectors to maintain
- ✅ **Better handling of dynamic content**: Claude verifies content is visible

## Prerequisites

### 1. Claude Account and API Key

You need an Anthropic API key to use Computer Use.

**Get Your API Key**:
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign in or create an account
3. Navigate to **API Keys** in the left sidebar
4. Click **Create Key**
5. Name it (e.g., "max-doc-ai-screenshots")
6. Copy the key immediately (starts with `sk-ant-`)

**Important**: Keep your API key secure. Never commit it to version control.

### 2. Python 3.8+

Check your Python version:
```bash
python3 --version
```

### 3. Product Credentials

You'll need login credentials for your product to enable visual authentication:
- Username or email
- Password
- (Optional) TOTP secret for 2FA

## Installation

### Step 1: Install Python Dependencies

Install the required packages:

```bash
# Install all dependencies from requirements.txt
pip install -r requirements.txt

# Or install individually:
pip install anthropic google-generativeai pillow pyautogui pyotp aiohttp
```

**Verify installation**:
```bash
python3 -c "import anthropic; print('✅ Anthropic SDK installed')"
python3 -c "import google.generativeai; print('✅ Google Gemini SDK installed')"
python3 -c "import pyautogui; print('✅ pyautogui installed')"
```

### Step 2: Platform-Specific Setup

#### macOS

**Grant Accessibility Permissions**:

pyautogui requires accessibility permissions to control the mouse and keyboard.

1. Open **System Preferences** → **Security & Privacy** → **Privacy**
2. Select **Accessibility** in the left sidebar
3. Click the lock icon and authenticate
4. Click **+** and add your terminal app (Terminal.app, iTerm2, etc.)
5. Check the box next to your terminal app

**Verify**:
```bash
python3 -c "import pyautogui; pyautogui.position(); print('✅ Mouse control works')"
```

#### Linux

**Install X11 tools**:

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-xlib xdotool

# Fedora
sudo dnf install python3-xlib xdotool
```

**For headless servers**, install virtual display:
```bash
sudo apt-get install xvfb
```

**Verify**:
```bash
python3 -c "import pyautogui; print('✅ Desktop automation ready')"
```

#### Windows

Windows support is planned but not yet implemented. You can help by contributing!

## Configuration

### Step 1: Set Up Environment Variables

Copy the example file:
```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```bash
# AI Provider API Keys
# You need at least ONE of these:

# Anthropic API Key (for Claude)
ANTHROPIC_API_KEY=sk-ant-api03-YOUR-KEY-HERE

# Google API Key (for Gemini - alternative provider)
# GOOGLE_API_KEY=YOUR-GOOGLE-API-KEY-HERE

# Product Authentication
SCREENSHOT_USER=your-username@example.com
SCREENSHOT_PASS=your-secure-password

# Optional: TOTP secret for 2FA
# TOTP_SECRET=YOUR-BASE32-SECRET
```

**Important**: Add `.env` to your `.gitignore` (it should already be there).

#### Choosing an AI Provider

max-doc-AI supports two AI providers for Computer Use screenshot capture:

**Anthropic Claude (Default)**:
- Models: `claude-sonnet-4-5`, `claude-opus-4-5`
- Pricing: $3-15/MTok input, $15-75/MTok output
- Best for: Highest quality and reliability
- Get key: [console.anthropic.com](https://console.anthropic.com)

**Google Gemini (Alternative)**:
- Models: `gemini-2.5-flash`, `gemini-2.0-flash-exp`
- Pricing: More cost-effective for high-volume usage
- Best for: Faster response times, budget-friendly
- Get key: [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

**Provider Selection**: The system automatically selects the provider based on which API key is available. If both are set, it defaults to Anthropic unless you explicitly configure otherwise in `config.yaml`.

### Step 2: Configure config.yaml

Copy the example configuration:
```bash
cp config.example.yaml config.yaml
```

Edit `config.yaml` and configure Computer Use:

#### Option 1: Using Anthropic Claude (Default)

```yaml
screenshots:
  # Select implementation
  implementation: "computer_use"  # or "playwright" for fallback

  # Display settings (keep ≤ 1280x800 for best accuracy)
  viewport_width: 1280
  viewport_height: 800

  # AI Provider Selection (optional - auto-detects if not specified)
  provider: "anthropic"  # or "google" for Gemini

  # Model selection
  model: "claude-sonnet-4-5"  # or claude-opus-4-5

  # API key (from .env)
  api_key: "${ANTHROPIC_API_KEY}"

  # Authentication
  auth:
    enabled: true
    type: "sso"  # or "username_password"
    login_url: "${PRODUCT_URL}/login"
    username: "${SCREENSHOT_USER}"
    password: "${SCREENSHOT_PASS}"
    sso_provider: "google"  # google, okta, azure, auth0, etc.

    # Optional: Multi-factor authentication
    mfa:
      enabled: false
      type: "totp"
      totp_secret: "${TOTP_SECRET}"
```

#### Option 2: Using Google Gemini

```yaml
screenshots:
  implementation: "computer_use"
  viewport_width: 1280
  viewport_height: 800

  # Explicitly select Google provider
  provider: "google"

  # Gemini model selection
  model: "gemini-2.5-flash"  # or gemini-2.0-flash-exp

  # Google API key (from .env)
  google_api_key: "${GOOGLE_API_KEY}"

  # Authentication (same as Claude)
  auth:
    enabled: true
    type: "sso"
    login_url: "${PRODUCT_URL}/login"
    username: "${SCREENSHOT_USER}"
    password: "${SCREENSHOT_PASS}"
    sso_provider: "google"
```

**Note**: If you don't specify a `provider`, the system will automatically choose based on which API key is available.

### Step 3: Update Product Information

Make sure your product URL is set:

```yaml
product:
  name: "YourProduct"
  url: "https://app.yourproduct.com"
```

## Verification

### Test 1: Configuration Loading

Verify your configuration loads correctly:

```bash
python3 -c "
import sys
sys.path.insert(0, 'scripts')
import config as cfg
print('✅ Config loaded')
print(f'   Product: {cfg.get_product_name()}')
print(f'   Implementation: {cfg.get_screenshot_config().get(\"implementation\")}')
"
```

### Test 2: API Key

Test your Anthropic API key:

```bash
python3 -c "
import anthropic
import os
from dotenv import load_dotenv
load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
response = client.messages.create(
    model='claude-sonnet-4-5',
    max_tokens=10,
    messages=[{'role': 'user', 'content': 'Hi'}]
)
print('✅ API key works')
print(f'   Model: {response.model}')
"
```

### Test 3: Desktop Automation

Test desktop automation (this will move your mouse):

```bash
python3 -c "
import pyautogui
import time

print('Testing desktop automation...')
print('Your mouse will move in 2 seconds...')
time.sleep(2)

# Save current position
x, y = pyautogui.position()
print(f'Current position: ({x}, {y})')

# Move mouse slightly
pyautogui.moveRel(10, 10, duration=0.5)
time.sleep(0.5)

# Return to original position
pyautogui.moveTo(x, y, duration=0.5)

print('✅ Desktop automation works')
"
```

### Test 4: Screenshot Capture

Test basic screenshot capture:

```bash
python3 -c "
import sys
sys.path.insert(0, 'scripts')
from screenshot.computer_use_tools import ComputerUseTool
import asyncio

async def test():
    tool = ComputerUseTool()
    screenshot = await tool._screenshot({})
    print('✅ Screenshot capture works')
    print(f'   Type: {type(screenshot)}')
    print(f'   Length: {len(screenshot)} chars')

asyncio.run(test())
"
```

### Test 5: Full Integration Test

Run the comprehensive test script:

```bash
python3 scripts/screenshot/test_computer_use.py
```

This will:
- Verify all dependencies
- Test configuration
- Test API connectivity
- Perform a simple screenshot capture
- Report any issues

## Authentication Setup

### SSO Authentication

If your product uses SSO (Google, Okta, Azure, etc.):

1. **Identify the SSO provider**: Note which SSO button you click during login
2. **Configure in config.yaml**:
   ```yaml
   auth:
     type: "sso"
     sso_provider: "google"  # or okta, azure, auth0
   ```
3. **Provide SSO credentials**: Use your SSO email and password in `.env`

### Username/Password Authentication

For direct username/password login:

```yaml
auth:
  type: "username_password"
  login_url: "${PRODUCT_URL}/login"
```

### Multi-Factor Authentication (MFA)

#### TOTP (Google Authenticator, Authy)

If your product uses TOTP-based 2FA:

1. **Get your TOTP secret**:
   - When setting up 2FA, your product shows a QR code
   - Look for "Can't scan?" or "Manual entry" option
   - Copy the base32 secret (e.g., `JBSWY3DPEHPK3PXP`)

2. **Add to .env**:
   ```bash
   TOTP_SECRET=JBSWY3DPEHPK3PXP
   ```

3. **Enable in config.yaml**:
   ```yaml
   mfa:
     enabled: true
     type: "totp"
     totp_secret: "${TOTP_SECRET}"
   ```

4. **Test TOTP generation**:
   ```bash
   python3 -c "
   import pyotp
   import os
   from dotenv import load_dotenv
   load_dotenv()

   secret = os.getenv('TOTP_SECRET')
   totp = pyotp.TOTP(secret)
   code = totp.now()
   print(f'✅ TOTP code: {code}')
   print('Try logging in with this code')
   "
   ```

#### SMS or Manual MFA

For SMS or manual MFA entry:

```yaml
mfa:
  enabled: false  # Keep disabled for now
  type: "manual"
```

When MFA is required, the Computer Use agent will pause and you'll need to manually enter the code. This will be improved in future versions.

## Cost Estimation

Computer Use API costs vary by model and usage.

### Pricing (as of January 2025)

- **Claude Sonnet 4.5**: $3/MTok input, $15/MTok output (recommended)
- **Claude Opus 4.5**: $15/MTok input, $75/MTok output (highest quality)

### Typical Costs

**Single screenshot capture session**:
- Authentication: ~15k input tokens + ~3k output tokens = **$0.09**
- Per screenshot: ~3k input tokens + ~500 output tokens = **$0.02**

**Example scenarios**:
- 5 screenshots with auth: ~$0.17
- 100 screenshots/month (20 sessions): ~$3.40
- 1000 screenshots/month: ~$34

**Cost optimization**:
- Use Sonnet 4.5 instead of Opus (5x cheaper)
- Batch screenshots in single sessions (shared auth cost)
- Only capture when needed

### Gemini Pricing

**Google Gemini** offers more cost-effective pricing:

- **Gemini 2.5 Flash**: Significantly cheaper than Claude
- **Gemini 2.0 Flash Exp**: Experimental model with fast response times

**Typical costs with Gemini**:
- Authentication: ~$0.03
- Per screenshot: ~$0.01
- 5 screenshots with auth: ~$0.08
- 100 screenshots/month: ~$1.50
- 1000 screenshots/month: ~$15

**Cost comparison**:
- Gemini: ~50% cheaper than Claude Sonnet
- Claude Opus: Most accurate, highest cost
- Claude Sonnet: Best balance
- Gemini Flash: Most cost-effective

**Choosing a provider**:
- Use **Claude Sonnet** for highest quality and reliability
- Use **Gemini Flash** for high-volume, budget-conscious workflows
- Try both and see which works best for your product

### Compare to Playwright

Playwright is "free" but:
- Engineer time debugging auth issues: **$200-500/month**
- Updating CSS selectors: **$100-200/month**
- Maintenance overhead: **Significant**

**Computer Use pays for itself** by eliminating these hidden costs, regardless of which AI provider you choose.

## Troubleshooting

### "No module named 'anthropic'" or "No module named 'google.generativeai'"

**Problem**: Python package not installed.

**Solution**:
```bash
# For Anthropic
pip install anthropic>=0.40.0

# For Google Gemini
pip install google-generativeai>=0.3.0

# Or install all dependencies
pip install -r requirements.txt
```

### "ANTHROPIC_API_KEY not set" or "GOOGLE_API_KEY not found"

**Problem**: Environment variable not loaded.

**Solution**:
1. Check `.env` file exists: `ls -la .env`
2. Verify API key is set:
   ```bash
   grep ANTHROPIC .env
   # or
   grep GOOGLE .env
   ```
3. Make sure no spaces around `=`:
   - `ANTHROPIC_API_KEY=sk-ant-...`
   - `GOOGLE_API_KEY=AIza...`
4. If using Gemini, make sure you have the correct provider set in `config.yaml`:
   ```yaml
   screenshots:
     provider: "google"
     google_api_key: "${GOOGLE_API_KEY}"
   ```

### "Google provider selected but GOOGLE_API_KEY not found"

**Problem**: Config specifies Google provider but no API key is available.

**Solution**:
1. Add `GOOGLE_API_KEY` to your `.env` file
2. Or switch to Anthropic provider in `config.yaml`
3. Or remove the `provider` setting to let it auto-detect

### "pyautogui.FailSafeException"

**Problem**: Mouse moved to corner (failsafe triggered).

**Solution**:
```python
# Disable failsafe in your script
import pyautogui
pyautogui.FAILSAFE = False
```

Or avoid moving mouse to corners during capture.

### "Permission denied" on macOS

**Problem**: Accessibility permissions not granted.

**Solution**: Follow macOS setup instructions above to grant accessibility permissions.

### Screenshots are blank or wrong size

**Problem**: Display configuration mismatch.

**Solution**:
1. Check your actual screen resolution:
   ```python
   import pyautogui
   print(pyautogui.size())
   ```
2. Update viewport in `config.yaml` to match
3. Keep dimensions ≤ 1280x800 for best Computer Use accuracy

### Authentication fails repeatedly

**Problem**: Credentials incorrect or login flow changed.

**Solution**:
1. Verify credentials by manually logging in
2. Check if login URL is correct
3. Review Computer Use agent output for error messages
4. Try increasing `max_iterations` in config
5. Check if CAPTCHA or unusual security measures are present

### "Rate limit exceeded"

**Problem**: Too many API requests.

**Solution**:
1. Wait a few minutes and try again
2. Reduce frequency of screenshot captures
3. Check your API usage at console.anthropic.com
4. Consider upgrading your API tier

### Computer Use takes too long

**Problem**: Agent loop iterations consuming time.

**Solution**:
1. This is expected - Computer Use trades speed for reliability
2. Typical session: 30-60 seconds for auth + 5-10 seconds per screenshot
3. Much faster than debugging Playwright failures
4. Consider batching screenshots to amortize auth cost

## Advanced Configuration

### Custom System Prompts

Customize how Claude approaches screenshot capture:

```yaml
computer_use:
  system_prompt_override: |
    You are capturing screenshots for product documentation.
    Be extra careful to wait for animations to complete.
    Verify every screenshot shows the intended content.
```

### Viewport Customization

Different resolutions for different use cases:

```yaml
screenshots:
  # Mobile
  viewport_width: 375
  viewport_height: 667

  # Tablet
  viewport_width: 768
  viewport_height: 1024

  # Desktop (default)
  viewport_width: 1280
  viewport_height: 800
```

### Multiple Environments

Set up different configs for dev/staging/prod:

```bash
# Development
cp config.yaml config.dev.yaml

# Staging
cp config.yaml config.staging.yaml

# Production
cp config.yaml config.prod.yaml
```

Use with:
```bash
CONFIG_FILE=config.staging.yaml python3 scripts/screenshot/demo_capture.py
```

## Next Steps

Now that Computer Use is set up:

1. **Run your first capture**:
   ```bash
   python3 scripts/screenshot/demo_capture.py
   ```

2. **Review the screenshots**:
   ```bash
   ls -lh output/screenshots/
   ```

3. **Compare with Playwright** (optional):
   ```bash
   # Switch to Playwright in config.yaml
   screenshots:
     implementation: "playwright"

   # Run same capture
   python3 scripts/screenshot/demo_capture.py

   # Compare quality and reliability
   ```

4. **Integrate into your workflow**:
   - Use in create-release skill
   - Automate with CI/CD
   - Schedule regular captures

5. **Read the migration guide**: [computer-use-migration.md](computer-use-migration.md)

## Getting Help

### Documentation

- [Computer Use Migration Guide](computer-use-migration.md)
- [Claude Computer Use Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)
- [max-doc-AI README](../README.md)

### Support

- **GitHub Issues**: [Report a bug](https://github.com/maxberko/max-doc-ai/issues)
- **Anthropic Support**: [Get help with Computer Use API](https://support.anthropic.com)

### Community

Share your experience:
- What problems did Computer Use solve for you?
- How does it compare to Playwright?
- What could be improved?

We'd love to hear from you!

---

**Happy Screenshot Capturing!** 📸
