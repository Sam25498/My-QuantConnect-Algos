import numpy as np
def pivot_high_points(source, leftbars=5, rightbars=5):
    pivot_highs = np.empty(len(source))
    pivot_highs[:] = np.nan
    for i in range(leftbars, len(source) - rightbars):
        if (source[i-leftbars:i].max() >= source[i] >= source[i+1:i+rightbars+1].max()):
            pivot_highs[i] = source[i]
    return pivot_highs
    
    
def pivot_low_points(source, leftbars=5, rightbars=5):
    pivot_lows = np.empty(len(source))
    pivot_lows[:] = np.nan
    for i in range(leftbars, len(source) - rightbars):
        if (source[i-leftbars:i].min() <= source[i] <= source[i+1:i+rightbars+1].min()):
            pivot_lows[i] = source[i]
    return pivot_lows

    
RSIList = [54.54702219621018, 53.49885270867954, 55.81908920231306, 56.543628819671135, 54.91334203757303, 53.28602298570815, 50.88206217227009, 58.75574829911107, 67.08791964978705, 67.93028602435466]
print(pivot_high_points(RSIList))
print(pivot_low_points(RSIList))

#Output
#   [nan nan nan nan nan nan nan nan nan nan]
#[nan nan nan nan nan nan nan nan nan nan]
data = RSIList
lbL = 5
lbR = 5

import numpy as np
plFound = np.isnan(pivot_low_points(data))
phFound = np.isnan(pivot_high_points(data))

print(plFound) #
print(phFound)

#Output
#[ True  True  True  True  True  True  True  True  True  True]
#[ True  True  True  True  True  True  True  True  True  True]


def count_bars_since_condition(condition, dt):
		count = 0
		condition_met = False
		for bar in dt:
				if condition(bar):
						condition_met = True
						count = 0
				elif condition_met:
						count += 1
		return count

print(count_bars_since_condition(plFound[1], data))
def InRange(self, cond, data):
		bars = count_bars_since_condition(cond, data)
		return rangeLower <= bars and bars <= rangeUpper
		
print(InRange(plFound[1], data ))
