""" zstandard

    description:
        Python bindings for interfacing with the Zstandard compression library
        supports compression level from 1 - 22

    source:
        https://pypi.org/project/zstandard/
        pip install zstandard

    methods:
        zstandard.ZstdCompressor(level=...).compress(data)
            level in:
                range 1-22
                zstandard.MAX_COMPRESSION_LEVEL: 22
                default is 3

        zstandard.ZstdDecompressor().decompress(data)
"""

import zstandard

def _compress(data, level):
    ctx = zstandard.ZstdCompressor(level=level)
    return ctx.compress(data)

def _decompress(data):
    ctx = zstandard.ZstdDecompressor()
    return ctx.decompress(data)

def generate():
    test_methods = {}
    for level in range(1, zstandard.MAX_COMPRESSION_LEVEL + 1):
        test_methods["zstandard-{}".format(level)] = {
            "compress": {
                "func": _compress,
                "args": [level],
            },
            "decompress": {
                "func": _decompress,
            },
        }
    return test_methods
