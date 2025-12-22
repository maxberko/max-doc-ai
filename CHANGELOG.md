# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Support for additional CDN providers (Cloudinary, S3)
- Additional announcement channels (Discord, Teams)
- Video recording support for demo workflows
- Multi-language documentation support
- Versioned documentation per release
- Integration with other knowledge bases (Notion, GitBook, Confluence)

## [1.0.0] - 2024-12-22

### Added
- Initial release of max-doc-AI
- 5 integrated Claude Code skills:
  - `create-release` - Master orchestrator for complete release workflow
  - `capture-screenshots` - Automated screenshot capture with Playwright
  - `update-product-doc` - AI-generated documentation from codebase
  - `sync-docs` - Upload to Pylon CDN and sync to knowledge base
  - `create-changelog` - Generate customer announcements (Slack/Email)
- Python scripts for core functionality:
  - Pylon API integration (upload, sync, conversion)
  - Screenshot capture with authentication
  - State tracking for synced articles
  - Configuration management
- Comprehensive documentation:
  - Complete setup guide with troubleshooting
  - Detailed usage guide for all skills
  - Configuration reference
  - Pylon integration technical guide
  - Demo product documentation (FlowState)
  - Contributing guidelines
- Demo content:
  - FlowState fictional product documentation
  - Example feature documentation (Dashboards)
  - Example announcements (Slack and Email)
  - Complete workflow demonstration
- GitHub templates:
  - Bug report template
  - Feature request template
  - Documentation issue template
  - Pull request template
- GNU General Public License v3.0
- Professional README with badges and quick start
- Example configuration files (config.example.yaml, .env.example)

### Features
- Automated browser screenshot capture with saved authentication
- Markdown to HTML conversion with React component wrappers
- Multi-channel announcement generation
- State tracking to prevent duplicate articles
- Collection-based organization in Pylon
- CloudFront CDN for screenshot hosting
- Codebase research for accurate documentation

### Documentation
- 5 comprehensive markdown guides (setup, usage, configuration, Pylon, demo)
- Inline code documentation and docstrings
- Troubleshooting sections for common issues
- Real-world use case examples
- Best practices and tips throughout

### Developer Experience
- Virtual environment support
- Clear error messages with emojis
- Idempotent operations (safe to re-run)
- Modular Python scripts
- Example demo content for reference

---

## Release Types

This project uses [Semantic Versioning](https://semver.org/):

- **MAJOR** version (X.0.0) - Incompatible API changes
- **MINOR** version (0.X.0) - New functionality, backwards compatible
- **PATCH** version (0.0.X) - Bug fixes, backwards compatible

## Change Categories

- **Added** - New features
- **Changed** - Changes to existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Removed features
- **Fixed** - Bug fixes
- **Security** - Security improvements
