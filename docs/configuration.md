# Configuration Reference

Complete reference for all configuration options in max-doc-AI.

## Configuration Files

### config.yaml

Main configuration file for all settings.

### .env

Environment variables for sensitive data (API keys, IDs, credentials).

## Configuration Schema

### Product Section

```yaml
product:
  name: "YourProduct"
  url: "https://app.yourproduct.com"
  documentation_url: "https://docs.yourproduct.com"
```

**Options:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Product name for documentation |
| `url` | string | Yes | Base URL for screenshot capture |
| `documentation_url` | string | No | Public documentation site URL |

### Pylon Section

```yaml
pylon:
  api_key: "${PYLON_API_KEY}"
  kb_id: "${PYLON_KB_ID}"
  author_user_id: "${PYLON_AUTHOR_ID}"
  api_base: "https://api.usepylon.com"
  collections:
    getting-started: "${COLLECTION_GETTING_STARTED_ID}"
    features: "${COLLECTION_FEATURES_ID}"
    integrations: "${COLLECTION_INTEGRATIONS_ID}"
```

**Options:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `api_key` | string | Yes | Pylon API key (from env var) |
| `kb_id` | string | Yes | Knowledge Base ID |
| `author_user_id` | string | Yes | Pylon user ID for article attribution |
| `api_base` | string | Yes | Pylon API base URL (default shown) |
| `collections` | map | Yes | Mapping of category names to collection IDs |

**Collection IDs:**
- Must match categories in `documentation.categories`
- Get IDs from Pylon web UI (in URL when viewing collection)
- Referenced via environment variables for security

### Screenshots Section

```yaml
screenshots:
  viewport_width: 1280
  viewport_height: 800
  output_dir: "./output/screenshots"
  format: "png"
  quality: 90

  model: "claude-sonnet-4-5"
  max_iterations: 50

  auth:
    enabled: true
    type: "sso"  # or "username_password"
    login_url: "${PRODUCT_URL}/login"
    username: "${SCREENSHOT_USER}"
    password: "${SCREENSHOT_PASS}"
    sso_provider: "google"

    mfa:
      enabled: false
      type: "totp"
      totp_secret: "${TOTP_SECRET}"
```

**Options:**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `viewport_width` | integer | No | 1280 | Display width in pixels (≤1280 recommended) |
| `viewport_height` | integer | No | 800 | Display height in pixels (≤800 recommended) |
| `output_dir` | string | Yes | - | Where to save screenshots |
| `format` | string | No | png | Image format (png, jpg) |
| `quality` | integer | No | 90 | JPEG quality (1-100) |
| `model` | string | No | claude-sonnet-4-5 | Claude model for Computer Use |
| `max_iterations` | integer | No | 50 | Max iterations for Computer Use tasks |

**Auth Options:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `enabled` | boolean | Yes | Enable authentication |
| `type` | string | Yes | Authentication type: "sso" or "username_password" |
| `login_url` | string | Yes | Login page URL |
| `username` | string | Yes | Username/email (from env var) |
| `password` | string | Yes | Password (from env var) |
| `sso_provider` | string | No | SSO provider: "google", "microsoft", etc. |

**MFA Options:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `enabled` | boolean | Yes | Enable MFA support |
| `type` | string | No | MFA type: "totp" |
| `totp_secret` | string | No | TOTP secret (from env var) |

**Notes:**
- Viewport size ≤1280x800 recommended for Computer Use coordinate accuracy
- Computer Use handles authentication automatically via visual login
- No cookie management or session files needed
- Credentials stored securely in .env file
- Cost: ~$0.02 per screenshot with Claude Sonnet 4.5

### Documentation Section

```yaml
documentation:
  base_path: "./demo/docs/product_documentation"
  categories:
    - getting-started
    - features
    - integrations
  include_console_urls: true
```

**Options:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `base_path` | string | Yes | Root directory for documentation |
| `categories` | array | Yes | List of documentation categories |
| `include_console_urls` | boolean | No | Add product URLs in docs |

**Categories:**
- Must have matching Pylon collections
- Create subdirectories under `base_path`
- Category names used in file paths and Pylon

### Announcements Section

```yaml
announcements:
  output_dir: "./demo/docs/product_documentation/changelog"
  channels:
    - slack
    - email
  batch_mode_enabled: true
```

**Options:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `output_dir` | string | Yes | Where to save announcement files |
| `channels` | array | Yes | Which announcement types to generate |
| `batch_mode_enabled` | boolean | No | Support multiple features in one changelog |

**Channels:**
- `slack` - Short announcement for Slack
- `email` - Longer announcement for email

### State Section

```yaml
state:
  sync_state_file: "./demo/docs/sync-state.json"
```

**Options:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `sync_state_file` | string | Yes | Path to Pylon sync state tracker |

## Environment Variables

Set in `.env` file:

```bash
# Pylon API
PYLON_API_KEY=pylon_api_xxxxx
PYLON_KB_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
PYLON_AUTHOR_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# Collections
COLLECTION_GETTING_STARTED_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
COLLECTION_FEATURES_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
COLLECTION_INTEGRATIONS_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

**Variable Substitution:**

In `config.yaml`, use `${VAR_NAME}` to reference environment variables:
```yaml
api_key: "${PYLON_API_KEY}"
```

The config loader automatically substitutes these at runtime.

## Adding New Categories

To add a new documentation category:

1. **Create Pylon Collection:**
   - Go to Pylon web UI
   - Create new collection
   - Copy collection ID

2. **Add to .env:**
   ```bash
   COLLECTION_NEW_CATEGORY_ID=your-collection-id
   ```

3. **Add to config.yaml:**
   ```yaml
   pylon:
     collections:
       new-category: "${COLLECTION_NEW_CATEGORY_ID}"

   documentation:
     categories:
       - new-category
   ```

4. **Create Directory:**
   ```bash
   mkdir -p demo/docs/product_documentation/new-category
   ```

5. **Use in Skills:**
   ```
   @claude Skill: update-product-doc
   Category: new-category
   ```

## Configuration Validation

Test your configuration:

```bash
# Validate config loads correctly
python3 scripts/config.py

# Check Pylon connection
python3 scripts/pylon/upload.py

# Verify state file
python3 scripts/utils/state.py --summary
```

**Expected output:**
- No errors when loading config
- Pylon API responds (not 401)
- State file initializes

## Best Practices

1. **Use Environment Variables for Secrets:** Never hardcode API keys in `config.yaml`
2. **Keep Viewport Consistent:** Same dimensions across all screenshots
3. **Organize Categories Logically:** Group related documentation
4. **Document Custom Settings:** Add comments in `config.yaml`
5. **Backup State File:** Track which articles are synced
6. **Test Configuration Changes:** Run validation commands after changes

## Troubleshooting

**Config Not Found:**
```bash
cp config.example.yaml config.yaml
```

**Environment Variable Not Set:**
- Check `.env` file exists
- Verify variable name matches exactly
- No spaces around `=`

**Collection ID Invalid:**
- Check ID format (UUID)
- Verify collection exists in Pylon
- Copy from Pylon URL (not collection name)

**Path Issues:**
- Use relative paths (`./`) or absolute paths
- Ensure directories exist
- Check file permissions

## Example Configurations

### Minimal Configuration

```yaml
product:
  name: "MyApp"
  url: "https://app.myapp.com"

pylon:
  api_key: "${PYLON_API_KEY}"
  kb_id: "${PYLON_KB_ID}"
  author_user_id: "${PYLON_AUTHOR_ID}"
  collections:
    features: "${COLLECTION_FEATURES_ID}"

documentation:
  base_path: "./docs"
  categories:
    - features
```

### Full Configuration

See `config.example.yaml` for complete example with all options.

## Next Steps

- [Usage Guide](usage.md) - Learn how to use the skills
- [Pylon Integration](pylon-integration.md) - Deep dive on Pylon
- [Setup Guide](setup.md) - Initial setup instructions
