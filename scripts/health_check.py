#!/usr/bin/env python3
"""
Health Check System for max-doc-ai

Verifies all components are working correctly and provides helpful guidance.
"""

import os
import sys
from pathlib import Path
import subprocess

# Add project root to path (must be first for utils/ imports)
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Colors
class C:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def check(name):
    """Decorator for health checks"""
    def decorator(func):
        func.check_name = name
        return func
    return decorator

class HealthChecker:
    """Run health checks and report status"""

    def __init__(self):
        self.checks = []
        self.results = []

    def add_check(self, func):
        """Add a health check function"""
        self.checks.append(func)

    def run_all(self):
        """Run all health checks"""
        print(f"\n{C.BOLD}{C.BLUE}{'='*70}")
        print(f"{'Health Check - max-doc-ai'.center(70)}")
        print(f"{'='*70}{C.END}\n")

        for check_func in self.checks:
            check_name = getattr(check_func, 'check_name', check_func.__name__)
            print(f"{C.BOLD}Checking: {check_name}{C.END}")

            try:
                passed, message, fix_hint = check_func()

                if passed:
                    print(f"  {C.GREEN}✅ {message}{C.END}")
                    self.results.append((check_name, True, message, None))
                else:
                    print(f"  {C.RED}❌ {message}{C.END}")
                    if fix_hint:
                        print(f"  {C.YELLOW}💡 {fix_hint}{C.END}")
                    self.results.append((check_name, False, message, fix_hint))

            except Exception as e:
                print(f"  {C.RED}❌ Error: {e}{C.END}")
                self.results.append((check_name, False, str(e), "Check error logs"))

            print()  # Blank line between checks

    def print_summary(self):
        """Print summary of all checks"""
        passed = sum(1 for _, result, _, _ in self.results if result)
        failed = len(self.results) - passed

        print(f"{C.BOLD}{'='*70}")
        print(f"{'Summary'.center(70)}")
        print(f"{'='*70}{C.END}\n")

        print(f"{C.GREEN}✅ Passed: {passed}{C.END}")
        print(f"{C.RED}❌ Failed: {failed}{C.END}")

        if failed == 0:
            print(f"\n{C.GREEN}{C.BOLD}🎉 All checks passed! Your system is ready to use.{C.END}\n")
        else:
            print(f"\n{C.YELLOW}⚠️  Some checks failed. See fixes above.{C.END}\n")

        print(f"{C.BOLD}{'='*70}{C.END}\n")

# Initialize checker
checker = HealthChecker()

@check("Python Version")
def check_python_version():
    """Check Python version is 3.8+"""
    if sys.version_info >= (3, 8):
        version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        return True, f"Python {version} installed", None
    else:
        version = f"{sys.version_info.major}.{sys.version_info.minor}"
        return False, f"Python {version} is too old", "Install Python 3.8 or newer"

@check("Configuration File")
def check_config_file():
    """Check if config.yaml exists"""
    config_path = PROJECT_ROOT / 'config.yaml'

    if config_path.exists():
        return True, "config.yaml found", None
    else:
        return False, "config.yaml not found", "Run: python3 scripts/setup.py"

@check("Configuration Loading")
def check_config_loads():
    """Check if config.yaml loads successfully"""
    try:
        import config as cfg
        config_obj = cfg.get_config()
        return True, "Configuration loads successfully", None
    except FileNotFoundError:
        return False, "config.yaml not found", "Run: python3 scripts/setup.py"
    except Exception as e:
        return False, f"Config has errors: {e}", "Check config.yaml syntax"

@check("Environment Variables")
def check_env_vars():
    """Check if .env file exists"""
    env_path = PROJECT_ROOT / '.env'

    if env_path.exists():
        # Count variables
        with open(env_path, 'r') as f:
            lines = [l for l in f.readlines() if l.strip() and not l.startswith('#')]
        return True, f".env file found ({len(lines)} variables)", None
    else:
        return False, ".env file not found", "Run: python3 scripts/setup.py"

@check("Knowledge Base Provider")
def check_kb_provider():
    """Check if KB provider is configured"""
    try:
        import config as cfg
        kb_info = cfg.get_kb_config()
        provider = kb_info['provider']
        return True, f"Provider configured: {provider}", None
    except Exception as e:
        return False, f"No KB provider configured", "Run: python3 scripts/setup.py"

@check("Provider Connection")
def check_provider_connection():
    """Check if we can connect to KB provider"""
    try:
        import config as cfg
        from utils.kb_providers import get_provider

        kb_info = cfg.get_kb_config()
        provider_name = kb_info['provider']
        provider = get_provider(provider_name, kb_info['config'])

        if not provider:
            return False, f"Could not initialize provider '{provider_name}'", "Check your API credentials"

        if provider.test_connection():
            return True, f"Successfully connected to {provider_name}", None
        else:
            return False, f"Cannot connect to {provider_name}", "Check API credentials and network"

    except Exception as e:
        return False, f"Connection test failed: {e}", "Run: python3 scripts/setup.py"

@check("Documentation Directories")
def check_doc_directories():
    """Check if documentation directories exist"""
    try:
        import config as cfg
        from utils.doc_inventory import DocumentInventory

        inventory = DocumentInventory()
        inventory.scan()

        if len(inventory.documents) > 0:
            return True, f"Found {len(inventory.documents)} documentation files", None
        else:
            return True, "No documentation yet (this is okay for new setup)", None

    except Exception as e:
        return False, f"Cannot scan documentation: {e}", "Check documentation paths in config.yaml"

@check("Output Directory")
def check_output_directory():
    """Check if output directory exists"""
    try:
        import config as cfg
        output_config = cfg.get_output_config()
        output_dir = Path(output_config['base_dir'])

        if not output_dir.is_absolute():
            output_dir = PROJECT_ROOT / output_dir

        if output_dir.exists():
            return True, f"Output directory exists: {output_dir}", None
        else:
            # Create it
            output_dir.mkdir(parents=True, exist_ok=True)
            return True, f"Created output directory: {output_dir}", None

    except Exception as e:
        return False, f"Cannot access output directory: {e}", "Check output config in config.yaml"

@check("Skills Registration")
def check_skills():
    """Check if skills are properly registered"""
    try:
        from utils.skill_validator import SkillValidator

        validator = SkillValidator()
        results = validator.validate_all()

        found = len(results['skills_found'])
        registered = len(results['skills_registered'])
        invalid = len(results['invalid_skills'])
        unregistered = len(results['skills_unregistered'])

        if unregistered > 0:
            return False, f"{unregistered} skills not registered", "Run: python3 utils/skill_validator.py"
        elif invalid > 0:
            return False, f"{invalid} skills have errors", "Run: python3 utils/skill_validator.py"
        else:
            return True, f"All {found} skills registered and valid", None

    except Exception as e:
        return False, f"Cannot validate skills: {e}", "Check .claude/skills/ directory"

@check("Git Repository")
def check_git():
    """Check if we're in a git repository"""
    try:
        subprocess.run(['git', 'status'], capture_output=True, check=True, cwd=PROJECT_ROOT)
        return True, "Git repository initialized", None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False, "Not a git repository", "Run: git init (optional)"

@check("Python Dependencies")
def check_dependencies():
    """Check if required Python packages are installed"""
    required = ['yaml', 'requests', 'markdown']
    missing = []

    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)

    if missing:
        return False, f"Missing packages: {', '.join(missing)}", f"Install with: pip install {' '.join(missing)}"
    else:
        return True, f"All required packages installed", None

# Register all checks
checker.add_check(check_python_version)
checker.add_check(check_config_file)
checker.add_check(check_config_loads)
checker.add_check(check_env_vars)
checker.add_check(check_kb_provider)
checker.add_check(check_provider_connection)
checker.add_check(check_doc_directories)
checker.add_check(check_output_directory)
checker.add_check(check_skills)
checker.add_check(check_git)
checker.add_check(check_dependencies)

def main():
    """Run health checks"""
    try:
        checker.run_all()
        checker.print_summary()

        # Provide next steps
        failed_count = sum(1 for _, result, _, _ in checker.results if not result)

        if failed_count > 0:
            print(f"{C.BOLD}What to do next:{C.END}")
            print(f"  1. Fix the issues listed above")
            print(f"  2. Run health check again: {C.BLUE}python3 scripts/health_check.py{C.END}")
            print(f"  3. Or run setup: {C.BLUE}python3 scripts/setup.py{C.END}\n")
        else:
            print(f"{C.BOLD}You're ready to go!{C.END}")
            print(f"  Try: {C.BLUE}python3 scripts/kb/sync.py discover{C.END}\n")

    except KeyboardInterrupt:
        print(f"\n\n{C.YELLOW}Health check cancelled{C.END}")
        sys.exit(0)

if __name__ == '__main__':
    main()
