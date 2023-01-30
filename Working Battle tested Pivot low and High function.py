import random
import math
from typing import List, Tuple, Optional

Candle =  [53.49885270867954, 55.81908920231306, 56.543628819671135, 54.91334203757303, 53.28602298570815, 50.88206217227009, 58.75574829911107, 67.08791964978705, 67.93028602435466, 75.28702830897068, 76.9579725679672, 82.36290879038326, 75.56817355864766, 69.34017533902532, 66.26009113033945, 66.92305028171671, 66.1901065326061, 72.12639096834278, 67.48430491755038, 61.09119571893404, 66.1211439315825, 64.55914192542599, 66.47582251910687, 65.01448108858648, 62.23219339963736, 60.23131566478151, 62.97975444439868, 67.11626474858487, 67.94503892701545, 69.33634520296228, 67.31662818606844, 64.29272574088958, 67.41862137031956, 66.25355570863366, 65.66153408223896, 73.16599131104705, 65.82743399746057, 63.48208639792445, 69.71217391618812, 65.89038676747833, 65.21102022978329, 60.44080824736788, 58.899785592758924, 44.79729798702304, 43.68581098953599, 46.413056115090875, 43.06240610656532, 43.21219406434934, 44.32165389969823, 42.87180298401592]
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

    
    
print(pivot_low(Candle))
#Output: [None, None, None, None, None, None, None, 50.88206217227009, None, None, None, None, None, None, None, None, None, None, None, None, None, 61.09119571893404, None, None, None, None, None, 60.23131566478151, None, None, None, None, None, 64.29272574088958, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
print(pivot_high(Candle))
#Output: [None, None, None, None, None, None, None, None, None, None, None, None, None, 82.36290879038326, None, None, None, None, None, 72.12639096834278, None, None, None, None, None, None, None, None, None, None, None, 69.33634520296228, None, None, None, None, None, 73.16599131104705, None, None, None, None, None, None, None, None, None, None, None, None]

###########################################################################################################################################################################
#############################                Next Logical Step                         #################################################################################


import pandas as pd
a = pivot_low(Candle)
b = pivot_high(Candle)
plFound = pd.isnull(a)
phFound = pd.isnull(b)

print(plFound)
#Output: [ True  True  True  True  True  True  True False  True  True  True  True True  True  True  True  True  True  True  True  True False  True  True True  True  True False  True  True  True  True  True False  True  True True  True  True  True  True  True  True  True  True  True  True  True  True  True]

print(phFound)
#Output: [ True  True  True  True  True  True  True  True  True  True  True  True  True False  True  True  True  True  True False  True  True  True  True  True  True  True  True  True  True  True False  True  True  True  True  True False  True  True  True  True  True  True  True  True  True  True  True  True]

########################################################################################################################################################################

print(valuewhen(plFound, Candle, 1))
