#!/usr/bin/env python3
"""
GitHub repository integration helper

Handles cloning and accessing external GitHub repositories.
"""

import os
import subprocess
import shutil
from pathlib import Path
from typing import Optional


class GitHubHelper:
    """Helper for working with GitHub repositories"""

    def __init__(self, repo_url: str, auth_method: str = 'gh',
                 github_pat: Optional[str] = None):
        """
        Initialize GitHub helper

        Args:
            repo_url: GitHub repository URL
            auth_method: 'gh' | 'pat' | 'ssh'
            github_pat: Personal Access Token (if auth_method='pat')
        """
        self.repo_url = repo_url
        self.auth_method = auth_method
        self.github_pat = github_pat
        self.working_dir = None

    def clone_repository(self, target_dir: Optional[str] = None) -> str:
        """
        Clone repository to local directory

        Args:
            target_dir: Target directory (default: temp dir)

        Returns:
            Path to cloned repository
        """
        if target_dir is None:
            # Create temp directory under /tmp/max-doc-ai-repos/
            base_temp = Path("/tmp/max-doc-ai-repos")
            base_temp.mkdir(parents=True, exist_ok=True)

            repo_name = Path(self.repo_url).stem
            target_dir = base_temp / repo_name

        target_path = Path(target_dir)

        # Remove if already exists
        if target_path.exists():
            shutil.rmtree(target_path)

        print(f"📥 Cloning repository: {self.repo_url}")
        print(f"   Target: {target_path}")

        # Clone based on auth method
        if self.auth_method == 'gh':
            # Use GitHub CLI (requires gh auth)
            result = subprocess.run(
                ['gh', 'repo', 'clone', self.repo_url, str(target_path)],
                capture_output=True,
                text=True
            )
        elif self.auth_method == 'ssh':
            # Use SSH (requires configured keys)
            result = subprocess.run(
                ['git', 'clone', self.repo_url, str(target_path)],
                capture_output=True,
                text=True
            )
        elif self.auth_method == 'pat':
            # Use PAT in URL
            if not self.github_pat:
                raise ValueError("GitHub PAT required for 'pat' auth method")

            # Convert HTTPS URL to include PAT
            auth_url = self.repo_url.replace(
                'https://',
                f'https://{self.github_pat}@'
            )
            result = subprocess.run(
                ['git', 'clone', auth_url, str(target_path)],
                capture_output=True,
                text=True
            )
        else:
            raise ValueError(f"Unknown auth method: {self.auth_method}")

        if result.returncode != 0:
            raise RuntimeError(
                f"Failed to clone repository:\n{result.stderr}"
            )

        print(f"   ✅ Cloned successfully")
        self.working_dir = str(target_path)
        return self.working_dir

    def cleanup(self):
        """Remove cloned repository"""
        if self.working_dir and Path(self.working_dir).exists():
            shutil.rmtree(self.working_dir)
            print(f"🗑️  Cleaned up: {self.working_dir}")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup"""
        # Don't cleanup on exit - let user decide when to cleanup
        # Useful for debugging or multiple operations
        pass


def get_repo_info(repo_path: str) -> dict:
    """
    Get information about a git repository

    Args:
        repo_path: Path to repository

    Returns:
        dict with remote, branch, commit info
    """
    result = {}

    # Get remote URL
    remote_result = subprocess.run(
        ['git', '-C', repo_path, 'remote', 'get-url', 'origin'],
        capture_output=True,
        text=True
    )
    if remote_result.returncode == 0:
        result['remote'] = remote_result.stdout.strip()

    # Get current branch
    branch_result = subprocess.run(
        ['git', '-C', repo_path, 'branch', '--show-current'],
        capture_output=True,
        text=True
    )
    if branch_result.returncode == 0:
        result['branch'] = branch_result.stdout.strip()

    # Get latest commit
    commit_result = subprocess.run(
        ['git', '-C', repo_path, 'log', '-1', '--format=%H %s'],
        capture_output=True,
        text=True
    )
    if commit_result.returncode == 0:
        result['commit'] = commit_result.stdout.strip()

    return result
