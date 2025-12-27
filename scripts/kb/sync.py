#!/usr/bin/env python3
"""
Generic Knowledge Base Sync Script

Syncs documentation to any KB provider (Pylon, Zendesk, Confluence, etc.)
"""

import os
import sys
from pathlib import Path

# Add parent and project directories to path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent

# IMPORTANT: Project root must be FIRST so utils can be found
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / 'scripts') not in sys.path:
    sys.path.append(str(PROJECT_ROOT / 'scripts'))

# Debug: print paths
if os.getenv('DEBUG'):
    print(f"PROJECT_ROOT: {PROJECT_ROOT}")
    print(f"sys.path[:3]: {sys.path[:3]}")
    print(f"utils exists: {(PROJECT_ROOT / 'utils').exists()}")
    print(f"kb_providers exists: {(PROJECT_ROOT / 'utils' / 'kb_providers').exists()}")

import config as cfg

# Import from project root (utils) and scripts (utils)
try:
    from utils.kb_providers import get_provider, Article  # From project/utils
    from scripts.utils import state as state_manager       # From scripts/utils
    from utils.doc_inventory import DocumentInventory      # From project/utils
except (ModuleNotFoundError, ImportError) as e:
    print(f"❌ Import error: {e}")
    print(f"   PROJECT_ROOT: {PROJECT_ROOT}")
    print(f"   sys.path: {sys.path[:3]}")
    raise


def sync_article_from_markdown(
    provider_name: str,
    markdown_path: str,
    article_key: str,
    title: str,
    slug: str,
    collection_name: str,
    provider_config: dict = None
) -> dict:
    """
    Sync an article from a markdown file to any KB provider

    Args:
        provider_name: Name of KB provider ('pylon', 'zendesk', etc.)
        markdown_path: Path to markdown file
        article_key: Unique key for state tracking
        title: Article title
        slug: Article slug
        collection_name: Collection/category name
        provider_config: Optional provider config (defaults to config.yaml)

    Returns:
        Dict with article info, or None if failed
    """
    print(f"\n{'='*60}")
    print(f"📄 Syncing to {provider_name.upper()}: {Path(markdown_path).name}")
    print(f"{'='*60}")

    # Get provider configuration
    if provider_config is None:
        provider_config = get_provider_config(provider_name)

    # Initialize provider
    provider = get_provider(provider_name, provider_config)
    if not provider:
        return None

    # Read markdown
    if not os.path.exists(markdown_path):
        print(f"❌ File not found: {markdown_path}")
        return None

    with open(markdown_path, 'r') as f:
        md_content = f.read()

    # Convert to provider-specific HTML
    print("🔄 Converting markdown to HTML...")
    html_content = provider.markdown_to_html(md_content)

    # Validate HTML
    is_valid, msg = provider.validate_html(html_content)
    print(f"   {'✅' if is_valid else '❌'} {msg}")

    # Load state to check if article exists
    state_data = state_manager.load_state()
    state_key = f"{provider_name}:{article_key}"
    existing_article = state_data.get('articles', {}).get(state_key)

    # Create Article object
    article = Article(
        title=title,
        slug=slug,
        body_html=html_content,
        collection_name=collection_name
    )

    if existing_article and existing_article.get('article_id'):
        # Update existing article
        article_id = existing_article['article_id']
        success = provider.update_article(article_id, article)

        if success:
            # Update state with new sync time
            state_manager.update_article_sync_time(state_key)
            return existing_article
        else:
            return None
    else:
        # Create new article
        result_article = provider.create_article(article)

        if result_article:
            # Save to state
            article_data = {
                'article_id': result_article.id,
                'collection_id': result_article.collection_id,
                'public_url': result_article.public_url,
                'internal_url': result_article.internal_url,
                'title': result_article.title,
                'slug': result_article.slug,
                'provider': provider_name
            }
            state_manager.save_article(state_key, article_data)
            return article_data
        else:
            return None


def get_provider_config(provider_name: str = None) -> dict:
    """
    Get provider configuration from config.yaml

    Args:
        provider_name: Provider name ('pylon', 'zendesk', etc.) or None for default

    Returns:
        Provider configuration dict
    """
    try:
        kb_info = cfg.get_kb_config()

        # Use specified provider or default from config
        if not provider_name:
            provider_name = kb_info['provider']

        # If requesting specific provider, get its config
        if provider_name != kb_info['provider']:
            config = cfg.get_config()
            kb_config = config.get('knowledge_base', {})
            providers = kb_config.get('providers', {})
            provider_config = providers.get(provider_name)

            if not provider_config:
                raise ValueError(
                    f"Provider '{provider_name}' not found in config.yaml.\n"
                    f"Available providers: {list(providers.keys())}"
                )
            return provider_config

        return kb_info['config']

    except Exception as e:
        # Try old Pylon-only format for backwards compatibility
        if provider_name in [None, 'pylon']:
            return cfg.get_pylon_config()
        raise e


def sync_multiple_articles(provider_name: str, articles: list[dict]) -> dict:
    """
    Sync multiple articles

    Args:
        provider_name: KB provider name
        articles: List of article dicts with 'file', 'key', 'title', 'slug', 'collection'

    Returns:
        Dict mapping article keys to sync results
    """
    print(f"\n{'='*60}")
    print(f"🚀 Syncing {len(articles)} articles to {provider_name.upper()}")
    print(f"{'='*60}\n")

    provider_config = get_provider_config(provider_name)
    results = {}

    for article_info in articles:
        result = sync_article_from_markdown(
            provider_name=provider_name,
            markdown_path=article_info['file'],
            article_key=article_info['key'],
            title=article_info['title'],
            slug=article_info['slug'],
            collection_name=article_info['collection'],
            provider_config=provider_config
        )
        results[article_info['key']] = result

    # Summary
    success_count = sum(1 for r in results.values() if r is not None)
    print(f"\n{'='*60}")
    print(f"✅ Synced {success_count}/{len(articles)} articles")
    print(f"{'='*60}\n")

    return results


def discover_documents(provider_name: str = None) -> None:
    """
    Discover and display available documentation

    Args:
        provider_name: Optional provider to show sync status for
    """
    print("🔍 Discovering documentation...\n")

    # Scan documentation
    inventory = DocumentInventory()
    inventory.scan()

    # Show summary
    inventory.print_summary()

    # Show what needs syncing
    unsynced = inventory.filter_synced(False)
    if unsynced:
        print("\n" + "=" * 70)
        print("⏳ Documents That Need Syncing")
        print("=" * 70)

        by_category = {}
        for doc in unsynced:
            if doc.category not in by_category:
                by_category[doc.category] = []
            by_category[doc.category].append(doc)

        for category, docs in sorted(by_category.items()):
            print(f"\n📁 {category.upper()} ({len(docs)} files)")
            for doc in sorted(docs, key=lambda d: d.slug or d.filename):
                print(f"  • {doc.title or doc.filename}")
                print(f"    Slug: {doc.slug}")
                print(f"    Path: {doc.path}")

                # Show how to sync
                print(f"\n    To sync:")
                provider_flag = f"--provider {provider_name} " if provider_name else ""
                print(f"    python3 scripts/kb/sync.py {provider_flag}\\")
                print(f"      --file {doc.path} \\")
                print(f"      --key {category}-{doc.slug} \\")
                print(f"      --title \"{doc.title or doc.slug}\" \\")
                print(f"      --slug {doc.slug} \\")
                print(f"      --collection {category}")
                print()

        print("=" * 70)


def sync_status(provider_name: str = None) -> None:
    """
    Show sync status of all documentation

    Args:
        provider_name: Optional provider to filter by
    """
    print("📊 Documentation Sync Status\n")

    inventory = DocumentInventory()
    inventory.scan()

    # Filter by provider if specified
    if provider_name:
        inventory.documents = [
            doc for doc in inventory.documents
            if not doc.synced or doc.sync_provider == provider_name
        ]
        print(f"Provider: {provider_name}\n")

    inventory.print_details()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Sync documentation to KB provider'
    )
    parser.add_argument(
        '--provider',
        help='KB provider name (pylon, zendesk, etc.)',
        default=None
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Discover command
    discover_parser = subparsers.add_parser('discover', help='Discover available documentation')

    # Status command
    status_parser = subparsers.add_parser('status', help='Show sync status of all documentation')

    # Sync command
    sync_parser = subparsers.add_parser('sync', help='Sync a specific file')
    sync_parser.add_argument(
        '--file',
        required=True,
        help='Markdown file to sync'
    )
    sync_parser.add_argument(
        '--key',
        required=True,
        help='Article key for state tracking'
    )
    sync_parser.add_argument(
        '--title',
        required=True,
        help='Article title'
    )
    sync_parser.add_argument(
        '--slug',
        required=True,
        help='Article slug'
    )
    sync_parser.add_argument(
        '--collection',
        required=True,
        help='Collection/category name'
    )

    args = parser.parse_args()

    # Determine provider
    if not args.provider:
        try:
            kb_info = cfg.get_kb_config()
            provider_name = kb_info['provider']
        except:
            provider_name = 'pylon'
    else:
        provider_name = args.provider

    # Handle commands
    if args.command == 'discover':
        discover_documents(provider_name)

    elif args.command == 'status':
        sync_status(provider_name)

    elif args.command == 'sync':
        result = sync_article_from_markdown(
            provider_name=provider_name,
            markdown_path=args.file,
            article_key=args.key,
            title=args.title,
            slug=args.slug,
            collection_name=args.collection
        )

        if result:
            print(f"\n✅ Article synced successfully!")
            print(f"   Public URL: {result.get('public_url')}")
            print(f"   Internal URL: {result.get('internal_url')}")
        else:
            print("\n❌ Sync failed")
            sys.exit(1)

    else:
        # No command - show help
        parser.print_help()
        print("\n📚 Available Commands:")
        print("  discover - Scan and list all available documentation")
        print("  status   - Show sync status of all documentation")
        print("  sync     - Sync a specific file to KB provider")
        print("\n💡 Examples:")
        print("  # Discover what documentation exists")
        print("  python3 sync.py discover")
        print("\n  # Check sync status")
        print("  python3 sync.py status")
        print("\n  # Sync a specific file")
        print("  python3 sync.py sync \\")
        print("    --file docs/features/dashboards.md \\")
        print("    --key features-dashboards \\")
        print("    --title 'Dashboards' \\")
        print("    --slug 'dashboards' \\")
        print("    --collection features")
