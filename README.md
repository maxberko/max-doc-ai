# max-doc-AI

**Stop wrestling with documentation. Let AI handle it.**

max-doc-AI is your friendly automation toolkit for product documentation. Just tell Claude what feature you shipped, and it handles everything—screenshots, docs, announcements, the whole nine yards. It's like having a technical writer, designer, and DevRel person all rolled into one AI assistant.

## What It Does

Think of max-doc-AI as your documentation autopilot. It gives Claude 5 superpowers:

- **📸 capture-screenshots** - Opens your app, navigates around, snaps perfect screenshots
- **📝 update-product-doc** - Reads your code, writes comprehensive docs that actually make sense
- **☁️ sync-docs** - Uploads everything to Pylon (your knowledge base in the cloud)
- **📢 create-changelog** - Writes customer announcements for Slack and email
- **🚀 create-release** - Does all of the above in one go. Seriously, just one command.

## How It Works

Here's the magic behind the curtain:

### 1. Claude Studies Your Code
Claude explores your codebase like a detective—understanding how your feature works, what patterns you use, and how everything fits together.

### 2. Screenshots, Captured Automatically
Playwright (a browser automation tool) logs into your app and captures pixel-perfect screenshots. No more awkward cropping or forgetting to update images.

### 3. Documentation, Written for Humans
Claude writes docs that include:
- Clear feature overviews
- Step-by-step guides
- Real use cases
- All those screenshots, perfectly embedded

### 4. Everything Synced to Your Knowledge Base
Your docs and images get uploaded to Pylon:
- Images go to the CDN (fast CloudFront URLs)
- Docs go to your knowledge base (organized and searchable)

### 5. Announcements, Ready to Share
Claude generates customer announcements in two flavors:
- **Slack**: Quick, punchy, with emojis 🎉
- **Email**: Detailed with examples and links

## Why You'll Love It

✅ **One Command = Complete Release** - From code to customer announcement in minutes
✅ **Actually Understands Your Code** - Not just templates, Claude researches your implementation
✅ **Always Up-to-Date Screenshots** - Automated capture means images never get stale
✅ **No More Copy-Paste** - Direct sync with your knowledge base
✅ **Multi-Channel Ready** - Generate Slack, email, or both
✅ **Smart State Tracking** - Never accidentally duplicate content

## Quick Start

Ready to automate your docs? Let's get you set up.

### What You'll Need

- [Claude Code](https://claude.com/claude-code) - Get it from Anthropic
- Python 3.8 or newer
- A [Pylon](https://usepylon.com) account - Free to start

### Installation (5 minutes)

```bash
# 1. Clone this repo
git clone https://github.com/maxberko/max-doc-ai.git
cd max-doc-ai

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install the browser for screenshots
playwright install chromium

# 4. Set up your config files
cp config.example.yaml config.yaml
cp .env.example .env

# 5. Add your credentials to .env
# (Get these from your Pylon dashboard)

# 6. Save your login session for screenshots
python3 scripts/auth_manager.py
```

### Your First Release

Now comes the fun part. Just tell Claude what to document:

```
@claude Create a release for the Dashboards feature
```

That's it! Claude will:
1. Explore your codebase to understand the feature
2. Capture screenshots of your app
3. Write comprehensive documentation
4. Upload everything to Pylon
5. Generate Slack and email announcements

Grab a coffee while it works. ☕

### Or Go Step-by-Step

Prefer to break it down? Use individual skills:

```
@claude Skill: capture-screenshots
Feature: User Authentication
URLs: /login, /signup, /settings
```

```
@claude Skill: update-product-doc
Feature: User Authentication
Category: getting-started
```

```
@claude Skill: create-changelog
Feature: User Authentication
Documentation URL: [your Pylon URL]
```

## Real-World Use Cases

**Product Teams**: Ship features faster. While your code is being reviewed, Claude's already drafting the docs.

**Developer Relations**: Document everything as it ships. No more backlog of "we should probably document that."

**Technical Writers**: Spend time on strategy, not screenshot updates. Let automation handle the tedious parts.

**Solo Developers**: Get professional-looking documentation without hiring a technical writer.

## Documentation

Everything you need to know:

- **[Setup Guide](docs/setup.md)** - Detailed installation and configuration
- **[Usage Guide](docs/usage.md)** - How to use each skill
- **[Configuration Reference](docs/configuration.md)** - Every config option explained
- **[Pylon Integration](docs/pylon-integration.md)** - Deep dive on the Pylon API
- **[Demo Product](docs/demo-product.md)** - See a complete example (FlowState)

## Project Structure

Everything's organized and easy to find:

```
max-doc-ai/
├── .claude/skills/          # The 5 Claude skills
├── scripts/                 # Python automation
│   ├── pylon/              # Pylon API integration
│   ├── screenshot/         # Screenshot automation
│   └── utils/              # Helpers and state tracking
├── demo/                   # Example docs (FlowState product)
├── docs/                   # Setup and usage guides
├── config.example.yaml     # Your config template
└── .env.example            # Your secrets template
```

## Configuration

Two files control everything:

**config.yaml** - Your product info and preferences
```yaml
product:
  name: "YourProduct"
  url: "https://app.yourproduct.com"

pylon:
  collections:
    getting-started: "${COLLECTION_GETTING_STARTED_ID}"
    features: "${COLLECTION_FEATURES_ID}"
```

**.env** - Your API keys (keep this secret!)
```bash
PYLON_API_KEY=pylon_api_xxxxx
PYLON_KB_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
COLLECTION_FEATURES_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

Full details in the [Configuration Reference](docs/configuration.md).

## Troubleshooting

**Screenshots are blank?**
- Run `python3 scripts/auth_manager.py` again to refresh your login session
- Check that your viewport size matches your app's responsive breakpoints

**Pylon API errors?**
- Double-check your API key in `.env`
- Make sure your collection IDs are correct
- Verify your Knowledge Base ID

**Claude can't find your feature?**
- Give more context about where the code lives
- Make sure the feature code is committed
- Check that Claude has access to your codebase

More help in the [Setup Guide](docs/setup.md#troubleshooting).

## Contributing

We'd love your help! Whether it's fixing bugs, adding features, or improving docs—all contributions are welcome.

Check out [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone and install
git clone https://github.com/maxberko/max-doc-ai.git
cd max-doc-ai
pip install -r requirements.txt

# Configure for testing
cp config.example.yaml config.yaml
cp .env.example .env
# Use a test Pylon KB, not production!

# Verify everything works
python3 scripts/config.py
```

## What's Next

We're planning some exciting additions:

- [ ] Support for more CDN providers (Cloudinary, S3, etc.)
- [ ] Additional announcement channels (Discord, Teams, in-app)
- [ ] Video recording for product demos
- [ ] Multi-language documentation
- [ ] Versioned docs (different versions per release)
- [ ] Integration with Notion, GitBook, Confluence

Got ideas? Open an issue!

## Requirements

Here's what you need:

- **Claude Code** - The CLI that runs everything
- **Python 3.8+** - For the automation scripts
- **Playwright** - Powers the screenshot automation
- **Pylon Account** - Your knowledge base and CDN
- **App Access** - Login credentials to capture screenshots

## License

This project is open source under the GNU General Public License v3.0. See [LICENSE](LICENSE) for details.

**What this means:**
- ✅ Free to use, modify, and share
- ✅ Patent protection included
- ⚠️ If you modify and distribute it, your version must also be GPL v3
- ⚠️ You must share your source code

Full license: https://www.gnu.org/licenses/gpl-3.0.txt

## Built With Love (and AI)

Standing on the shoulders of giants:
- [Claude Code](https://claude.com/claude-code) - AI that actually understands code
- [Playwright](https://playwright.dev/) - Browser automation done right
- [Pylon](https://usepylon.com) - Beautiful knowledge bases

---

**Made with Claude Code** 🤖

*Questions? Open an issue. We're here to help!*
