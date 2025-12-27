#!/usr/bin/env python3
"""
Knowledge Base Providers

Factory and registry for KB providers (Pylon, Zendesk, Confluence, etc.)
"""

from typing import Dict, Optional
from utils.kb_providers.base import KBProvider, Article, ImageUpload, ArticleStatus
from utils.kb_providers.pylon import PylonProvider
from utils.kb_providers.zendesk import ZendeskProvider


# Provider registry
PROVIDERS = {
    'pylon': PylonProvider,
    'zendesk': ZendeskProvider,
    # Add more providers here as they're implemented:
    # 'confluence': ConfluenceProvider,
    # 'notion': NotionProvider,
    # 'intercom': IntercomProvider,
    # 'gitbook': GitBookProvider,
}


def get_provider(provider_name: str, config: Dict) -> Optional[KBProvider]:
    """
    Factory function to create a KB provider instance

    Args:
        provider_name: Name of the provider ('pylon', 'zendesk', etc.)
        config: Provider-specific configuration dict

    Returns:
        KBProvider instance or None if provider not found
    """
    provider_class = PROVIDERS.get(provider_name.lower())

    if not provider_class:
        available = ', '.join(PROVIDERS.keys())
        print(f"❌ Unknown provider: {provider_name}")
        print(f"   Available providers: {available}")
        return None

    try:
        return provider_class(config)
    except Exception as e:
        print(f"❌ Error initializing {provider_name} provider: {e}")
        return None


def list_available_providers() -> list[str]:
    """Get list of available provider names"""
    return list(PROVIDERS.keys())


def register_provider(name: str, provider_class: type):
    """
    Register a custom provider

    Args:
        name: Provider name
        provider_class: Class that implements KBProvider
    """
    if not issubclass(provider_class, KBProvider):
        raise ValueError(f"{provider_class.__name__} must inherit from KBProvider")

    PROVIDERS[name.lower()] = provider_class
    print(f"✅ Registered provider: {name}")


# Export main classes and functions
__all__ = [
    'KBProvider',
    'Article',
    'ImageUpload',
    'ArticleStatus',
    'PylonProvider',
    'ZendeskProvider',
    'get_provider',
    'list_available_providers',
    'register_provider',
]
