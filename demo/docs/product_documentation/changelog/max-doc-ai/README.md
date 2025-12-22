# max-doc-ai Release

## Overview

**Feature:** max-doc-ai
**Category:** features
**Release Date:** 2025-12-22
**Target Audience:** Product teams, developer relations, technical writers, startups

## Description

max-doc-ai is an open-source framework that automates the complete product documentation workflow using Claude Code. It handles codebase research, screenshot capture, documentation generation, knowledge base sync, and multi-channel announcement creation in a single automated workflow.

## Key Capabilities

- Codebase-aware documentation with Claude Code analysis
- Automated screenshot capture using Playwright
- Pylon KB integration with CDN hosting
- Multi-channel announcement generation (Slack, Email)
- Complete release workflow orchestration
- State management for sync operations

## URLs

**Repository:** https://github.com/maxberko/max-doc-ai
**Documentation:** [Pylon public URL - would be set after successful sync]
**Internal docs:** [Pylon internal URL - would be set after successful sync]

## Announcement Files

- ✅ `slack-announcement.md` - Slack channel announcement
- ✅ `email-announcement.md` - Email newsletter announcement
- ✅ `README.md` - This file with release metadata

## Release Checklist

### Pre-Release
- [x] Documentation reviewed and approved
- [x] Feature fully tested (dry run completed)
- [x] Announcement copy created
- [ ] Pylon credentials configured for production sync
- [ ] Support/community briefed on new tool

### Distribution
- [ ] Post to relevant Slack channels
- [ ] Share in Claude Code community
- [ ] Publish to social media (Twitter, LinkedIn)
- [ ] Submit to relevant newsletters/communities
- [ ] Update main repository README

### Post-Release
- [ ] Monitor GitHub issues and discussions
- [ ] Track repository stars and forks
- [ ] Document common questions for FAQ
- [ ] Plan improvements based on feedback
- [ ] Create example workflows/tutorials

## Technical Details

**Documentation file:** `demo/docs/product_documentation/features/max-doc-ai.md`
**Screenshots:** N/A (CLI tool without UI)
**Database changes:** N/A
**Feature flags:** N/A

## Skills Included

1. **create-release** - Master orchestrator for complete workflow
2. **capture-screenshots** - Playwright-based screenshot automation
3. **update-product-doc** - Documentation generation
4. **sync-docs** - Pylon KB integration (upload & sync modes)
5. **create-changelog** - Multi-channel announcement generation

## Notes

### About This Release

This is a dry run/demonstration of the max-doc-ai release workflow running on itself. The workflow successfully:
- Researched the max-doc-ai codebase
- Generated comprehensive documentation (385 lines)
- Created Slack and email announcements
- Attempted Pylon sync (failed due to unconfigured credentials, as expected)

### Configuration Required for Production

To use in production:
1. Set valid `PYLON_API_KEY` in `.env`
2. Configure `PYLON_KB_ID` and collection IDs
3. Save authentication session for screenshot capture
4. Update product URLs in `config.yaml`

### Customization Notes

The conversational flow in create-release was recently updated to use simple text prompts instead of complex multi-select questions, making it faster and more intuitive.
