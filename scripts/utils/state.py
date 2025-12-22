"""
State management for Pylon sync

Tracks which articles have been synced to Pylon, their IDs, URLs, and last sync times.

This is necessary because Pylon's API doesn't provide a "list all articles" endpoint,
so we need to maintain our own state file to know which articles exist.
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
import sys

# Add parent directory to path for config import
sys.path.insert(0, str(Path(__file__).parent.parent))
import config as cfg


def get_state_file_path():
    """Get the path to the state file from config"""
    try:
        config = cfg.get_config()
        return config.get('state', {}).get(
            'sync_state_file',
            './demo/docs/sync-state.json'
        )
    except:
        return './demo/docs/sync-state.json'


def load_state() -> Dict:
    """
    Load Pylon sync state from file

    Returns:
        Dict with state data including articles, collections, etc.
    """
    state_file = get_state_file_path()

    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            return json.load(f)

    # Initialize empty state if file doesn't exist
    try:
        pylon_config = cfg.get_pylon_config()
        return {
            "knowledge_base_id": pylon_config['kb_id'],
            "author_user_id": pylon_config['author_user_id'],
            "collections": pylon_config['collections'],
            "articles": {},
            "last_updated": datetime.now().isoformat()
        }
    except:
        # Minimal state if config not available
        return {
            "knowledge_base_id": "",
            "author_user_id": "",
            "collections": {},
            "articles": {},
            "last_updated": datetime.now().isoformat()
        }


def save_state(state: Dict):
    """
    Save Pylon sync state to file

    Args:
        state: State dictionary to save
    """
    state_file = get_state_file_path()

    # Ensure directory exists
    state_path = Path(state_file)
    state_path.parent.mkdir(parents=True, exist_ok=True)

    # Update last_updated timestamp
    state['last_updated'] = datetime.now().isoformat()

    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2)


def save_article(article_key: str, article_data: Dict):
    """
    Save article information to state

    Args:
        article_key: Unique key for the article (e.g., 'dashboards', 'getting-started')
        article_data: Article data dict with article_id, URLs, etc.
    """
    state = load_state()

    # Add sync timestamp
    article_data['synced_at'] = datetime.now().isoformat()

    # Save to articles dict
    if 'articles' not in state:
        state['articles'] = {}

    state['articles'][article_key] = article_data

    save_state(state)

    print(f"💾 State updated: {article_key}")


def get_article(article_key: str) -> Optional[Dict]:
    """
    Get article information from state

    Args:
        article_key: Unique key for the article

    Returns:
        Article data dict, or None if not found
    """
    state = load_state()
    return state.get('articles', {}).get(article_key)


def update_article_sync_time(article_key: str):
    """
    Update the last sync time for an article

    Args:
        article_key: Unique key for the article
    """
    state = load_state()

    if article_key in state.get('articles', {}):
        state['articles'][article_key]['synced_at'] = datetime.now().isoformat()
        save_state(state)


def delete_article(article_key: str):
    """
    Remove article from state

    Note: This only removes it from our state tracking.
    It does NOT delete the article from Pylon.

    Args:
        article_key: Unique key for the article
    """
    state = load_state()

    if article_key in state.get('articles', {}):
        del state['articles'][article_key]
        save_state(state)
        print(f"🗑️  Removed from state: {article_key}")
    else:
        print(f"⚠️  Article not found in state: {article_key}")


def list_articles() -> Dict[str, Dict]:
    """
    List all articles in state

    Returns:
        Dict mapping article keys to article data
    """
    state = load_state()
    return state.get('articles', {})


def print_state_summary():
    """Print a summary of the current state"""
    state = load_state()

    print("\n" + "="*60)
    print("📊 Pylon Sync State Summary")
    print("="*60)

    print(f"\nKnowledge Base ID: {state.get('knowledge_base_id')}")
    print(f"Last Updated: {state.get('last_updated')}")

    articles = state.get('articles', {})
    print(f"\n📄 Articles: {len(articles)}")

    if articles:
        print("\nSynced articles:")
        for key, data in articles.items():
            synced_at = data.get('synced_at', 'Unknown')
            article_id = data.get('article_id', 'No ID')
            print(f"  • {key}")
            print(f"    ID: {article_id}")
            print(f"    Synced: {synced_at}")
            if 'public_url' in data:
                print(f"    URL: {data['public_url']}")

    print()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Manage Pylon sync state'
    )
    parser.add_argument(
        '--summary',
        action='store_true',
        help='Print state summary'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all articles'
    )
    parser.add_argument(
        '--get',
        help='Get article by key'
    )
    parser.add_argument(
        '--delete',
        help='Delete article from state by key'
    )

    args = parser.parse_args()

    if args.summary or (not any([args.list, args.get, args.delete])):
        print_state_summary()
    elif args.list:
        articles = list_articles()
        print(json.dumps(articles, indent=2))
    elif args.get:
        article = get_article(args.get)
        if article:
            print(json.dumps(article, indent=2))
        else:
            print(f"❌ Article not found: {args.get}")
    elif args.delete:
        delete_article(args.delete)
