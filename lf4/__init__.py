import numpy as np



def load(f):
    if not hasattr(f, "read"): f = open(f, "rb")
    elif f.mode != "rb": raise ValueError("File handle must be opened for binary read.")
    
    ndim = f.read(1)[0]
    shape = np.frombuffer(f.read(2*ndim), dtype = "<u2")
    data = np.frombuffer(f.read(), dtype = "<f4")

    try: data.shape = shape
    except ValueError: raise RuntimeError("Wrong amount of data for size in header.")

    return data.copy()

def save(f, data):
    if not hasattr(f, "write"): f = open(f, "wb")
    elif f.mod != "wb": raise ValueError("File handle must be opened for binary write.")
    
    shape = np.array(data.shape, dtype = "<u2")
    data = data.astype("<f4")
    
    f.write(bytes([data.ndim]))
    f.write(shape.tobytes())
    f.write(data.tobytes())
