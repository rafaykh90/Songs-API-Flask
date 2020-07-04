from functools import reduce
from typing import List, Union, Dict, Any


def get_average(items: List[Union[int, float]]) -> float:
    if not items:
        return None

    total_items = len(items)
    total_value = sum(items)

    return round(total_value / total_items, 2)
