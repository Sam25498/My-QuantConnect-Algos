import pandas as pd
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
print(len(RSIList))
print(RSIList[0])
print()

