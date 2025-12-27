#!/usr/bin/env python3
"""
Interactive Setup Wizard for max-doc-ai

Guides first-time users through configuration with a friendly, step-by-step process.
"""

import os
import sys
import subprocess
from pathlib import Path
import yaml
import json

# Add project root to path (must be first for utils/ imports)
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Colors for terminal output
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    """Print a section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}")
    print(f"{text.center(70)}")
    print(f"{'='*70}{Colors.END}\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

def ask_question(question, default=None, options=None):
    """Ask user a question"""
    if options:
        print(f"\n{Colors.BOLD}{question}{Colors.END}")
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
        while True:
            answer = input(f"\n{Colors.BOLD}→{Colors.END} Enter number (1-{len(options)}): ").strip()
            try:
                idx = int(answer) - 1
                if 0 <= idx < len(options):
                    return options[idx]
            except ValueError:
                pass
            print_error(f"Please enter a number between 1 and {len(options)}")
    else:
        default_text = f" [{default}]" if default else ""
        answer = input(f"\n{Colors.BOLD}{question}{default_text}\n→{Colors.END} ").strip()
        return answer if answer else default

def check_file_exists(filepath):
    """Check if a file exists"""
    return Path(filepath).exists()

def check_command_exists(command):
    """Check if a command exists in PATH"""
    try:
        subprocess.run([command, '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def welcome_screen():
    """Display welcome screen"""
    print(f"""
{Colors.BOLD}{Colors.BLUE}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║              Welcome to max-doc-ai Setup! 👋                      ║
║                                                                   ║
║   Let's get you up and running in just a few minutes.           ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.END}

{Colors.BOLD}What is max-doc-ai?{Colors.END}

max-doc-ai automates your product documentation workflow:
  • 📸 Capture product screenshots automatically
  • 📝 Generate comprehensive documentation
  • 🔄 Sync to your knowledge base (Pylon, Zendesk, etc.)
  • 📣 Create customer announcements

{Colors.BOLD}This wizard will:{Colors.END}
  1. Check your system requirements
  2. Help you choose a knowledge base provider
  3. Set up your configuration
  4. Verify everything works
  5. Show you how to create your first release

{Colors.GREEN}Let's get started!{Colors.END}
""")
    input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.END}")

def check_system_requirements():
    """Check system requirements"""
    print_header("Step 1: System Requirements Check")

    requirements = {
        'Python 3.8+': sys.version_info >= (3, 8),
        'Git': check_command_exists('git'),
    }

    all_good = True
    for name, passed in requirements.items():
        if passed:
            print_success(f"{name} installed")
        else:
            print_error(f"{name} not found")
            all_good = False

    if not all_good:
        print_warning("\nSome requirements are missing. Please install them and run setup again.")
        print_info("Visit https://github.com/anthropics/max-doc-ai for installation instructions")
        sys.exit(1)

    print_success("\n✨ All system requirements met!")

def choose_kb_provider():
    """Help user choose a knowledge base provider"""
    print_header("Step 2: Choose Your Knowledge Base")

    print("""
Where do you publish your product documentation?

We support multiple knowledge base platforms. Choose the one you use:
""")

    providers = {
        "Pylon": {
            "description": "Modern KB with React components",
            "difficulty": "Easy",
            "features": "Great UI, React support, CloudFront CDN"
        },
        "Zendesk Guide": {
            "description": "Zendesk's help center platform",
            "difficulty": "Easy",
            "features": "Multi-locale, sections, tight Zendesk integration"
        },
        "I don't have one yet": {
            "description": "We'll help you set one up",
            "difficulty": "Easy",
            "features": "We recommend starting with Pylon (free tier available)"
        },
        "Other / I'll configure manually": {
            "description": "Use config.yaml directly",
            "difficulty": "Advanced",
            "features": "Full control over configuration"
        }
    }

    for i, (name, info) in enumerate(providers.items(), 1):
        print(f"{Colors.BOLD}{i}. {name}{Colors.END}")
        print(f"   {info['description']}")
        print(f"   {Colors.BLUE}Difficulty: {info['difficulty']}{Colors.END}")
        print(f"   Features: {info['features']}\n")

    while True:
        choice = input(f"{Colors.BOLD}→{Colors.END} Enter number (1-{len(providers)}): ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(providers):
                return list(providers.keys())[idx]
        except ValueError:
            pass
        print_error(f"Please enter a number between 1 and {len(providers)}")

def setup_pylon():
    """Interactive Pylon setup"""
    print_header("Pylon Setup")

    print("""
{Colors.BOLD}Setting up Pylon Knowledge Base{Colors.END}

Pylon is a modern knowledge base platform perfect for product documentation.

{Colors.BOLD}What you'll need:{Colors.END}
  1. A Pylon account (sign up at https://usepylon.com)
  2. API key (from Pylon settings)
  3. Knowledge Base ID
  4. Collection IDs for your documentation categories

{Colors.BLUE}Don't have a Pylon account?{Colors.END}
  → Visit https://usepylon.com to sign up (free tier available)
  → Create your first knowledge base
  → Come back here when ready!
""")

    has_account = ask_question("Do you have a Pylon account set up?", options=["Yes", "No, I'll set it up now", "Skip for now"])

    if has_account == "No, I'll set it up now":
        print_info("\n📋 Opening Pylon signup in your browser...")
        print_info("Come back here after you've created your knowledge base!")
        input(f"\n{Colors.BOLD}Press Enter when ready to continue...{Colors.END}")
    elif has_account == "Skip for now":
        print_warning("\nSkipping Pylon setup. You can configure it later in config.yaml")
        return None

    print(f"\n{Colors.BOLD}Let's collect your Pylon credentials:{Colors.END}\n")

    config = {}

    # API Key
    print(f"{Colors.BLUE}1. API Key{Colors.END}")
    print("   Get this from: https://app.usepylon.com/settings/api-keys")
    config['api_key'] = ask_question("Paste your Pylon API key:")

    # KB ID
    print(f"\n{Colors.BLUE}2. Knowledge Base ID{Colors.END}")
    print("   Find this in your Pylon KB settings URL")
    config['kb_id'] = ask_question("Paste your Knowledge Base ID:")

    # Author ID
    print(f"\n{Colors.BLUE}3. Author User ID{Colors.END}")
    print("   Find this in your Pylon user settings")
    config['author_user_id'] = ask_question("Paste your User ID:")

    # Collections
    print(f"\n{Colors.BLUE}4. Collections{Colors.END}")
    print("   Collections organize your documentation")
    print("   We recommend: getting-started, features, integrations")

    collections = {}
    for category in ['getting-started', 'features', 'integrations']:
        coll_id = ask_question(f"Collection ID for '{category}' (or press Enter to skip):")
        if coll_id:
            collections[category] = coll_id

    config['collections'] = collections
    config['api_base'] = 'https://api.usepylon.com'

    return config

def setup_zendesk():
    """Interactive Zendesk setup"""
    print_header("Zendesk Guide Setup")

    print("""
{Colors.BOLD}Setting up Zendesk Guide{Colors.END}

{Colors.BOLD}What you'll need:{Colors.END}
  1. Zendesk subdomain (e.g., 'mycompany' for mycompany.zendesk.com)
  2. Admin email
  3. API token
  4. Section IDs for your documentation categories
""")

    config = {}

    config['subdomain'] = ask_question("Your Zendesk subdomain:")
    config['email'] = ask_question("Admin email:")
    config['api_token'] = ask_question("API token:")
    config['locale'] = ask_question("Default locale:", default="en-us")

    # Sections
    print(f"\n{Colors.BLUE}Section IDs (categories):{Colors.END}")
    categories = {}
    for category in ['getting-started', 'features', 'integrations']:
        section_id = ask_question(f"Section ID for '{category}' (or press Enter to skip):")
        if section_id:
            categories[category] = section_id

    config['categories'] = categories

    return config

def create_config_file(provider, provider_config):
    """Create config.yaml file"""
    print_header("Step 3: Creating Configuration")

    # Load example config
    example_config_path = Path(__file__).parent.parent / 'config.example.yaml'

    if example_config_path.exists():
        with open(example_config_path, 'r') as f:
            config = yaml.safe_load(f)
    else:
        config = {}

    # Set up knowledge_base section
    if provider and provider_config:
        if 'knowledge_base' not in config:
            config['knowledge_base'] = {}

        config['knowledge_base']['provider'] = provider.lower().replace(' ', '_').replace('guide', '').strip()

        if 'providers' not in config['knowledge_base']:
            config['knowledge_base']['providers'] = {}

        config['knowledge_base']['providers'][config['knowledge_base']['provider']] = provider_config

    # Create .env file for secrets
    env_path = Path(__file__).parent.parent / '.env'
    env_vars = []

    if provider == "Pylon" and provider_config:
        env_vars.extend([
            f"PYLON_API_KEY={provider_config.get('api_key', '')}",
            f"PYLON_KB_ID={provider_config.get('kb_id', '')}",
            f"PYLON_AUTHOR_ID={provider_config.get('author_user_id', '')}",
        ])
        for name, coll_id in provider_config.get('collections', {}).items():
            var_name = f"COLLECTION_{name.upper().replace('-', '_')}_ID"
            env_vars.append(f"{var_name}={coll_id}")

    # Write .env file
    if env_vars:
        with open(env_path, 'w') as f:
            f.write("# max-doc-ai Environment Variables\n")
            f.write("# Generated by setup wizard\n\n")
            f.write('\n'.join(env_vars))
        print_success(f"Created .env file with your credentials")

    # Update config to use env vars
    if provider == "Pylon" and provider_config:
        config['knowledge_base']['providers']['pylon']['api_key'] = '${PYLON_API_KEY}'
        config['knowledge_base']['providers']['pylon']['kb_id'] = '${PYLON_KB_ID}'
        config['knowledge_base']['providers']['pylon']['author_user_id'] = '${PYLON_AUTHOR_ID}'

        collections = {}
        for name in provider_config.get('collections', {}).keys():
            var_name = f"COLLECTION_{name.upper().replace('-', '_')}_ID"
            collections[name] = f"${{{var_name}}}"
        config['knowledge_base']['providers']['pylon']['collections'] = collections

    # Write config.yaml
    config_path = Path(__file__).parent.parent / 'config.yaml'
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    print_success(f"Created config.yaml")
    print_info(f"Config file: {config_path}")
    print_info(f"Secrets file: {env_path}")

def verify_setup():
    """Verify the setup works"""
    print_header("Step 4: Verification")

    print("Testing your configuration...\n")

    # Test config loading
    try:
        import config as cfg
        config_obj = cfg.get_config()
        print_success("Config file loads correctly")
    except Exception as e:
        print_error(f"Config file has errors: {e}")
        return False

    # Test KB provider connection
    try:
        kb_info = cfg.get_kb_config()
        provider_name = kb_info['provider']
        print_success(f"Knowledge base provider: {provider_name}")

        # Try to initialize provider
        from utils.kb_providers import get_provider

        provider = get_provider(provider_name, kb_info['config'])
        if provider:
            print_success(f"Provider '{provider_name}' initialized")

            # Test connection
            if provider.test_connection():
                print_success(f"✨ Connection to {provider_name} successful!")
            else:
                print_warning(f"Could not connect to {provider_name}")
                print_info("Check your API credentials and try again")
                return False
        else:
            print_error(f"Could not initialize provider '{provider_name}'")
            return False

    except Exception as e:
        print_warning(f"Could not test KB connection: {e}")
        print_info("You can test manually later with: python3 scripts/kb/sync.py status")

    return True

def show_next_steps():
    """Show next steps"""
    print_header("🎉 Setup Complete!")

    print(f"""
{Colors.GREEN}{Colors.BOLD}You're all set!{Colors.END} Here's what to do next:

{Colors.BOLD}1. Discover Your Documentation{Colors.END}
   See what documentation you already have:

   {Colors.BLUE}python3 scripts/kb/sync.py discover{Colors.END}

{Colors.BOLD}2. Check Sync Status{Colors.END}
   See what's synced to your knowledge base:

   {Colors.BLUE}python3 scripts/kb/sync.py status{Colors.END}

{Colors.BOLD}3. Create Your First Release{Colors.END}
   Let Claude create a complete release with docs:

   {Colors.BLUE}claude "Create a release for [your feature name]"{Colors.END}

{Colors.BOLD}4. Or Sync Existing Docs{Colors.END}
   Sync documentation you've already written:

   {Colors.BLUE}python3 scripts/kb/sync.py sync \\
     --file path/to/your/doc.md \\
     --key category-slug \\
     --title "Your Title" \\
     --slug "your-slug" \\
     --collection features{Colors.END}

{Colors.BOLD}📚 Learn More:{Colors.END}
   • Documentation: KB_PROVIDERS.md
   • Release workflow: RELEASE_WORKFLOW_INTEGRATION.md
   • Feature guide: NEW_FEATURES.md

{Colors.BOLD}💡 Pro Tips:{Colors.END}
   • Run health checks: {Colors.BLUE}python3 scripts/health_check.py{Colors.END}
   • Validate skills: {Colors.BLUE}python3 utils/skill_validator.py{Colors.END}
   • Export inventory: {Colors.BLUE}python3 utils/doc_inventory.py --export{Colors.END}

{Colors.GREEN}Happy documenting! 🚀{Colors.END}
""")

def main():
    """Main setup wizard"""
    try:
        # Welcome
        welcome_screen()

        # System check
        check_system_requirements()

        # Choose provider
        provider = choose_kb_provider()

        # Setup provider
        provider_config = None
        if provider == "Pylon":
            provider_config = setup_pylon()
        elif provider == "Zendesk Guide":
            provider_config = setup_zendesk()
        elif provider == "I don't have one yet":
            print_info("\nWe recommend Pylon for new users")
            setup_anyway = ask_question("Set up Pylon now?", options=["Yes", "No, skip for now"])
            if setup_anyway == "Yes":
                provider = "Pylon"
                provider_config = setup_pylon()

        # Create config
        if provider_config:
            create_config_file(provider, provider_config)

            # Verify
            if verify_setup():
                # Success!
                show_next_steps()
            else:
                print_warning("\nSetup completed but verification had issues")
                print_info("You can fix the configuration and test with:")
                print_info("  python3 scripts/kb/sync.py status")
        else:
            print_info("\nSetup skipped. You can run setup again anytime:")
            print_info("  python3 scripts/setup.py")

    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Setup cancelled. You can run it again anytime:{Colors.END}")
        print(f"  python3 scripts/setup.py")
        sys.exit(0)
    except Exception as e:
        print_error(f"\nSetup failed: {e}")
        print_info("Please report this issue at: https://github.com/anthropics/max-doc-ai/issues")
        sys.exit(1)

if __name__ == '__main__':
    main()
