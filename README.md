# max-doc-AI

Automate product documentation workflows with Claude Code.

max-doc-AI is a collection of Claude Code skills that automate documentation creation, screenshot capture, and customer announcements. Point it at your codebase, and it handles the documentation workflow end-to-end.

## What It Does

max-doc-AI provides 5 integrated Claude skills:

- **📸 capture-screenshots** - Automated screenshot capture using Claude's Computer Use API
- **📝 update-product-doc** - AI-generated documentation from your codebase
- **☁️ sync-docs** - Upload to Pylon CDN and sync to knowledge base
- **📢 create-changelog** - Generate customer announcements for Slack/Email
- **🚀 create-release** - Orchestrate the complete release workflow

## How It Works

### 1. Codebase Research
Claude explores your codebase to understand the feature implementation, patterns, and architecture.

### 2. Screenshot Capture
Claude's Computer Use API provides visual browser automation with intelligent authentication and content verification for reliable screenshots.

### 3. Documentation Generation
Claude writes comprehensive documentation including:
- Feature overview
- Configuration steps
- Use cases
- Embedded screenshots

### 4. Knowledge Base Sync
Documentation and screenshots are uploaded to Pylon:
- Images → Pylon CDN (CloudFront URLs)
- Docs → Pylon KB (organized by collections)

### 5. Customer Announcements
Generate targeted announcements:
- **Slack**: Short, engaging format
- **Email**: Detailed explanation with examples

## Key Features

- **Fully Automated** - One command generates complete release materials
- **Codebase-Aware** - Claude researches your code to understand features
- **Intelligent Screenshot Capture** - Computer Use API with visual authentication (no session expiration!)
- **Reliable Content Capture** - Claude waits naturally for pages to load and verifies content
- **Knowledge Base Integration** - Direct sync with Pylon KB
- **Multi-Channel Announcements** - Generate Slack and email variations
- **State Tracking** - Track what's synced to avoid duplicates

## Quick Start

### Prerequisites

- [Claude Code](https://claude.com/claude-code) installed and configured
- Python 3.8+
- Pylon account with API access

### Setting Up Claude

Before you can use max-doc-AI, you need to set up your Claude account and API key:

#### 1. Create a Claude Account

If you don't have a Claude account yet:
1. Visit [claude.ai](https://claude.ai)
2. Sign up for an account (you can use Google, email, or other sign-in options)
3. Verify your email address if required

#### 2. Get Your Claude API Key

To use Claude Code and max-doc-AI, you'll need an API key:

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign in with your Claude account
3. Navigate to **API Keys** in the left sidebar
4. Click **Create Key**
5. Give your key a descriptive name (e.g., "max-doc-ai-local")
6. Copy the API key immediately (you won't be able to see it again)

**Important:** Keep your API key secure and never commit it to version control.

#### 3. Install Claude Code CLI

Install the Claude Code command-line tool:

```bash
# macOS/Linux
brew install anthropics/tap/claude

# Or using npm
npm install -g @anthropic-ai/claude-code

# Or using pip
pip install claude-code
```

Verify the installation:
```bash
claude --version
```

#### 4. Configure Your API Key

Set up your API key for Claude Code:

```bash
# Option 1: Interactive setup (recommended)
claude auth login

# Option 2: Set environment variable
export ANTHROPIC_API_KEY=your-api-key-here

# Option 3: Add to your shell profile for persistence
echo 'export ANTHROPIC_API_KEY=your-api-key-here' >> ~/.zshrc  # or ~/.bashrc
source ~/.zshrc  # or ~/.bashrc
```

**Verify your setup:**
```bash
claude run "print hello world"
```

If you see a response from Claude, you're all set!

**Usage Costs:** Claude API usage is billed based on tokens processed. Check current pricing at [anthropic.com/pricing](https://www.anthropic.com/pricing). max-doc-AI operations typically cost between $0.10-$0.50 per feature release depending on codebase size.

### Installation

#### Option 1: Interactive Setup (Recommended)

The easiest way to get started:

```bash
# 1. Clone the repository
git clone https://github.com/maxberko/max-doc-ai.git
cd max-doc-ai

# 2. Run the interactive setup wizard
python3 scripts/setup.py

# 3. Verify everything works
python3 scripts/health_check.py

# 4. Create your first release
claude "Create a release for [your feature name]"
```

**Done!** You're ready to go in under 5 minutes. 🚀

The setup wizard will:
- Check your system requirements
- Help you choose a knowledge base provider (Pylon, Zendesk, etc.)
- Collect your credentials securely
- Create configuration files automatically
- Verify your connection
- Show you exactly what to do next

For detailed information, see **[GETTING_STARTED.md](GETTING_STARTED.md)**.

#### Option 2: Manual Configuration (Advanced)

For advanced users who prefer manual setup:

```bash
# 1. Clone and install dependencies
git clone https://github.com/maxberko/max-doc-ai.git
cd max-doc-ai
pip install -r requirements.txt

# 2. Copy configuration templates
cp config.example.yaml config.yaml
cp .env.example .env

# 3. Configure your environment
# Edit .env with your credentials:
#   - ANTHROPIC_API_KEY=your-api-key
#   - SCREENSHOT_USER=your-product-username
#   - SCREENSHOT_PASS=your-product-password
#   - PYLON_API_KEY=your-pylon-key
#   (and other required keys)

# 4. Update config.yaml with your product details
# See docs/computer-use-setup.md for detailed configuration

# 5. Verify Computer Use setup
python3 scripts/screenshot/test_computer_use.py
```

**macOS Users**: Grant accessibility permissions for pyautogui in System Preferences → Security & Privacy → Accessibility.

**See**: [Computer Use Setup Guide](docs/computer-use-setup.md) for complete installation instructions.

### Basic Usage

Complete release workflow:
```
@claude Create a release for the Dashboards feature
```

**Interactive Pre-Flight:**
Claude will first ask you a series of questions to configure the release:
- How to provide feature information (PRD text, short description, or feature name)
- Repository source (current codebase or external GitHub repo)
- Release date (today or specify a date in YYYY-MM-DD format)

**Automated Execution:**
After collecting information, Claude will automatically:
1. Research the feature in your codebase (or clone external repo)
2. Capture product screenshots
3. Generate comprehensive documentation
4. Upload screenshots to Pylon CDN
5. Sync documentation to Pylon KB
6. Create customer announcements

**Output Structure:**

**IMPORTANT:** All generated files are saved to the `./output/` directory. Nothing is saved outside this folder.

```
output/
├── features/YYYY-MM-DD_feature-name/
│   └── feature-name.md              # Complete documentation
├── changelogs/YYYY-MM-DD/
│   └── feature-name/
│       ├── slack-announcement.md    # Slack announcement
│       ├── email-announcement.md    # Email announcement
│       └── README.md                # Release metadata
├── screenshots/
│   └── feature-name-*.png           # Product screenshots
└── sync-state.json                  # Pylon sync state tracking
```

**Dated Organization:** Features and changelogs are organized by release date (YYYY-MM-DD format) for easy tracking and archiving.

Or use individual skills:
```
@claude Skill: capture-screenshots
Feature: User Authentication
URLs: /login, /signup, /settings

@claude Skill: update-product-doc
Feature: User Authentication
Category: getting-started

@claude Skill: create-changelog
Feature: User Authentication
Documentation URL: [Pylon URL]
```

## Documentation

### Getting Started
- **[Computer Use Setup](docs/computer-use-setup.md)** - Set up Claude's Computer Use API for screenshots
- **[Setup Guide](docs/setup.md)** - Complete installation and configuration
- **[Usage Guide](docs/usage.md)** - How to use each skill

### Advanced
- **[Configuration Reference](docs/configuration.md)** - All configuration options
- **[Pylon Integration](docs/pylon-integration.md)** - Deep dive on Pylon KB integration
- **[Demo Product](docs/demo-product.md)** - Example documentation workflow

## Project Structure

```
max-doc-ai/
├── .claude/
│   └── skills/              # Claude Code skills
│       ├── create-release/
│       ├── capture-screenshots/
│       ├── update-product-doc/
│       ├── sync-docs/
│       └── create-changelog/
├── scripts/
│   ├── config.py            # Configuration loader
│   ├── auth_manager.py      # Browser authentication
│   ├── pylon/               # Pylon API integration
│   │   ├── upload.py        # Screenshot upload to CDN
│   │   └── sync.py          # Documentation sync
│   ├── screenshot/          # Screenshot capture
│   │   └── capture.py       # Playwright automation
│   └── utils/               # Utilities
│       ├── state.py         # Sync state tracking
│       ├── github_helper.py # GitHub repository integration
│       └── migrate_output.py # Migration helper
├── output/                  # ALL GENERATED FILES GO HERE
│   ├── features/            # Documentation: YYYY-MM-DD_feature-name/
│   ├── changelogs/          # Announcements: YYYY-MM-DD/feature-name/
│   ├── screenshots/         # All product screenshots
│   └── sync-state.json      # Pylon sync tracking
├── demo/                    # Example documentation (reference only)
│   └── docs/
│       └── product_documentation/
├── docs/                    # Setup guides
├── config.example.yaml      # Configuration template
├── .env.example             # Environment variables template
└── requirements.txt         # Python dependencies
```

## Configuration

The system is configured via two files:

**config.yaml** - Product and workflow settings
```yaml
product:
  name: "YourProduct"
  url: "https://app.yourproduct.com"

screenshots:
  viewport_width: 1280
  viewport_height: 800
  model: "claude-sonnet-4-5"

  auth:
    enabled: true
    type: "sso"
    login_url: "${PRODUCT_URL}/login"
    username: "${SCREENSHOT_USER}"
    password: "${SCREENSHOT_PASS}"
    sso_provider: "google"

pylon:
  collections:
    getting-started: "${COLLECTION_GETTING_STARTED_ID}"
    features: "${COLLECTION_FEATURES_ID}"
```

**.env** - API keys and IDs (never commit this!)
```bash
# Claude API for Computer Use
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx

# Screenshot Authentication
SCREENSHOT_USER=your-username@example.com
SCREENSHOT_PASS=your-password

# Pylon API
PYLON_API_KEY=pylon_api_xxxxx
PYLON_KB_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
COLLECTION_FEATURES_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

See [Configuration Reference](docs/configuration.md) for all options.

## Use Cases

### Product Teams
- Automate release documentation
- Keep KB in sync with product
- Generate consistent customer communications

### Developer Relations
- Document new features as they ship
- Create educational content from code
- Maintain up-to-date product guides

### Technical Writers
- Accelerate documentation creation
- Ensure technical accuracy from code
- Manage multi-channel content distribution

## Requirements

- **Claude Code** - The CLI tool that runs the skills
- **Python 3.8+** - For scripts and automation
- **Anthropic API Key** - For Computer Use API (screenshot automation)
- **Pylon Account** - Knowledge base and CDN hosting
- **Product Credentials** - Username/password for visual authentication during screenshot capture

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone and install dependencies
git clone https://github.com/maxberko/max-doc-ai.git
cd max-doc-ai
pip install -r requirements.txt

# Configure for your test environment
cp config.example.yaml config.yaml
cp .env.example .env
# Edit with your test Pylon KB credentials

# Test individual components
python3 scripts/config.py              # Verify config
python3 scripts/auth_manager.py        # Test auth flow
python3 scripts/utils/state.py         # Check state tracking
```

## Roadmap

- [ ] Support additional CDN providers (Cloudinary, S3)
- [ ] Additional announcement channels (Discord, Teams)
- [ ] Video recording support (demo workflows)
- [ ] Multi-language documentation support
- [ ] Versioned documentation (per release)
- [ ] Integration with other knowledge bases (Notion, GitBook)

## Troubleshooting

**Screenshots are blank/empty:**
- Re-run `python3 scripts/auth_manager.py` to refresh auth session
- Check viewport size matches your product's responsive breakpoints

**Pylon API errors:**
- Verify API key in `.env` is correct and active
- Check collection IDs match what exists in Pylon
- Ensure Knowledge Base ID is correct

**Claude can't find feature:**
- Provide more context about code location
- Check that feature code is committed
- Ensure Claude has access to the codebase

See [Setup Guide](docs/setup.md#troubleshooting) for more solutions.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

**Key points:**
- Free to use, modify, and distribute
- Patent protection included
- Derivative works must also be GPL v3
- Source code must be made available with distributions

For the full license text, visit: https://www.gnu.org/licenses/gpl-3.0.txt

## Acknowledgments

Built with:
- [Claude Code](https://claude.com/claude-code) - AI-powered CLI
- [Playwright](https://playwright.dev/) - Browser automation
- [Pylon](https://usepylon.com) - Knowledge base platform

---

**Made with Claude Code**
