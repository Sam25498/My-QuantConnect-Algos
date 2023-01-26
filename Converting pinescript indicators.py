"""
conditions
to use methods like barssince, valuewhen from pinescript, which allows conditions like: setupCountUp == self.p.setup_bars the easiest method I found 
is to use numpy for this.

convert a line to a numpy array (using get(size=SIZE) to not work on complete line but only a defined range of data)
"""

def line2arr(line, size=-1):
    if size <= 0:
        return np.array(line.array)
    else:
        return np.array(line.get(size=size))
    
    
 """provide methods which works as methods from pinescript: so I wrote the methods I needed."""   
def na(val):
    return val != val

def nz(x, y=None):
    if isinstance(x, np.generic):
        return x.fillna(y or 0)
    if x != x:
        if y is not None:
            return y
        return 0
    return x

def barssince(condition, occurrence=0):
    cond_len = len(condition)
    occ = 0
    since = 0
    res = float('nan')
    while cond_len - (since+1) >= 0:
        cond = condition[cond_len-(since+1)]
        if cond and not cond != cond:
            if occ == occurrence:
                res = since
                break
            occ += 1
        since += 1
    return res


def valuewhen(condition, source, occurrence=0):
    res = float('nan')
    since = barssince(condition, occurrence)
    if since is not None:
        res = source[-(since+1)]
    return res    
