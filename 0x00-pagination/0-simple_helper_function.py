#!/usr/bin/env python3
"""A module -> pagination"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Function that returns a tuple """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return start_index, end_index
