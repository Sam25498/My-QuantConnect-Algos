ef line2arr(line, size=-1):
    if size <= 0:
        return np.array(line.array)
    else:
        return np.array(line.get(size=size))
