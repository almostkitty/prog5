import re
import sys
import requests
from urllib.request import urlopen
from importlib.abc import PathEntryFinder, Loader
from importlib.util import spec_from_loader


class URLFinder(PathEntryFinder):
    def __init__(self, url, available):
        self.url = url
        self.available = available

    def find_spec(self, name, target=None):
        if name in self.available:
            origin = "{}/{}.py".format(self.url, name)
            loader = URLLoader()
            return spec_from_loader(name, loader, origin=origin)
        else:
            return None


class URLLoader(Loader):
    def create_module(self, target):
        return None

    def exec_module(self, module):
        with urlopen(module.__spec__.origin) as page:
            source = page.read()
        code = compile(source, module.__spec__.origin, mode="exec")
        exec(code, module.__dict__)


def url_hook(some_str):
    if not some_str.startswith(("http", "https")):
        raise ImportError

    #with urlopen(some_str) as page:
    #    data = page.read().decode("utf-8")

    try:
        response = requests.get(some_str)
        response.raise_for_status()
        data = response.text

    except requests.RequestException as e:
        print(f"Ошибка: Не удалось подключиться к хосту {some_str}. Причина: {e}")
        raise ImportError(f"Не удалось получить список модулей с {some_str}") from e

    filenames = re.findall("[a-zA-Z_][a-zA-Z0-9_]*.py", data)
    modnames = {name[:-3] for name in filenames}
    return URLFinder(some_str, modnames)


sys.path_hooks.append(url_hook)

sys.path.append("http://localhost:8000")


try:
    from rootserver.myremotemodule import myfoo
    myfoo()
except ImportError:
    print("Ошибка импорта модуля myremotemodule")
except Exception as e:
    print(f"Ошибка при вызове myfoo(): {e}")
