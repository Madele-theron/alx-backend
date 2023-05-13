#!/usr/bin/env python3
"""A module -> pagination"""

import csv
from typing import List
import math
index_range = __import__("0-simple_helper_function").index_range


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Returns a sublist of the full dataset"""
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        start_index, end_index = index_range(page, page_size)
        result = []

        if start_index >= len(self.dataset()):
            return result
        result = self.dataset()
        return result[start_index:end_index]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """Returns a dictionary of paginated information"""

        # Get the page data
        page_data = self.get_page(page, page_size)

        # Calculate the pagination information
        total_pages = math.ceil(len(self.dataset) / page_size)
        has_next_page = page < total_pages
        has_prev_page = page > 1

        # Save data in dict
        pagination_data = {
            "page_size": len(page_data),
            "page": page,
            "data": page_data,
            "next_page": page + 1 if has_next_page else None,
            "prev_page": page - 1 if has_prev_page else None,
            "total_pages": total_pages,
        }

        return pagination_data
