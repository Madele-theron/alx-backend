#!/usr/bin/env python3
"""A module that """
from collections import OrderedDict, defaultdict
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """Inherits from BaseCaching and is a caching system"""
    def __init__(self):
        super().__init__()
        self.cache_data = {}
        self.frequency = defaultdict(OrderedDict)

    def put(self, key, item):
        """
        Add item to cache

        Args:
            key: to identify the item
            item: item to be cached
        """
        if key is None or item is None:
            return

        # if key already exists move key-value pair
        # to next frequency
        if key in self.cache_data:
            frequency_count = self.cache_data[key]
            self.frequency[frequency_count].move_to_end(key)
            self.cache_data[key] += 1
        else:
            # If cache is full find least frequency used item
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                min_frequency = min(self.frequency.keys())
                discarded_item = next(iter(self.frequency[min_frequency]))

                # if there are more than one item with least frequency
                # use LRU method
                if len(self.frequency[min_frequency]) > 1:
                    del self.frequency[min_frequency][discarded_item]
                else:
                    del self.frequency[min_frequency]
                    del self.cache_data[discarded_item]

                print(f"DISCARD: {discarded_item}")

            # add new key with frequency of count 1
            self.cache_data[key] = 1
            self.frequency[1][key] = True

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

        # move item to next frequency
        frequency_count = self.cache_data[key]
        self.frequency[frequency_count].move_to_end(key)
        self.cache_data[key] += 1

        return self.cache_data[key]
