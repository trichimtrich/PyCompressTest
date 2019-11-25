# Testing libraries

## Information

### python-quicklz

- Change module name to `python_quicklz` for importing

- Commit [45806bd13d654fa883ce64dc59d4e14b4005acd5](https://github.com/sergey-dryabzhinsky/python-quicklz/tree/45806bd13d654fa883ce64dc59d4e14b4005acd5)

- Checkout [repo](https://github.com/trichimtrich/python-quicklz)

### pyqlz

- Fix the uncompile-able code

- [pyqlz-1.5.5.tar.gz](https://files.pythonhosted.org/packages/ef/cc/4d04d7e4ab9ee83e51af37d8fc90b7d6a5b46b3e47cb83c60f340f53d5ee/pyqlz-1.5.5.tar.gz)

- Install `Cython` first

- Checkout [repo](https://github.com/trichimtrich/pyqlz)

### python-zstd

- Change module name to `python_zstd` to avoid conflict with `zstandard` library.

- Checkout [repo](https://github.com/trichimtrich/python-zstd)

### python-snappy

- Add instruction for Windows

### Others

In `requirements.txt`

- brotli
- lz4
- py-lz4framed
- lz4tools (not fixed)
- pyquicklz
- zstandard

And `builtins`

- zlib
- lzma
- bz2

## Installation

> Do both

### From Pypi

- Pip `requirements.win.txt` for Windows

- Pip `requirements.txt` for Linux/MacOS

### Modified libraries

```bash
cd <lib-name>
git submodule update --init
python setup.py install
```