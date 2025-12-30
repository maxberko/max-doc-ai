#!/usr/bin/env python3
"""
Skill Validator

Validates that all skills are properly registered and accessible
"""

import os
import json
from pathlib import Path
from typing import List, Dict


class SkillValidator:
    """Validate skill registration and structure"""

    def __init__(self, base_dir: str = None):
        if base_dir is None:
            # Try to find .claude directory
            base_dir = self._find_claude_dir()

        self.base_dir = Path(base_dir)
        self.skills_dir = self.base_dir / "skills"
        self.settings_file = self.base_dir / "settings.local.json"

    def _find_claude_dir(self) -> Path:
        """Find .claude directory from current location"""
        current = Path.cwd()

        # Check current directory
        if (current / ".claude").exists():
            return current / ".claude"

        # Check parent directories
        for parent in current.parents:
            if (parent / ".claude").exists():
                return parent / ".claude"

        raise FileNotFoundError("Could not find .claude directory")

    def validate_all(self) -> Dict:
        """Run all validations and return results"""
        results = {
            'skills_found': [],
            'skills_registered': [],
            'skills_unregistered': [],
            'invalid_skills': [],
            'permissions': {},
            'warnings': [],
            'errors': []
        }

        # Find all skills
        if not self.skills_dir.exists():
            results['errors'].append(f"Skills directory not found: {self.skills_dir}")
            return results

        for skill_dir in self.skills_dir.iterdir():
            if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
                skill_name = skill_dir.name
                results['skills_found'].append(skill_name)

                # Validate skill structure
                is_valid, issues = self._validate_skill_structure(skill_dir)
                if not is_valid:
                    results['invalid_skills'].append({
                        'name': skill_name,
                        'issues': issues
                    })

        # Check permissions
        if self.settings_file.exists():
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                permissions = settings.get('permissions', {}).get('allow', [])

                # Extract skill permissions
                for perm in permissions:
                    if perm.startswith('Skill('):
                        skill_name = perm.replace('Skill(', '').replace(')', '')
                        results['skills_registered'].append(skill_name)


                results['permissions'] = {
                    'total': len(permissions),
                    'skills': len(results['skills_registered'])
                }
        else:
            results['warnings'].append(f"Settings file not found: {self.settings_file}")

        # Find unregistered skills
        for skill in results['skills_found']:
            if skill not in results['skills_registered']:
                results['skills_unregistered'].append(skill)

        return results

    def _validate_skill_structure(self, skill_dir: Path) -> tuple[bool, List[str]]:
        """Validate that a skill has required files"""
        issues = []

        # Check for SKILL.md
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            # Try lowercase
            skill_file = skill_dir / "skill.md"
            if not skill_file.exists():
                issues.append("Missing SKILL.md or skill.md file")
                return False, issues

        # Validate SKILL.md has required frontmatter
        with open(skill_file, 'r', encoding='utf-8') as f:
            content = f.read()

            # Check for frontmatter
            if not content.startswith('---'):
                issues.append("SKILL.md missing frontmatter (---)")

            # Check for name
            if 'name:' not in content:
                issues.append("SKILL.md missing 'name:' in frontmatter")

            # Check for description
            if 'description:' not in content:
                issues.append("SKILL.md missing 'description:' in frontmatter")

        return len(issues) == 0, issues

    def print_report(self):
        """Print a formatted validation report"""
        results = self.validate_all()

        print("\n" + "=" * 70)
        print("🔍 Skill Validation Report")
        print("=" * 70)

        # Skills found
        print(f"\n📦 Skills Found: {len(results['skills_found'])}")
        for skill in results['skills_found']:
            registered = "✅" if skill in results['skills_registered'] else "❌"
            print(f"  {registered} {skill}")

        # Registered skills
        print(f"\n✅ Registered in Permissions: {len(results['skills_registered'])}")
        for skill in results['skills_registered']:
            exists = "✅" if skill in results['skills_found'] else "⚠️  (missing)"
            print(f"  {exists} {skill}")

        # Unregistered skills
        if results['skills_unregistered']:
            print(f"\n❌ Unregistered Skills: {len(results['skills_unregistered'])}")
            for skill in results['skills_unregistered']:
                print(f"  • {skill}")
            print("\n  To fix: Add to .claude/settings.local.json:")
            for skill in results['skills_unregistered']:
                print(f'    "Skill({skill})",')

        # Invalid skills
        if results['invalid_skills']:
            print(f"\n⚠️  Invalid Skills: {len(results['invalid_skills'])}")
            for skill in results['invalid_skills']:
                print(f"  • {skill['name']}")
                for issue in skill['issues']:
                    print(f"    - {issue}")

        # Warnings
        if results['warnings']:
            print(f"\n⚠️  Warnings:")
            for warning in results['warnings']:
                print(f"  • {warning}")

        # Errors
        if results['errors']:
            print(f"\n❌ Errors:")
            for error in results['errors']:
                print(f"  • {error}")

        # Summary
        print(f"\n" + "=" * 70)
        if not results['errors'] and not results['invalid_skills'] and not results['skills_unregistered']:
            print("✅ All skills are valid and registered!")
        else:
            print("⚠️  Some issues found - see details above")
        print("=" * 70 + "\n")


def validate_skills():
    """Convenience function to run validation"""
    validator = SkillValidator()
    validator.print_report()


if __name__ == '__main__':
    validate_skills()
