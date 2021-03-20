
import re
import functools
import inspect

#? Self-Modifying code
def codedit(find, replace, namespace=globals()):
    def wrapper(f):
        #! Only works for global functions !
        if hasattr(f, "source"):
            source = f.source
        else:
            source_lines, _ = inspect.getsourcelines(f)
            while source_lines[0][0] == "@":
                source_lines = source_lines[1:]
            source = "".join(source_lines)
        new = re.sub(find, replace, source)
        exec(new, namespace)
        namespace[f.__name__] = eval(f.__name__)
        namespace[f.__name__].source = new
        return namespace[f.__name__]
    return wrapper

from pyqol.Bittors import I

#* Codedit modules
_Get_Torch_Modules = lambda: {
    "Linear": (r'Lin *@ *(.*) *>> *(.*) \| *"(.*)"', r"nn.Linear(\1, \2)"),
    "Conv2d": (r'Conv2d *@(.*)>>(.*) *\|(.*) *\| *(.*) *\| *(.*)\| *"(.*)"', r"nn.Conv2d(\1, \2, \3, \4)")
}
class Codedits():
    @staticmethod
    def Lambda(lambda_symbol):
        return codedit(r"{(.*)" + lambda_symbol + r"(.*)}", r"lambda \1: \2")
    @staticmethod
    def TorchBasics(names=_Get_Torch_Modules(), namespace=globals()):
        def wrapper(f):
            for module in _Get_Torch_Modules():
                if module in names:
                    f = codedit(*names[module], namespace=namespace)(f)
            return f
        return wrapper
Codedits.TorchGate = codedit(r"Gate *\[(.*) << (.*)\] *\|(.*)\|(.*)#", r"Gate([\1 for _ in I(\2)], \3, output_dims=[\4])")
