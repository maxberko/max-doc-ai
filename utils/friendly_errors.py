#!/usr/bin/env python3
"""
Friendly Error Handler

Catches common errors and provides helpful, actionable guidance to users.
"""

import sys
from pathlib import Path

class FriendlyError(Exception):
    """Base class for friendly errors"""
    def __init__(self, message, fix_hint=None, docs_link=None):
        self.message = message
        self.fix_hint = fix_hint
        self.docs_link = docs_link
        super().__init__(message)

    def print_friendly(self):
        """Print a friendly error message"""
        print(f"\n❌ {self.message}\n")
        if self.fix_hint:
            print(f"💡 How to fix:")
            for line in self.fix_hint.split('\n'):
                print(f"   {line}")
            print()
        if self.docs_link:
            print(f"📚 Learn more: {self.docs_link}\n")


class ConfigNotFoundError(FriendlyError):
    """Config file not found"""
    def __init__(self):
        super().__init__(
            message="Configuration file (config.yaml) not found",
            fix_hint="""Run the interactive setup wizard:
   python3 scripts/setup.py

Or copy the example config:
   cp config.example.yaml config.yaml
   # Then edit config.yaml with your settings""",
            docs_link="GETTING_STARTED.md"
        )


class EnvFileNotFoundError(FriendlyError):
    """Environment file not found"""
    def __init__(self):
        super().__init__(
            message="Environment file (.env) not found",
            fix_hint="""Run the interactive setup wizard:
   python3 scripts/setup.py

Or create .env manually:
   # Create .env with your API keys
   echo 'PYLON_API_KEY=your-key' > .env
   echo 'PYLON_KB_ID=your-kb-id' >> .env""",
            docs_link="GETTING_STARTED.md#configuration"
        )


class InvalidConfigError(FriendlyError):
    """Config file has errors"""
    def __init__(self, detail):
        super().__init__(
            message=f"Configuration file has errors: {detail}",
            fix_hint="""Check your config.yaml for syntax errors:
   python3 -c "import yaml; yaml.safe_load(open('config.yaml'))"

Or run the setup wizard to recreate it:
   python3 scripts/setup.py""",
            docs_link="GETTING_STARTED.md#configuration"
        )


class ProviderNotConfiguredError(FriendlyError):
    """KB provider not configured"""
    def __init__(self, provider=None):
        msg = "Knowledge base provider not configured"
        if provider:
            msg = f"Provider '{provider}' not configured in config.yaml"

        super().__init__(
            message=msg,
            fix_hint="""Run the setup wizard to configure your KB provider:
   python3 scripts/setup.py

Or add provider manually to config.yaml:
   knowledge_base:
     provider: "pylon"
     providers:
       pylon:
         api_key: "${PYLON_API_KEY}"
         # ... more settings""",
            docs_link="KB_PROVIDERS.md"
        )


class ProviderConnectionError(FriendlyError):
    """Cannot connect to KB provider"""
    def __init__(self, provider, detail=None):
        msg = f"Cannot connect to {provider}"
        if detail:
            msg = f"{msg}: {detail}"

        super().__init__(
            message=msg,
            fix_hint=f"""Check your {provider} credentials:
   1. Verify API key is correct in .env
   2. Check network connectivity
   3. Confirm {provider} service is accessible

Test the connection:
   python3 scripts/health_check.py

Or reconfigure:
   python3 scripts/setup.py""",
            docs_link="GETTING_STARTED.md#troubleshooting"
        )


class DocumentNotFoundError(FriendlyError):
    """Documentation file not found"""
    def __init__(self, filepath):
        super().__init__(
            message=f"Documentation file not found: {filepath}",
            fix_hint="""Check the file path is correct:
   ls -la {path}

Discover available documentation:
   python3 scripts/kb/sync.py discover

Or create the documentation first:
   claude "Create documentation for [feature]" """.format(path=Path(filepath).parent),
            docs_link="RELEASE_WORKFLOW_INTEGRATION.md"
        )


class SyncFailedError(FriendlyError):
    """Failed to sync to KB"""
    def __init__(self, reason=None):
        msg = "Failed to sync documentation to knowledge base"
        if reason:
            msg = f"{msg}: {reason}"

        super().__init__(
            message=msg,
            fix_hint="""Check sync status:
   python3 scripts/kb/sync.py status

Verify KB connection:
   python3 scripts/health_check.py

Try syncing again:
   python3 scripts/kb/sync.py sync --file [file] --key [key] --title [title] --slug [slug] --collection [category]""",
            docs_link="GETTING_STARTED.md#troubleshooting"
        )


class SkillNotRegisteredError(FriendlyError):
    """Skill not properly registered"""
    def __init__(self, skill_name):
        super().__init__(
            message=f"Skill '{skill_name}' is not registered or has errors",
            fix_hint="""Validate all skills:
   python3 utils/skill_validator.py

Check if skill is listed in .claude/settings.local.json:
   cat .claude/settings.local.json

Add skill to permissions if missing:
   "permissions": {{
     "allow": [
       "Skill({skill})",
       ...
     ]
   }}""".format(skill=skill_name),
            docs_link="GETTING_STARTED.md#troubleshooting"
        )


def handle_common_errors(func):
    """Decorator to catch and prettify common errors"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            if 'config.yaml' in str(e):
                error = ConfigNotFoundError()
            elif '.env' in str(e):
                error = EnvFileNotFoundError()
            else:
                error = DocumentNotFoundError(str(e))
            error.print_friendly()
            sys.exit(1)
        except ModuleNotFoundError as e:
            print(f"\n❌ Missing Python module: {e}\n")
            print(f"💡 Install required packages:")
            print(f"   pip install pyyaml requests markdown\n")
            sys.exit(1)
        except KeyError as e:
            if 'provider' in str(e) or 'knowledge_base' in str(e):
                error = ProviderNotConfiguredError()
                error.print_friendly()
                sys.exit(1)
            else:
                raise
        except ConnectionError as e:
            error = ProviderConnectionError("KB provider", str(e))
            error.print_friendly()
            sys.exit(1)
        except FriendlyError as e:
            e.print_friendly()
            sys.exit(1)
        except KeyboardInterrupt:
            print("\n\n⚠️  Operation cancelled by user\n")
            sys.exit(0)
        except Exception as e:
            # Unknown error - show it but also provide help
            print(f"\n❌ Unexpected error: {e}\n")
            print(f"💡 Try these steps:")
            print(f"   1. Run health check: python3 scripts/health_check.py")
            print(f"   2. Check your configuration: cat config.yaml")
            print(f"   3. Review logs for details")
            print(f"\n📚 If the issue persists, please report it:")
            print(f"   https://github.com/anthropics/max-doc-ai/issues\n")
            raise  # Re-raise for full traceback
    return wrapper


# Example usage in scripts:
"""
from utils.friendly_errors import handle_common_errors, ConfigNotFoundError

@handle_common_errors
def main():
    # Your code here
    if not config_exists():
        raise ConfigNotFoundError()

    # ... rest of code

if __name__ == '__main__':
    main()
"""
