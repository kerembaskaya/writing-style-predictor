import sys
from os.path import abspath
from os.path import dirname
from os.path import join

try:
    import style
except ModuleNotFoundError:
    base_path = abspath(dirname(dirname(__file__)))
    sys.path.insert(1, base_path)
    import style
