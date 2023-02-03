import pandas as pd
from typing import List, Tuple, Optional
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
        
def barssince(condition, occurrence=0):
        '''
        Impl of barssince

        RETURNS
        Number of bars since condition was true.
        REMARKS
        If the condition has never been met prior to the current bar, the function returns na.
        '''
        cond_len = len(condition)
        occ = 0
        since = 0
        res = float('nan')
        while cond_len - (since + 1) >= 0:
            cond = condition[cond_len-(since+1)]
            # check for nan cond != cond == True when nan
            if cond and not cond != cond:
                if occ == occurrence:
                    res = since
                    break
                occ += 1
            since += 1
        return res

    
def valuewhen(condition, source, occurrence=0): #print(valuewhen(plFound, Candle[5], 1))
        '''
        Impl of valuewhen
        + added occurrence

        RETURNS
        Source value when condition was true
        '''
        res = float('nan')
        since = barssince(condition, occurrence)
        if since is not None:
            res = source[-(since + 1)]
        return res

RSIList = [80.99, 80.17, 77.81, 72.55, 66.67, 68.41, 78.41, 78.41, 80.89, 80.70, 83.77, 81.96, 81.85, 77.77, 82.07, 81.29, 80.01, 78.73, 77.21, 81.23, 78.08, 65.40, 67.63, 67.63, 67.63, 69.39 ]
lwlist  =  [0.897935, 0.898065, 0.89902, 0.898985, 0.898895, 0.898695, 0.898855, 0.898945, 0.899395, 0.89942, 0.899875, 0.900425, 0.90116, 0.9017, 0.90194, 0.901065, 0.90085, 0.901115, 0.902275, 0.901915, 0.901785, 0.901635, 0.901145, 0.90106, 0.90105, 0.900845, 0.900965, 0.90047, 0.90042, 0.900545, 0.900475, 0.899665, 0.899745, 0.900455, 0.901465, 0.901355, 0.900685, 0.90052, 0.900335, 0.90011, 0.899695, 0.89933, 0.90006, 0.90112, 0.90336, 0.90376, 0.903925, 0.9036, 0.903565, 0.90334, 0.90384, 0.90411, 0.90402, 0.903835, 0.903815, 0.90388, 0.90438, 0.905015, 0.90448, 0.90329, 0.902605, 0.901605, 0.901555, 0.90231, 0.901595, 0.90205, 0.903, 0.90624, 0.906, 0.90594, 0.90596, 0.90629, 0.90534, 0.90512, 0.90498, 0.9054, 0.90521, 0.90508, 0.904955, 0.9039, 0.90346, 0.90381, 0.90389, 0.905485, 0.906435, 0.905675, 0.90382, 0.90287, 0.90249, 0.90396, 0.90309, 0.90273, 0.902815, 0.90305, 0.902985, 0.903085, 0.90291, 0.902155, 0.90176, 0.902425, 0.902105, 0.90205, 0.90194, 0.90179, 0.901995, 0.901485, 0.901585, 0.901395, 0.901625, 0.902915, 0.90332, 0.902615, 0.903305, 0.903465, 0.902565, 0.9015, 0.901695, 0.902125, 0.902785, 0.90274, 0.9028, 0.902865, 0.902605, 0.902215, 0.90219, 0.90172, 0.902765, 0.90306, 0.90284, 0.90295, 0.902525, 0.90308, 0.9021, 0.90079, 0.899235, 0.89734, 0.89752, 0.89678, 0.89569, 0.89501, 0.895165, 0.895155, 0.89437, 0.89445, 0.894695, 0.89477, 0.89496, 0.8951, 0.894035, 0.89322, 0.893295, 0.89329, 0.89432, 0.894265, 0.89469, 0.8951, 0.897865, 0.897625, 0.89757, 0.89801, 0.897585, 0.898945, 0.89943, 0.900545, 0.90144, 0.90198, 0.902235, 0.90222, 0.90167, 0.90156, 0.901735, 0.90236, 0.90239, 0.90255, 0.902235, 0.902285, 0.90247, 0.90242, 0.902665, 0.902855, 0.903445, 0.902725, 0.901595, 0.901305, 0.902145, 0.902905, 0.904395, 0.90625, 0.90689, 0.90655, 0.90712, 0.907045, 0.907145, 0.907735, 0.90752, 0.907325, 0.906895, 0.90653, 0.906965, 0.90746]

print(len(RSIList))
print(RSIList[0])
print()

pls = pivot_low(RSIList)
#phs = 
plFound = pd.isnull(pls)
#phFound = pd.isnull(phs)
print(pls)
print(valuewhen(plFound, RSIList, 1))
#Output: 80.99

#[None, None, None, None, None, None, 66.67, None, None, None, None, None, None, None, None, 77.77, None, None, None, None, None, None, None, 65.4, None, None]
#67.63



