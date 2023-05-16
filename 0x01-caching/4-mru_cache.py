#!/usr/bin/env python3
"""A module that """
from collections import OrderedDict
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """Inherits from BaseCaching and is a caching system"""
    def __init__(self):
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """
        Add item to cache

        Args:
            key: to identify the item
            item: item to be cached
        """
        if key is None or item is None:
            return

        # if key already exists move to end of dict
        # last item is most recently used
        if key in self.cache_data:
            self.cache_data.move_to_end(key)
        else:
            # If cache is full remove the last item in dict
            # (most recently used item)
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                discarded_item = next(reversed(self.cache_data))
                del self.cache_data[discarded_item]
                print(f"DISCARD: {discarded_item}")

        # Update value for key
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

        # new key goes to end of dict
        self.cache_data.move_to_end(key)

        return self.cache_data[key]
