#!/usr/bin/env python3
"""A module that """
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """Inherits from BaseCaching and is a caching system"""
    def put(self, key, item):
        """
        Add item to cache

        Args:
            key: to identify the item
            item: item to be cached

        """
        if key is None or item is None:
            return

        self.cache_data[key] = item

    def get(self, key):
        """
        Retrieve item from cache

        Args:
            key: associated with the item.

        Returns:
            Item value if found in the cache, else None.

        """
        if key is None or key not in self.cache_data:
            return None

        return self.cache_data[key]
