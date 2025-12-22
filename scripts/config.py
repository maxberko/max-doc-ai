"""
Configuration loader for max-doc-AI

Loads configuration from config.yaml and environment variables.
Environment variables take precedence over YAML values.
"""

import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_config(config_path='config.yaml'):
    """
    Load configuration from YAML file with environment variable substitution

    Args:
        config_path: Path to config.yaml file (default: 'config.yaml' in project root)

    Returns:
        dict: Configuration dictionary
    """
    # Default to project root if relative path
    if not os.path.isabs(config_path):
        project_root = Path(__file__).parent.parent
        config_path = project_root / config_path

    # Load YAML config
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}\n"
            f"Please copy config.example.yaml to config.yaml and configure it."
        )

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Substitute environment variables
    config = _substitute_env_vars(config)

    return config


def _substitute_env_vars(obj):
    """
    Recursively substitute ${ENV_VAR} placeholders with environment variable values

    Args:
        obj: Config object (dict, list, string, etc.)

    Returns:
        Object with environment variables substituted
    """
    if isinstance(obj, dict):
        return {key: _substitute_env_vars(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [_substitute_env_vars(item) for item in obj]
    elif isinstance(obj, str):
        # Replace ${VAR_NAME} with environment variable value
        if obj.startswith('${') and obj.endswith('}'):
            var_name = obj[2:-1]
            value = os.getenv(var_name)
            if value is None:
                raise ValueError(
                    f"Environment variable '{var_name}' is not set.\n"
                    f"Please set it in your .env file or environment."
                )
            return value
        return obj
    else:
        return obj


# Load configuration on module import
try:
    CONFIG = load_config()
except FileNotFoundError:
    # Config file doesn't exist - user needs to create it
    CONFIG = None
    print("⚠️  Warning: config.yaml not found. Please copy config.example.yaml to config.yaml")


def get_config():
    """Get the loaded configuration"""
    if CONFIG is None:
        raise RuntimeError(
            "Configuration not loaded. Please create config.yaml from config.example.yaml"
        )
    return CONFIG


# Convenience accessors for common config values
def get_product_name():
    """Get product name from config"""
    return get_config()['product']['name']


def get_product_url():
    """Get product URL from config"""
    return get_config()['product']['url']


def get_pylon_config():
    """Get Pylon configuration"""
    return get_config()['pylon']


def get_screenshot_config():
    """Get screenshot configuration"""
    return get_config()['screenshots']


def get_documentation_config():
    """Get documentation configuration"""
    return get_config()['documentation']


def get_announcements_config():
    """Get announcements configuration"""
    return get_config()['announcements']


def get_anthropic_api_key():
    """
    Get Anthropic API key for Computer Use

    Checks in order:
    1. Environment variable ANTHROPIC_API_KEY
    2. Screenshots config

    Returns:
        str: API key or None if not found
    """
    # Check environment first
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if api_key:
        return api_key

    # Fall back to config
    try:
        screenshot_config = get_screenshot_config()
        return screenshot_config.get('api_key')
    except:
        return None


def get_output_config():
    """Get output configuration with defaults"""
    config = get_config()
    output_config = config.get('output', {})

    # Defaults
    defaults = {
        'base_dir': './output',
        'use_dated_folders': True,
        'features_template': 'features/{date}_{feature_slug}',
        'changelogs_template': 'changelogs/{date}',
        'screenshots_template': 'screenshots',
        'legacy_mode': False,
        'legacy_base': './demo/docs/product_documentation'
    }

    # Merge with defaults
    for key, value in defaults.items():
        if key not in output_config:
            output_config[key] = value

    return output_config


def build_output_path(
    path_type: str,
    release_date: str,
    feature_slug: str = None
) -> str:
    """
    Build output path based on configuration

    Args:
        path_type: 'features' | 'changelogs' | 'screenshots'
        release_date: Release date in YYYY-MM-DD format
        feature_slug: Feature slug (required for features)

    Returns:
        Absolute path to output directory
    """
    output_config = get_output_config()

    # Check legacy mode
    if output_config['legacy_mode']:
        base = output_config['legacy_base']
        if path_type == 'features':
            return os.path.join(base, 'features')
        elif path_type == 'changelogs':
            if feature_slug:
                return os.path.join(base, 'changelog', feature_slug)
            else:
                return os.path.join(base, 'changelog')
        elif path_type == 'screenshots':
            return os.path.join(base, 'screenshots')

    # New structure
    base = output_config['base_dir']

    if path_type == 'features':
        if not feature_slug:
            raise ValueError("feature_slug required for features path")
        template = output_config['features_template']
        path = template.format(date=release_date, feature_slug=feature_slug)
    elif path_type == 'changelogs':
        template = output_config['changelogs_template']
        path = template.format(date=release_date)
    elif path_type == 'screenshots':
        template = output_config['screenshots_template']
        path = template
    else:
        raise ValueError(f"Unknown path_type: {path_type}")

    full_path = os.path.join(base, path)

    # Convert to absolute path
    if not os.path.isabs(full_path):
        project_root = Path(__file__).parent.parent
        full_path = project_root / full_path

    return str(full_path)


# Module-level constants for backward compatibility
if CONFIG:
    PRODUCT_NAME = CONFIG['product']['name']
    PRODUCT_URL = CONFIG['product']['url']

    PYLON_API_KEY = CONFIG['pylon']['api_key']
    PYLON_KB_ID = CONFIG['pylon']['kb_id']
    PYLON_API_BASE = CONFIG['pylon']['api_base']
    PYLON_AUTHOR_ID = CONFIG['pylon']['author_user_id']
    PYLON_COLLECTIONS = CONFIG['pylon']['collections']

    SCREENSHOT_VIEWPORT_WIDTH = CONFIG['screenshots']['viewport_width']
    SCREENSHOT_VIEWPORT_HEIGHT = CONFIG['screenshots']['viewport_height']
    SCREENSHOT_OUTPUT_DIR = CONFIG['screenshots']['output_dir']
    SCREENSHOT_AUTH_FILE = CONFIG['screenshots']['auth_session_file']

    DOCS_BASE_PATH = CONFIG['documentation']['base_path']
    DOCS_CATEGORIES = CONFIG['documentation']['categories']

    ANNOUNCEMENTS_OUTPUT_DIR = CONFIG['announcements']['output_dir']
    ANNOUNCEMENTS_CHANNELS = CONFIG['announcements']['channels']
