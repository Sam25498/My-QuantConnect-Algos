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
