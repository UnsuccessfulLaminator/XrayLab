import numpy as np



def load_mpx_imgs(f, width = 256, height = 256, dtype = np.uint16, n = None):
    if not hasattr(f, "read"): f = open(f, "rb")

    if n: data = np.frombuffer(f.read(width*height*dtype(0).itemsize*n), dtype = dtype)
    else: data = np.frombuffer(f.read(), dtype = dtype)
    
    data.shape = (-1, 256, 256)

    return data.copy() # frombuffer returns a read-only array, copy to make it writeable
