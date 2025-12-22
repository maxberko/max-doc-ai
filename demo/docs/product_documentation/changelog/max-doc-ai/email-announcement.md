# Introducing max-doc-ai: Your Documentation Workflow, Automated

Hello,

We're excited to share max-doc-ai, an open-source framework that automates your entire product documentation workflow using Claude Code. If you've ever spent hours writing documentation, capturing screenshots, or creating release announcements, this is for you.

## What is max-doc-ai?

max-doc-ai is a collection of five Claude Code skills that work together to handle everything from codebase research to published documentation. Point it at your repository, answer a few simple questions, and watch as it researches your features, captures screenshots, writes comprehensive documentation, syncs to your knowledge base, and generates multi-channel announcements—all in a single automated workflow.

## Key Capabilities

**Codebase-Aware Documentation**
Instead of manually researching how features work, Claude explores your code to understand implementation details, user flows, and configuration options. This ensures your documentation accurately reflects what you actually built, not what you thought you built.

**Automated Screenshot Capture**
Using Playwright browser automation with saved authentication sessions, max-doc-ai captures consistent, professional screenshots at configurable viewport sizes. No more manually clicking through your product and taking screenshots one by one.

**Knowledge Base Integration**
Direct integration with Pylon KB handles the entire publishing workflow: uploads screenshots to CDN, converts markdown to HTML with required React wrappers, creates or updates articles with proper collection assignment, and returns public URLs for sharing.

**Multi-Channel Announcements**
Automatically generates channel-specific content: short, engaging Slack messages (15-25 lines with emojis) and detailed, professional email announcements (40-60 lines)—both linking to your published documentation.

**Complete Release Workflow**
The create-release skill orchestrates everything: research, screenshots, upload, documentation, sync, and announcements. One command runs the entire process from start to finish without stopping.

**State Management**
Tracks which articles exist in your knowledge base to prevent duplicates and enable updates. Since Pylon doesn't provide a "list all articles" endpoint, max-doc-ai maintains its own state file for reliable sync operations.

## Who Should Use This?

max-doc-ai is perfect for product teams and developer relations who ship features frequently and need documentation to keep pace. Whether you're a startup maintaining professional docs without dedicated writers, a technical writer accelerating content creation, or a product manager ensuring releases include complete documentation, max-doc-ai reduces documentation time from hours to minutes.

## Technical Highlights

Built on Claude Code with Python scripts for API integrations and browser automation, max-doc-ai demonstrates sophisticated integration patterns. It uses the Explore agent for codebase research, Playwright for screenshot capture, Pylon's Attachments API for CDN hosting, and handles Pylon's specific requirements like React image wrappers and collection ID assignment during article creation.

## Getting Started

Ready to automate your documentation workflow?

1. Clone the repository: `git clone https://github.com/maxberko/max-doc-ai.git`
2. Install dependencies: `pip install -r requirements.txt && playwright install chromium`
3. Configure your Pylon credentials and product settings
4. Run `/create-release` in Claude Code

The framework includes example documentation, detailed setup guides, and five production-ready skills you can use as-is or customize for your workflow.

For detailed installation instructions, configuration reference, and usage examples, check out our [documentation](https://github.com/maxberko/max-doc-ai).

## What's Next?

max-doc-ai is open source and actively maintained. We're exploring integrations with additional knowledge base platforms, enhanced screenshot capture capabilities, and improved codebase analysis patterns. Have suggestions or want to contribute? Open an issue or pull request on GitHub.

---

Best regards,
The max-doc-ai Team

**Repository:** https://github.com/maxberko/max-doc-ai
**Documentation:** [Documentation URL]
