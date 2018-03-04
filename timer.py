import time

def timer(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('{} took {:2.2f} ms'.format(method.__name__, (te - ts) * 1000))
        return result
    return timed