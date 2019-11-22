__author__ = 'chb'

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

setup(
  name = 'pyqlz',
  version='1.5.0',
  ext_modules=cythonize([
    Extension("pyqlz", ["pyqlz.pyx",'quicklz.c']),
    ])
)