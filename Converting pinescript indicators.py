ef line2arr(line, size=-1):
    if size <= 0:
        return np.array(line.array)
    else:
        return np.array(line.get(size=size))
    
    
    
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

