from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'version.txt'), encoding='utf-8') as f:
    version = f.read()

__version__ = version
