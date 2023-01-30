import numpy as np
import random
import math
from typing import List, Tuple, Optional
import pandas as pd
rangeLower = 5
rangeUpper = 60

def pivot_low(source, bars_left: int = 4, bars_right: int = 2, fill_null_values: bool = False) -> List[Optional[float]]:
    result = []
    for i in range(len(source)):
        if i < bars_left + bars_right:
            result.append(None)
            continue
        is_pivot = True
        subset = source[i - bars_left - bars_right : i + bars_right + 1]
        value_to_check = subset[bars_left]
        for left_pivot in range(bars_left):
            if subset[left_pivot] < value_to_check:
                is_pivot = False
                break
        if is_pivot:
            for right_pivot in range(bars_left + 1, len(subset)):
                if subset[right_pivot] <= value_to_check:
                    is_pivot = False
                    break
            if is_pivot:
                result.append(value_to_check)
            else:
                result.append(None)
        else:
            result.append(None)
    if fill_null_values:
        return fill_pivot_nulls(result)
    return result

def pivot_high(source, bars_left: int = 4, bars_right: int = 2, fill_null_values: bool = False): #-> List[Optional[float]]:
    result = []
    for i in range(len(source)):
        if i < bars_left + bars_right:
            result.append(None)
            continue
        is_pivot = True
        subset = source[i - bars_left - bars_right : i + bars_right + 1]
        value_to_check = subset[bars_left]
        for left_pivot in range(bars_left):
            if subset[left_pivot] > value_to_check:
                is_pivot = False
                break
        if is_pivot:
            for right_pivot in range(bars_left + 1, len(subset)):
                if subset[right_pivot] >= value_to_check:
                    is_pivot = False
                    break
            if is_pivot:
                result.append(value_to_check)
            else:
                result.append(None)
        else:
            result.append(None)
    if fill_null_values:
        return fill_pivot_nulls(result)
    return result


def fill_pivot_nulls(result: List[Optional[float]]) -> List[Optional[float]]:
    values = []
    null_counter = 0
    for item in result:
        if item is not None:
            values.append((item, null_counter))
            null_counter = 0
        else:
            null_counter += 1
    final_list = []
    is_first = True
    for i in range(len(values)):
        if is_first:
            for j in range(values[i][1]):
                final_list.append(None)
            final_list.append(values[i][0])
            is_first = False
        else:
            current = values[i]
            previous = values[i - 1]
            count = current[1]
            for x in range(1, count + 1):
                if current[0] > previous[0]:
                    amount_to_use = (current[0] - previous[0]) / (count + 1)
                    final_list.append(round(previous[0] + (amount_to_use * x), 8))
                else:
                    final_list.append(previous[0])
    return final_list
    

    

