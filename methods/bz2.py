""" bz2

    description:
        builtin python binding for bzip2 compression algorithm

    source:
        https://docs.python.org/3/library/bz2.html

    methods:
        bz2.compress(data, compresslevel=...)
            preset in:
                range 1-9
                default is 9

        bz2.decompress()
"""

import bz2

def generate():
    test_methods = {}
    for level in range(0, 9 + 1):
        test_methods["bz2-{}".format(level)] = {
            "compress": {
                "func": bz2.compress,
                "kargs": {
                    "compresslevel": level,
                },
            },
            "decompress": {
                "func": bz2.decompress,
            },
        }
    return test_methods
