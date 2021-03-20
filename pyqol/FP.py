

import functools
import time
from fastcore.all import store_attr, L


def _NoMatchError(*args, **kwargs):
    raise ValueError(f"No Matches for arguments: {args} & {kwargs}")

def _Default(*args, **kwargs):
    return True

def _PackArgs(*args, **kwargs):
    return ([*args], {**kwargs})

#? The Main Function
class F(object):
    def __init__(self, f): 
        store_attr()
    def __call__(self, *args, **kwargs):
        return self.f(*args, **kwargs)
    def __mul__(self, other):
        return F(lambda *args, **kwargs: self(other(*args, **kwargs)))
    def __add__(self, other):
        return F(lambda *args, **kwargs: other(self(*args, **kwargs)))

def Function(f):
    func = F(f)
    return func

#? The Better Function
class B(F):
    def __init__(self, default = _NoMatchError,): 
        store_attr()
        self.cases = L()
        self.preprocesses = L()
    def add_method(self, register, *args, **kwargs):
        if type(args[0]) == type(lambda x:x):
            test = args[0]
        else:
            test = lambda *args2, **kwargs2:  args2 == args and kwargs2 == kwargs 
        def definition(func):
            if type(func) == type(lambda x:x):
                register.append((test, func))
                return func
            else:
                func2 = lambda *args, **kwargs: func
                register.append((test, func2))
                return func2
        return definition
    def case(self, *args, **kwargs):
        return self.add_method(self.cases, *args, **kwargs)
    def preprocess(self, *args, **kwargs):
        return self.add_method(self.preprocesses, *args, **kwargs)
    def __call__(self, *args, **kwargs):
        for preprocess in self.preprocesses:
            test, func = preprocess
            if test(*args, **kwargs):
                args, kwargs = _PackArgs(func(*args, **kwargs))
        for case in self.cases:
            test, func = case
            if test(*args, **kwargs):
                return func(*args, **kwargs)
        return self.default(*args, **kwargs)

def Bunction(f):
    func = B(f)
    return func

class Helpers():
    @staticmethod
    def timer(f):
        """Prints the runtime of a decorated function"""
        def wrapper_timer(*args, **kwargs):
            start_time = time.perf_counter()
            value = f(*args, **kwargs)
            end_time = time.perf_counter()
            run_time = end_time - start_time
            print(f"Finished {f.__name__!r} in {run_time:.4f} secs")
            return value
        return wrapper_timer


class Map():
    @staticmethod
    def over(itr):
        def exec(f):
            return L(f(e) for e in itr)
        return exec
    @staticmethod
    def using(f):
        def exec(itr):
            return L(f(e) for e in itr)
        return exec