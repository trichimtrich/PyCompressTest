""" zlib

    description:
        builtin python binding for DEFLATED

    source:
        https://docs.python.org/3/library/zlib.html

    methods:
        zlib.compress(data, level=...)
            level in:
                zlib.Z_BEST_SPEED: 1
                zlib.Z_BEST_COMPRESSION: 9

                zlib.Z_DEFAULT_COMPRESSION: -1 (equal to 6 in scale 1-9)

        zlib.decompress(data)
"""

import zlib

def generate():
    test_methods = {}
    for level in range(zlib.Z_BEST_SPEED, zlib.Z_BEST_COMPRESSION + 1):
        test_methods["zlib-{}".format(level)] = {
            "compress": {
                "func": zlib.compress,
                "kargs": {
                    "level": level,
                }
            },
            "decompress": {
                "func": zlib.decompress,
            },
        }
    return test_methods
