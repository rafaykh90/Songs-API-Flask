from functools import reduce
from typing import List, Union, Dict, Any


def get_average(items: List[Union[int, float]], key: str = None) -> float:
    total_items = len(items)
    total_value = reduce(lambda total, value: total +
                         (value[key] if key else value), items, 0)

    return round(total_value / total_items, 2)
