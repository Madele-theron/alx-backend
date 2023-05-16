#!/usr/bin/env python3
"""A module that """
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """Inherits from BaseCaching and is a caching system"""
    def __init__(self):
        super().__init__()

    def put(self, key, item):
        """
        Add item to cache

        Args:
            key: to identify the item
            item: item to be cached

        """
        if key is None or item is None:
            return

        # if cache is full discard the last item
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            last_item = self.cache_data.popitem()[0]
            print(f"DISCARD: {last_item}")

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
