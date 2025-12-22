## Overview

max-doc-ai automates your entire product documentation workflow using Claude Code. Instead of spending hours writing documentation, capturing screenshots, and creating announcements, point max-doc-ai at your codebase and it handles everything from research to publishing.

Built as a collection of Claude Code skills, max-doc-ai analyzes your code to understand features, captures consistent screenshots, generates comprehensive documentation, syncs to your knowledge base, and creates multi-channel announcements—all in a single command.

Perfect for product teams, developer relations, and technical writers who want to maintain accurate, up-to-date documentation without the manual effort.

## Key Capabilities

- **Codebase-Aware Documentation**: Claude analyzes your code to understand implementation details, user flows, and configuration options, ensuring technical accuracy
- **Automated Screenshot Capture**: Uses Playwright to capture consistent, high-quality screenshots with saved authentication sessions
- **Knowledge Base Integration**: Direct sync with Pylon KB including CDN hosting for images and automatic article publishing with proper collection assignment
- **Multi-Channel Announcements**: Generates tailored content for different channels—engaging Slack messages and detailed email announcements
- **Complete Release Workflow**: One command runs the entire process from research to published documentation without stopping
- **State Management**: Tracks sync state to prevent duplicates and enable updates without recreation

## How It Works

### The Complete Workflow

max-doc-ai orchestrates five specialized skills that work together:

**1. Research Phase**
Claude explores your codebase using the Explore agent to understand what the feature does, how it works, and how users interact with it. This ensures documentation reflects the actual implementation.

**2. Screenshot Capture**
Playwright opens a browser with your saved authentication session, navigates to specified URLs, waits for pages to fully load, and captures screenshots at a consistent viewport size (1470x840 by default).

**3. Image Upload**
Screenshots are uploaded to Pylon's CDN via the Attachments API, returning CloudFront URLs that will be embedded in the documentation.

**4. Documentation Generation**
Claude writes user-focused documentation based on codebase research, following your documentation patterns and embedding screenshots with CloudFront URLs at appropriate sections.

**5. Knowledge Base Sync**
Documentation is converted from markdown to HTML with Pylon-required React wrappers, then created or updated in your Pylon knowledge base with proper collection assignment.

**6. Announcement Creation**
Claude generates channel-specific announcements—a short, engaging Slack message (15-25 lines with emojis) and a detailed, professional email (40-60 lines)—both linking to the published documentation.

### Architecture

```
Claude Code CLI
    ↓
Skills (.claude/skills/)
    ↓
Python Scripts (scripts/)
    ↓
External Services (Pylon API, Playwright)
```

The framework uses Claude Code to execute skills, Python for API integrations and browser automation, and connects to Pylon for knowledge base management.

## Getting Started

### Prerequisites

- Claude Code installed and configured
- Python 3.8 or higher
- Pylon account with API access
- Product with web interface (for screenshots)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/maxberko/max-doc-ai.git
cd max-doc-ai
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
playwright install chromium
```

3. Copy configuration templates:
```bash
cp config.example.yaml config.yaml
cp .env.example .env
```

4. Configure environment variables in `.env`:
```bash
PYLON_API_KEY=pylon_api_xxxxx
PYLON_KB_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
PYLON_AUTHOR_ID=your-user-id
COLLECTION_GETTING_STARTED_ID=collection-id-1
COLLECTION_FEATURES_ID=collection-id-2
COLLECTION_INTEGRATIONS_ID=collection-id-3
```

5. Update `config.yaml` with your product details:
```yaml
product:
  name: "YourProduct"
  url: "https://app.yourproduct.com"
  documentation_url: "https://docs.yourproduct.com"
```

6. Save authentication session for screenshot capture:
```bash
python3 scripts/auth_manager.py
```

### Your First Release

Run the complete release workflow:

```bash
claude code
```

Then in Claude Code:
```
/create-release
```

Claude will ask you a few simple questions:
1. Describe the feature (name, short description, or paste a PRD)
2. Where is the code? (current codebase, folder path, or GitHub URL)
3. Release date (type "today" or specify a date)

After you confirm, the automation runs completely without stopping, producing:
- Screenshots in `output/screenshots/`
- Documentation in `output/features/YYYY-MM-DD_feature-name/`
- Announcements in `output/changelogs/YYYY-MM-DD/`
- Published article in Pylon KB

## Configuration

### Main Configuration (config.yaml)

```yaml
product:
  name: "YourProduct"
  url: "https://app.yourproduct.com"
  documentation_url: "https://docs.yourproduct.com"

pylon:
  api_key: "${PYLON_API_KEY}"
  kb_id: "${PYLON_KB_ID}"
  author_user_id: "${PYLON_AUTHOR_ID}"
  api_base: "https://api.usepylon.com"
  collections:
    getting-started: "${COLLECTION_GETTING_STARTED_ID}"
    features: "${COLLECTION_FEATURES_ID}"
    integrations: "${COLLECTION_INTEGRATIONS_ID}"

screenshots:
  viewport_width: 1470
  viewport_height: 840
  output_dir: "./demo/docs/product_documentation/screenshots"
  auth_session_file: "./scripts/auth_session.json"
  format: "png"
  quality: 90

documentation:
  base_path: "./demo/docs/product_documentation"
  categories:
    - getting-started
    - features
    - integrations

announcements:
  output_dir: "./demo/docs/product_documentation/changelog"
  channels:
    - slack
    - email
```

### Environment Variables (.env)

Store sensitive data in `.env` (never commit this file):

```bash
# Pylon API credentials
PYLON_API_KEY=pylon_api_xxxxx
PYLON_KB_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
PYLON_AUTHOR_ID=your-user-id

# Pylon collection IDs
COLLECTION_GETTING_STARTED_ID=collection-id-1
COLLECTION_FEATURES_ID=collection-id-2
COLLECTION_INTEGRATIONS_ID=collection-id-3
```

### Customization Options

**Viewport Size**: Adjust screenshot dimensions for brand consistency:
```yaml
screenshots:
  viewport_width: 1920  # Larger viewport
  viewport_height: 1080
```

**Categories**: Add custom documentation categories:
```yaml
documentation:
  categories:
    - getting-started
    - features
    - integrations
    - api-reference  # Custom category
    - tutorials      # Custom category
```

**Announcement Channels**: Configure which announcement formats to generate:
```yaml
announcements:
  channels:
    - slack
    - email
    - twitter  # Add custom channel
```

## Skills Reference

### create-release

**Purpose**: Master orchestrator that runs the complete release workflow from start to finish.

**When to use**: When a feature is complete and ready for customer communication.

**What it does**: Research → Screenshots → Upload → Documentation → Sync → Announcements

**Usage**:
```
/create-release
```

**Interactive prompts**:
- Feature description (name, description, or full PRD)
- Code location (current, folder path, or GitHub URL)
- Release date

**Output**: Complete release package with screenshots, documentation, and announcements.

### capture-screenshots

**Purpose**: Automated screenshot capture using Playwright browser automation.

**When to use**: When you need consistent product screenshots for documentation.

**What it does**:
- Loads saved authentication session
- Navigates to specified URLs
- Waits for page load and specific elements
- Captures screenshots at consistent viewport size

**Usage**: Create a capture script in `scripts/screenshot/` or invoke via create-release.

### update-product-doc

**Purpose**: Generate comprehensive, user-focused product documentation.

**When to use**: Creating new documentation or updating existing docs.

**What it does**:
- Researches feature implementation in codebase
- Generates documentation following established patterns
- Embeds screenshots using CloudFront URLs
- Saves markdown files ready for Pylon sync

**Output**: Markdown file in `demo/docs/product_documentation/[category]/`

### sync-docs

**Purpose**: Sync documentation and screenshots to Pylon knowledge base.

**Modes**:

**Mode 1 - Upload Screenshots**:
- Uploads images to Pylon Attachments API
- Returns CloudFront CDN URLs for embedding

**Mode 2 - Sync Documentation**:
- Converts markdown to HTML with React wrappers
- Creates or updates Pylon KB articles
- Sets collection_id for proper organization
- Returns public and internal article URLs

**Usage**: Invoked automatically by create-release or run manually via Python scripts.

### create-changelog

**Purpose**: Generate customer announcements for feature releases.

**When to use**: After documentation is published and you need to announce the feature.

**What it does**:
- Researches feature for value propositions
- Creates Slack announcement (15-25 lines, engaging, with emojis)
- Creates Email announcement (40-60 lines, professional, detailed)
- Includes links to Pylon documentation

**Output**: Announcement files in `output/changelogs/YYYY-MM-DD/`

## Use Cases

### Use Case 1: Weekly Feature Releases

**Situation**: Your team ships new features every week and needs to keep documentation current without dedicating writer resources to each release.

**Solution**: Run `/create-release` after merging each feature PR. max-doc-ai analyzes the code changes, captures screenshots of the new UI, generates documentation, and creates announcements—all in under 10 minutes.

**Benefit**: Documentation stays current with product without manual effort. Your support team and customers always have accurate information.

### Use Case 2: API Documentation Maintenance

**Situation**: Your API endpoints change frequently and documentation falls out of sync with implementation, causing integration issues for developers.

**Solution**: Use max-doc-ai to analyze your API route definitions, generate endpoint documentation with request/response examples, and sync to your developer portal automatically.

**Benefit**: API documentation always matches current implementation, reducing developer confusion and support tickets.

### Use Case 3: Integration Documentation

**Situation**: You're launching integrations with Slack, GitHub, and Jira. Each integration needs setup guides, configuration docs, and troubleshooting information.

**Solution**: Run max-doc-ai for each integration. It researches the authentication flow, available actions, and configuration options from your codebase, then generates complete integration guides.

**Benefit**: Consistent documentation format across all integrations, created in hours instead of days.

### Use Case 4: Product Launch Preparation

**Situation**: You're launching a major new feature and need documentation, screenshots, and announcements ready for launch day—all coordinated across multiple channels.

**Solution**: Run the complete release workflow once. max-doc-ai generates everything you need: polished documentation with screenshots, Slack message for internal team, and email announcement for customers.

**Benefit**: All launch materials ready in one automated workflow, ensuring consistency across channels and saving days of manual work.

### Use Case 5: Documentation Audit and Updates

**Situation**: Your documentation is months old and no longer reflects current product state. You need to update dozens of articles but lack the time to research each change.

**Solution**: Run max-doc-ai's documentation skill for each outdated article. It researches current implementation, identifies what's changed, and generates updated documentation.

**Benefit**: Complete documentation refresh completed in days instead of weeks, with confidence that everything reflects current product state.

## FAQ

**Q: Does max-doc-ai work with any knowledge base platform?**

A: Currently, max-doc-ai integrates with Pylon KB. The architecture is designed for extensibility—you can add support for other platforms by creating new sync scripts in `scripts/pylon/`.

**Q: Can I customize the documentation templates?**

A: Yes! The documentation structure and writing style are controlled by skill instructions in `.claude/skills/update-product-doc/`. Edit these to match your brand voice and structure preferences.

**Q: How long does authentication session stay valid?**

A: Authentication sessions typically expire after 2-4 hours. If screenshot capture fails with authentication errors, run `python3 scripts/auth_manager.py` to save a fresh session.

**Q: Can I use max-doc-ai with private GitHub repositories?**

A: Yes! When the create-release skill detects a private GitHub URL, it automatically checks accessibility and asks for your authentication method (GitHub CLI, SSH, or Personal Access Token).

**Q: What happens if screenshot capture fails?**

A: The workflow continues without stopping. Failed screenshots are noted in the output, and you can manually capture and upload them later. Documentation and announcements are still generated.

**Q: Can I run individual skills instead of the complete workflow?**

A: Absolutely! Each skill can be invoked independently. For example, run `/update-product-doc` to just generate documentation, or invoke the Python scripts directly for more control.

**Q: Does this work for mobile apps or desktop applications?**

A: Screenshot capture requires a web interface accessible via browser. For mobile/desktop apps, you'd need to capture screenshots manually or modify the capture scripts to use different tools.

**Q: How do I customize the announcement style?**

A: Edit the instructions in `.claude/skills/create-changelog/`. You can change tone, length, format, and even add custom announcement channels.

## Need Help?

Visit the project repository for detailed setup guides and troubleshooting:
- GitHub: https://github.com/maxberko/max-doc-ai
- Documentation: `/docs` folder in the repository
- Issues: https://github.com/maxberko/max-doc-ai/issues

For questions about Claude Code itself:
- Claude Code docs: https://docs.anthropic.com/claude/docs/claude-code
