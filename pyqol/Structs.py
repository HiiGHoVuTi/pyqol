
from fastcore.all import store_attr
import functools
from fastcore.all import L
L = L

#? Dict, but cool
class Struct(object):
    def __init__(self, *args, **kwargs): 
        store_attr()
        for k, v in kwargs.items():
            vars(self)[k] = v
    def get(self, key):
        return vars(self).get(key)
    def __add__(self, other):
        if type(other) == type(self):
            return Struct(**{
                **vars(self),
                **vars(other),
            })
        else:
            raise NotImplementedError(f"Addition of {type(Struct)} and {type(Other)}")

class Registry():
    """Creates a registry of functions"""
    def __init__(self,):
        self.registry = dict()
    def register(self, f):
        self.registry[f.__name__] = f
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            f(*args, **kwargs)
        return wrapper
    def __getitem__(self, name):
        return self.registry[name]


import operator
class NaV():
    def __init__(self, message):
        store_attr()
        self.logs = L()
    def __str__(self):
        return f"Not a Value !\nMessage: {self.message}\n" + \
            ("Logs:\n" + "\n".join([f"Operation {k.__repr__()[19:-1]} with {v}" 
                for k, v in self.logs.items]) 
            if len(self.logs) > 0 else "")
    def __repr__(self):
        return self.__str__()
    @classmethod
    def consume(self, operator):
        def _(self, other):
            self.logs.append(L(operator, other))
            return self
        return _

for name in ["__add__", "__sub__", "__mul__", "__truediv__", "__floordiv__",
                "__mod__", "__pow__", "__rshift__", "__lshift__", "__and__",
                "__or__", "__xor__", "__LT__", "__GT__", "__LE__", "__GE__",
                "__EQ__", "__NE__", "__ISUB__", "__IADD__", "__IMUL__", "__IDIV__",
                "__IFLOORDIV__", "__IMOD__", "__IPOW__", "__IRSHIFT__", "__ILSHIFT__",
                "__IAND__", "__IOR__", "__IXOR__", "__NEG__", "__POS__", "__INVERT__"]:
    try:
        setattr(NaV, name, NaV.consume(getattr(operator, name.lower())))
    except:
        pass


from pyqol.Bittors import I
from inspect import signature

class Stream():
    Generator = lambda count, fn, requires_idx=False: Struct(uid="generator", fn=fn, count=count, requires_idx=requires_idx)
    List = lambda x: Struct(uid="list", elements=x)
    Iterator = lambda x: Struct(uid="iterator", it=x)

    def __init__(self, iterable=[], cached=True, cache_size=10):
        self.generated = iterable
        self.cached = cached
        self.cache_size = cache_size
        self.start_index = 0
        self.current = 0
        self.generators = []
    def __iter__(self):
       return self
    def get(self, idx):
        try:
            return self.generated[idx - self.start_index]
        except IndexError:
            if idx < 0:
                raise IndexError("Stream index < 0, you're generating with a function expecting more arguments than there are element in the Stream")
            try:
                gen = self.generators[0]
            except IndexError:
                return IndexError
            params = len(signature(gen.fn).parameters)
            if gen.get("requires_idx"):
                params -= 1
            inputs = [self.get(idx - i - 1) for i in I(-params)]
            if gen.get("requires_idx"):
                inputs = [idx, *inputs]
            try:
                res = gen.fn(*inputs)
            except StopIteration:
                self.generators = self.generators[1:]
                return self.get(idx)
            if self.cached:
                if len(self.generated) > idx - self.start_index:
                    self.generated[idx - self.start_index] = res
                else:
                    self.generated.append(res)
            if gen.count != None:
                gen.count -= 1
            self.update()
            return res
    def __getitem__(self, key):
        if isinstance(key, slice):
            start = key.start if key.start else 0
            stop = key.stop if key.stop else start
            step = key.step if key.step else 1
            for i in I(stop // step - start):
                j = start + i * step
                yield self.get(j)
        else:
            yield self.get(key)
    def update(self):
        self.start_index += max(0, len(self.generated) - self.cache_size)
        self.generated = self.generated[-self.cache_size:]
        if self.generators[0].count != None:
            if self.generators[0].count <= 0:
                self.generators = self.generators[1:]
    def __next__(self):
        self.current += 1
        value = self.get(self.current - 1)
        if value == IndexError:
            raise StopIteration
        return value
    def __lshift__(self, other):
        if type(other) == Struct:
            if other.get("uid") == "generator":
                 self.generators.append(other)
            elif other.get("uid") == "list":
                l = L(reversed(other.elements))
                gen = Struct(
                    fn = lambda: l.pop(),
                    count = len(other.elements)
                )
                self.generators.append(gen)
            elif other.get("uid") == "iterator":
                it = other.it
                gen = Struct(
                    fn = lambda: next(it),
                    count = None
                )
                self.generators.append(gen)
        else:
            self.generators.append(Stream.Generator(1, lambda: other))
        return self
