import numpy as np
def pivot_high_points(source, leftbars=5, rightbars=5):
    pivot_highs = np.empty(len(source))
    pivot_highs[:] = np.nan
    for i in range(leftbars, len(source) - rightbars):
        if (source[i-leftbars:i].max() >= source[i] >= source[i+1:i+rightbars+1].max()):
            pivot_highs[i] = source[i]
    return pivot_highs
    
