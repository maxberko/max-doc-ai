# Pull Request: Add Google Gemini Support & Playwright Privacy Mode

## Description
This PR introduces support for Google's Gemini models (via `google-generativeai`) as an alternative provider for the "Computer Use" functionality. Additionally, it integrates a "Privacy-First" Playwright capture mode as a selectable provider.

## Changes
- **New Gemini Adapter**: Added `scripts/screenshot/gemini_client.py` which implements the `ComputerUseClient` interface using Gemini's multimodal and function-calling capabilities.
- **Provider Selection System**: Updated `scripts/screenshot/factory.py` and `scripts/screenshot/computer_use_capture.py` to support a modular `provider` system. Supported providers: `anthropic`, `google` (Gemini), and `playwright`.
- **Playwright "Privacy" Mode**: Refactored the legacy Playwright capturer (`scripts/screenshot/capture.py`) to implement the `ScreenshotCapturerBase` interface. This allows users to opt for a headless, browser-only capture method that prevents desktop/private data leakage.
- **Configuration**:
    - Added `GOOGLE_API_KEY` support in `config.py`.
    - Updated `config.yaml` to allow specifying the provider and model.
- **Improved Robustness**:
    - Fixed encoding issues in `skill_validator.py` for Windows environments (UTF-8).
    - Added missing required legacy keys in `config.yaml` to prevent startup crashes.

## How to Test
1. Set `GOOGLE_API_KEY` in your `.env`.
2. Update `config.yaml` with:
   ```yaml
   screenshots:
     provider: "google"
     model: "gemini-2.5-flash"
   ```
   Or for Playwright:
   ```yaml
   screenshots:
     provider: "playwright"
   ```
3. Run `python scripts/demo_gemini_doc.py` or your standard documentation workflow.

## Advantages
- **Privacy & Security**: Headless Playwright mode ensures no background desktop content is accidentally captured.
- **Cost Efficiency**: Gemini 2.5 Flash is significantly more cost-effective for high-frequency documentation updates.
- **Flexibility**: Users can now choose their preferred AI provider and capture method based on their needs.
