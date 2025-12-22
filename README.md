# max-doc-AI

**Automate your product documentation workflow with Claude Code.**

max-doc-AI is a collection of Claude Code skills that automate the entire process of creating, updating, and distributing product documentation. From capturing screenshots to syncing with your knowledge base to generating customer announcements—all powered by AI.

## What It Does

max-doc-AI provides 5 integrated Claude skills that work together:

- **📸 capture-screenshots** - Automated screenshot capture using Playwright
- **📝 update-product-doc** - AI-generated documentation from your codebase
- **☁️ sync-docs** - Upload to Pylon CDN and sync to knowledge base
- **📢 create-changelog** - Generate customer announcements for Slack/Email
- **🚀 create-release** - Orchestrate the complete release workflow

## Key Features

✅ **Fully Automated** - One command to generate complete release materials
✅ **Codebase-Aware** - Claude researches your code to understand features
✅ **Screenshot Automation** - Authenticated browser automation with Playwright
✅ **Knowledge Base Integration** - Direct sync with Pylon KB
✅ **Multi-Channel Announcements** - Generate Slack and email variations
✅ **State Tracking** - Track what's synced to avoid duplicates

## Quick Start

### Prerequisites

- [Claude Code](https://claude.com/claude-code) installed and configured
- Python 3.8+
- Pylon account with API access

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/max-doc-ai.git
cd max-doc-ai

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install Playwright browsers
playwright install chromium

# 4. Copy and configure
cp config.example.yaml config.yaml
cp .env.example .env

# 5. Edit config.yaml and .env with your values
# See docs/setup.md for detailed configuration

# 6. Set up authentication for screenshots
python3 scripts/auth_manager.py
```

### Basic Usage

**Complete release workflow:**
```
@claude Create a release for the Dashboards feature
```

Claude will automatically:
1. Research the feature in your codebase
2. Capture product screenshots
3. Generate comprehensive documentation
4. Upload screenshots to Pylon CDN
5. Sync documentation to Pylon KB
6. Create customer announcements

**Or use individual skills:**
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

- **[Setup Guide](docs/setup.md)** - Complete installation and configuration
- **[Usage Guide](docs/usage.md)** - How to use each skill
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
│       └── state.py         # Sync state tracking
├── demo/                    # Example documentation
│   └── docs/
│       └── product_documentation/
├── docs/                    # Setup guides
├── config.example.yaml      # Configuration template
├── .env.example             # Environment variables template
└── requirements.txt         # Python dependencies
```

## How It Works

### 1. Codebase Research
Claude explores your codebase to understand the feature implementation, patterns, and architecture.

### 2. Screenshot Capture
Playwright automates browser navigation with saved authentication sessions to capture consistent, professional screenshots.

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
- **Slack**: Short, engaging format with emojis
- **Email**: Detailed explanation with examples

## Configuration

The system is configured via two files:

**config.yaml** - Product and workflow settings
```yaml
product:
  name: "YourProduct"
  url: "https://app.yourproduct.com"

pylon:
  collections:
    getting-started: "${COLLECTION_GETTING_STARTED_ID}"
    features: "${COLLECTION_FEATURES_ID}"
```

**.env** - API keys and IDs (never commit this!)
```bash
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
- **Playwright** - Browser automation for screenshots
- **Pylon Account** - Knowledge base and CDN hosting
- **Product Access** - Authenticated access to capture screenshots

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone and install dependencies
git clone https://github.com/yourusername/max-doc-ai.git
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
- ✅ Free to use, modify, and distribute
- ✅ Patent protection included
- ⚠️ Derivative works must also be GPL v3
- ⚠️ Source code must be made available with distributions

For the full license text, visit: https://www.gnu.org/licenses/gpl-3.0.txt

## Acknowledgments

Built with:
- [Claude Code](https://claude.com/claude-code) - AI-powered CLI
- [Playwright](https://playwright.dev/) - Browser automation
- [Pylon](https://usepylon.com) - Knowledge base platform

---

**Made with Claude Code** 🤖
