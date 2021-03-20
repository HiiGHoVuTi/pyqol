from fastcore.foundation import L

def I(i, *k, enum=False, reverse=False, chunking=False, chunk_size=1):
    #? Types
    if type(i) == type(None):
        j = 0
        while True:
            yield j
            j += 1
    elif type(i) == int:
        if i < 0: i = -i; loopyloop = reversed(range(i))
        else: loopyloop = range(i)
    else: loopyloop = i
    
    if len(k) > 0:
        loopyloop = zip(loopyloop, *[I(ki) for ki in k])

    #? Modifiers
    if reverse:
        loopyloop = reversed(loopyloop)
    if enum:
        loopyloop = enumerate(loopyloop)
    if chunking:
        iterator = iter(loopyloop)
        while True:
            yielding = L()
            for _ in I(chunk_size):
                try:
                    yielding += next(iterator)
                except:
                    return
            yield yielding
    #? Final Run
    for j in loopyloop:
        yield j

class Multiterator():
    all = 0xA11
    def __init__(self,):
        self.iterations = {}
    def __call__(self, name, *args, **kwargs):
        self.iterations[name] = True
        for m in I(*args, **kwargs):
            if self.iterations[name]:
                yield m
            else:
                break
    def stop(self, name):
        if name == Multiterator.all:
            for i in self.iterations:
                self.iterations[i] = False
        else:
            self.iterations[name] = False


def IR(i, *args, **kwargs):
    return I(i, reverse=True, *args, **kwargs)

def IE(i, *args, **kwargs):
    return I(i, enum=True, *args, **kwargs)

def IC(i, chunk_size, *args, **kwargs):
    return I(i, chunking=True, chunk_size=chunk_size, *args, **kwargs)