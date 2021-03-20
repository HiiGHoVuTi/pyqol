
# PyQoL

This package contains a lot of feature for Quality of Life, functionnal programming, and others.


> Big titles represent modules, so for imports, you need to use `from pyqol.MODULE import function`

# `.CORE`

## `codedit`

Codedit is a decorator that lets you change the source code of a function using regexes. Sadly the syntax has to be "python-valid" before, but the code doesn't have to mean anything though.

```py
from pyqol.CORE import codedit

@codedit("oooooooone", "1")
def add_one(x):
    return x + oooooooone
@codedit(r"_(.+)_more_than\[(.+)\]", r"\2 + \1")
def add_one(x):
    return _1_more_than[x]
```
Obviously, in that case it's not that useful, but I'm sure you can find some hacks using it :)

## `Codedits`

Is a class that contains all known useful codedits.

### `.Lambda`

Lets you define a custom lambda operator.
```py
from pyqol.CORE import Codedits

@Codedits.Lambda(">>")
def add_one(x):
    ld = {a >> a + 1}
    return ld(x)
```
Valid lambdas include: `-1>`, `>`, `:`, `>>`, ..

# `.Bittors` (better iterators)

## `I` is the new `range`

```py
from pyqol.Bittors import I, IC, IE, IR, Multiterator
```

`I`, and its brothers `IR`, `IC`, `IE` are iteration functions, used to create loops.
It will iterate over any iterable, and transform a `int` argument into a range from `0` to this `int`. Negative `int`s lead to a backwards loop.
It will iterate over all arguments at the same time, and zip them.

Arguments are:
```haskell
I(*args, revserse = False, enum = False, chunking=False, chunk_size=1)
```

`Enum = True` is the same as zipping with `I(None)`, which returns an infinite loop. It also can be called with `IE`

Chunking, also called by `IC` returns multiple values at once, in a tuple.
```py
IC(-8, chunk_size=2) -> (7, 6), (5, 4), (3, 2), (1, 0)
```

> No `start, end, step` here, all arguments are the iterations

## `Multiterator`
This lets you handle complex iteration patterns while not suffering from the usual problems caused by having nested loops.
Here, an example speaks for itself:
```py
my_iterator = Multiterator()
for i in my_iterator("outer range loop", 5):
    for j, k in my_iterator("inner zip loop", x, z):
        if ...
          my_iterator.stop("inner zip loop")
        if ...
          my_iterator.stop("outer range loop")
        if ...
          my_iterator.stop(Multiterator.all)
```

> Multiterator's call works exactly like a `I` call.

# `.Structs`

## `Struct`

Struct takes any arguments when created, and stores them. It is similar to a JS object.
```py
from pyqol.Structs import Struct

my_object = Struct(health=100, strength=20)
my_object.sword = Swords.Diamond
def _run(self: Struct):
    pass
my_object.run = _run
my_object.run()
sword_type = my_object.get("sword")
will_return_none = my_object.get("Flamingo")
```

## `Registry`

You can create registers of functions (for plugin management, or special scoping), by creating a registry:
```py
from pyqol.Structs import Registry

r = Registry()
```
Then, you can register functions in it, and access them that way.
```py
@r.register
def my_happy_little_function(x):
    print(f"happy little {x}")

r.registry["my_happy_little_function"]("accident")
r["my_happy_little_function"]("programmer")
```

## `NaV`
is a substitute for a value, like `Nothing` in FP, or `NaN` in JS. It nullifies any operation done to it, and logs them internally. This means that you can have a program fail silently, and still know what happened to that variable.
```py
from pyqol.Structs import NaV

def div(a, b):
    if b == 0: return NaV("Division by 0")
    return a / b
foo = div(8, 0)
bar = foo * 8 + 5
print(bar)
```
```c
Not a Value !
Message: Division by 0
Logs:
Operation mult with 8
Operation add with 5
```

> Most external libs won't be compatible with this, it might not always be optimal to use NaV.

## `Stream`

This is a big feature, quite hard to explain properly.
A stream works like a queue, for iterables and lazy evaluation. You can add four things to a Stream's queue: Literals, Lists (anything that can turn into a list), Iterable (no ranges) and Generators.
A few examples will speak for themselves.

```py
from pyqol.Structs import Stream

for i in Stream([1, 2, 3]):
    print(i) #1, 2, 3

my_stream = Stream() << 1 << 2 << 3
list(my_stream) == [1, 2, 3]

for i in my_stream:
    ...
    my_stream << next_val << other_val
```

### `Stream.List`

```py
my_stream << Stream.List([1, 2, 3, 4, 5])
```

### `Stream.Iterable`

```py
my_stream << Stream.Iterable(I(12))
my_stream << other_stream # streamception
```

### `Stream.Generator`

For this, you have multiple options. This lets you generate the next element of the stream depending on the index of the element, and the elements prior.
```py
s << Stream.Generator(3, lambda idx: idx * 2, require_index=True)
# 0, 2, 4
s << Stream.Generator(5, lambda a: a * 2)
# 4*2, 16, 32, 64, 128
```
Now, let's create the easiest fibonacci iterator ever ! Don't worry about performence, it's autocached !
```py
# first define a basecase
fib = Stream(cache_size=50) << 1 << 1 
# None means it'll generate forever
fib << Stream.Generator(None, lambda a, b: a + b)
for i in fib[:20]:
    print(i) # 1, 1, 2, 3, 5, ....
```

# `.FP`

## `Function`
You can decorate one of your functions with `Function` to access function composition, and other features.
```py
from pyqol.FP import Funtion, F

@Function
def add_two(n): return n + 2
mult_by_two = Function(lambda x: x * 2)

add_then_mult = (add_two + mult_by_two)
mult_then_add = (add_two * mult_by_two)
```

## `Bunction` (better function)

This class is a superset of `Function`, which allows for cool setups. Let's implement the fibonacci function with it, in a very defensive manner:
```python
# First, setup the default case
from pyqol.FP import Bunction, B

@Bunction
def fib(n):
    return fib(n-1) + fib(n-2) 
```
Alone, this function doesn't work, it needs to return `1` if the input is `0` or `1`. We can easily patch this by adding cases, which will overwrite the default.
```py
#if x is 0, this case will be executed
@fib.case(lambda x : x == 0)
def _one(x): return 1
```
Yes, this is ugly, that's why you can also do this:
```py
# if input is 1, return 1
fib.case(1)(1)
```
Now, let's do a little defensive programming, and make our function idiot-proof:
```py
fib.case(lambda x : x < 0)(0)
```
We can even preprocess the inputs, to fit in one of our cases when it couldn't before
```py
@fib.preprocess(lambda x : type(x) == str)
def _exec(x):
    if x.isnumber(): # implement your own isnumber, python doesn't have one for floats for some reason
        return float(x) # will then be converted to a float
    else:
        return 0 # will input 0 to fib

# Then, convert floats to ints
fib.preprocess(lambda x : type(x) == float)(lambda x : int(x))
```

## `Map`

```py
from pyqol.FP import Map
```

A new tool for iterating, the `Map`

## `Map.over`

Map over is a curried function taking in an iterable, then a function, and outputs a new `L`ist of the results of the function. You can use it as a decorator, or as a normal function call
```py
Map.over([0, 1, 2, 3])(lambda x : x * 2) == L(0, 2, 4, 6)
@Map.over([0, 1, 2, 3])
def newlist(e):
    return e * 2
newlist == L(0, 2, 4, 6)
```

That last functionnality might look extremely wierd, and it does, but it can be practical if used correctly.
If you have a set of objects you iterate over everywhere in the code, that you might change, why not have them all in once place ?
```py
agents = L(...)
ForAllAgents = Map.over(agents)
#...
@ForAllAgents
def training_log(agent):
    #...
    return log_info
print(training_log)
```

## `Map.using`

It is the exact same as `Map.over`, but the argument order is swapped.
```py
@Map.using
def mult_list_by_two(e):
    return e * 2
mult_list_by_two([0, 1, 2, 3]) == L(0, 2, 4, 6)
```

## `Helpers`

```py
from pyqol.FP import Helpers
```

## `.timer`

A simple decorator for debugging the execution time of a function:
```py
@Helpers.timer
def takes_long():
    for i in I(None):
        if i == int(1e12): break;
takes_long() # will print:
# Finished takes_long in x secs
```

# `ML`

A collection of helpers for making Neural Networks !
For now, most of the supported code is in PyTorch, so feel free to sumbit equivalents in other frameworks !

> Requires torch :(

## `PyTorchModules`

```py
from pyqol.ML import PyTorchModules
```

### `.Flatten`
### `.Residual`
### `.LowerBound`
### `.GDN`

# `All`

Easier imports (requires the dependencies from all the modules though..)

```py
from pyqol.All import Struct, Helpers, I, B
```
