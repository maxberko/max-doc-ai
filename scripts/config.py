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
