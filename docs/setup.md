# Setup Guide

Complete installation and configuration guide for max-doc-AI.

## Prerequisites

Before you begin, ensure you have:

- **Claude Code** installed and configured
- **Python 3.8+** installed
- **Pylon account** with API access
- **Git** for version control (optional but recommended)

## Quick Start (5 minutes)

```bash
# 1. Clone or download the repository
git clone https://github.com/yourusername/max-doc-ai.git
cd max-doc-ai

# 2. Install Python dependencies (includes Computer Use API)
pip install -r requirements.txt

# 3. Copy example configuration files
cp config.example.yaml config.yaml
cp .env.example .env

# 4. Configure (see Configuration section below)
# Edit config.yaml and .env with your values

# 5. Test the installation
python3 scripts/config.py

# 6. Verify Computer Use setup
python3 scripts/screenshot/test_computer_use.py
```

## Detailed Setup

### Step 1: Install Dependencies

**Python Packages:**
```bash
pip install -r requirements.txt
```

This installs:
- `anthropic` - Claude Computer Use API for screenshot automation
- `pillow` - Image processing for screenshots
- `pyautogui` - Desktop automation for Computer Use
- `pyotp` - TOTP/MFA support for authentication
- `aiohttp` - Async HTTP client for Computer Use API
- `requests` - HTTP client for Pylon API
- `pyyaml` - YAML configuration parsing
- `python-dotenv` - Environment variable management

**Platform-Specific Setup:**

On **macOS**, grant accessibility permissions for pyautogui:
1. Go to System Preferences → Security & Privacy → Accessibility
2. Add Terminal (or your Python IDE) to the allowed apps

On **Linux**, install xdotool:
```bash
sudo apt-get install xdotool
```

See [Computer Use Setup Guide](computer-use-setup.md) for detailed configuration.

### Step 2: Configure Pylon

#### 2.1 Create Pylon Account

1. Sign up at https://usepylon.com
2. Create a new Knowledge Base
3. Note your Knowledge Base ID from the URL

#### 2.2 Generate API Key

1. Go to Pylon Settings → API Keys
2. Click "Create API Key"
3. Give it a descriptive name (e.g., "max-doc-AI")
4. Copy the API key (starts with `pylon_api_`)
5. Store it securely - you won't see it again

#### 2.3 Create Collections

Create collections for your documentation categories:

1. In Pylon, go to your Knowledge Base
2. Click "Collections" → "New Collection"
3. Create collections matching your categories:
   - `getting-started`
   - `features`
   - `integrations`
   - (Add more as needed)
4. Copy each collection ID from the URL when viewing it

#### 2.4 Get Author User ID

1. Go to your Pylon profile settings
2. Your user ID is in the URL or API responses
3. Alternatively, make a test API call and check the response

### Step 3: Configure Environment Variables

Edit `.env` file with your Pylon credentials:

```bash
# Pylon Configuration
PYLON_API_KEY=pylon_api_your_actual_key_here
PYLON_KB_ID=your-knowledge-base-id-here
PYLON_AUTHOR_ID=your-user-id-here

# Collection IDs (from Pylon)
COLLECTION_GETTING_STARTED_ID=collection-id-1
COLLECTION_FEATURES_ID=collection-id-2
COLLECTION_INTEGRATIONS_ID=collection-id-3
```

**Security Note:** Never commit `.env` to version control. It's in `.gitignore` by default.

### Step 4: Configure Product Settings

Edit `config.yaml` with your product information:

```yaml
product:
  name: "YourProduct"
  url: "https://app.yourproduct.com"
  documentation_url: "https://docs.yourproduct.com"
```

**Customize:**
- Replace "YourProduct" with your product name
- Update URLs to match your application
- Adjust screenshot viewport size if needed
- Modify documentation categories as appropriate

### Step 5: Setup Authentication for Screenshots

max-doc-AI uses Claude's Computer Use API for screenshot automation, which handles authentication automatically via visual login.

**Configure authentication in `.env`:**

```bash
# Anthropic API for Computer Use
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx

# Screenshot Authentication (for visual login)
SCREENSHOT_USER=your-username@example.com
SCREENSHOT_PASS=your-password

# Optional: TOTP for MFA
TOTP_SECRET=BASE32SECRET
```

**Configure in `config.yaml`:**

```yaml
screenshots:
  auth:
    enabled: true
    type: "sso"  # or "username_password"
    login_url: "${PRODUCT_URL}/login"
    username: "${SCREENSHOT_USER}"
    password: "${SCREENSHOT_PASS}"
    sso_provider: "google"  # if using SSO
```

**How it works:**
- Computer Use performs visual authentication each session
- No cookie management or session expiration issues
- Works with any authentication method (SSO, username/password, MFA)

See [Computer Use Setup Guide](computer-use-setup.md) for detailed configuration.

### Step 6: Verify Installation

Test that everything is configured correctly:

```bash
# Test configuration loading
python3 scripts/config.py

# Check Pylon connection
python3 scripts/pylon/upload.py

# View state (should be empty initially)
python3 scripts/utils/state.py --summary
```

**Expected output:**
- Config loads without errors
- Pylon API credentials are valid
- State file is initialized

## Configuration Files

### config.yaml

Main configuration file. See [Configuration Guide](configuration.md) for detailed options.

**Key sections:**
- `product` - Your product information
- `pylon` - Pylon API settings
- `screenshots` - Screenshot capture settings
- `documentation` - Documentation paths
- `announcements` - Changelog settings

### .env

Environment variables for sensitive data.

**Never commit this file to version control.**

Contains:
- Anthropic API key (for Computer Use)
- Screenshot credentials (username/password)
- Pylon API key
- Knowledge Base ID
- Author User ID
- Collection IDs

## Directory Structure

After setup, your directory should look like:

```
max-doc-ai/
├── .claude/
│   └── skills/          # Claude Code skills
├── scripts/
│   ├── config.py        # Configuration loader
│   ├── auth_manager.py  # (deprecated - legacy Playwright only)
│   ├── pylon/           # Pylon integration
│   ├── screenshot/      # Screenshot capture (Computer Use)
│   └── utils/           # Utilities
├── output/              # Generated content (screenshots, docs, changelogs)
├── demo/                # Example documentation (reference only)
│   └── docs/
├── docs/                # Setup guides (this file)
├── config.yaml          # Your configuration
├── .env                 # Your environment variables
└── requirements.txt     # Python dependencies
```

## Troubleshooting

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'anthropic'`

**Solution:**
```bash
pip install -r requirements.txt
```

**Problem:** Computer Use dependencies not working

**Solution:**
```bash
# Verify installation
python3 scripts/screenshot/test_computer_use.py

# See docs/computer-use-setup.md for detailed troubleshooting
```

### Configuration Errors

**Problem:** `FileNotFoundError: Configuration file not found`

**Solution:**
```bash
cp config.example.yaml config.yaml
# Edit config.yaml with your values
```

### Pylon API Errors

**Problem:** `401 Unauthorized`

**Solution:**
- Check that `PYLON_API_KEY` is set correctly in `.env`
- Verify the API key is active in Pylon settings
- Try generating a new API key

**Problem:** `Collection not found`

**Solution:**
- Verify collection IDs in `.env` are correct
- Check that collections exist in Pylon
- Ensure collection names in `config.yaml` match `.env` variables

### Screenshot/Computer Use Errors

**Problem:** Screenshots are blank or show login page

**Solution:**
- Verify `SCREENSHOT_USER` and `SCREENSHOT_PASS` are correct in `.env`
- Check authentication configuration in `config.yaml`
- Ensure login URL is correct
- Run test script: `python3 scripts/screenshot/test_computer_use.py`
- See [Computer Use Setup Guide](computer-use-setup.md) for detailed troubleshooting

**Problem:** Computer Use API errors

**Solution:**
- Verify `ANTHROPIC_API_KEY` is set correctly in `.env`
- Check API key is active at console.anthropic.com
- Ensure you have sufficient API credits
- Check viewport size is ≤ 1280x800 (larger sizes may cause coordinate issues)

## Next Steps

After setup is complete:

1. **Read the [Usage Guide](usage.md)** - Learn how to use the Claude skills
2. **Review [Configuration Guide](configuration.md)** - Understand all configuration options
3. **Check [Pylon Integration](pylon-integration.md)** - Deep dive on Pylon specifics
4. **Try the demo** - Explore the FlowState example documentation

## Getting Help

If you encounter issues:

- Check the [troubleshooting section](#troubleshooting) above
- Review error messages carefully
- Ensure all prerequisites are met
- Verify configuration files are correct
- Test individual components (config, Pylon, screenshots) separately

For bugs or feature requests, please open an issue on GitHub.
