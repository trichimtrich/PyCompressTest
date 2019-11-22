""" py-lz4framed

    description:
        This is an LZ4-frame compression library for Python v3.2+ (and 2.7+), bound to Yann Collet’s LZ4 C implementation
        Supports compression level from 0 to 12

    source:
        https://pypi.org/project/py-lz4framed/
        pip install py-lz4framed

    methods:
        lz4framed.compress(data, level=...)
            level in:
                lz4framed.LZ4F_COMPRESSION_MIN: 0
                lz4framed.LZ4F_COMPRESSION_MAX: 12

                lz4framed.LZ4F_COMPRESSION_MIN_HC: 3

        lz4framed.decompress(data)
"""

import lz4framed

def generate():
    test_methods = {}
    for level in range(lz4framed.LZ4F_COMPRESSION_MIN, lz4framed.LZ4F_COMPRESSION_MAX + 1):
        test_methods["py-lz4framed-{}".format(level)] = {
            "compress": {
                "func": lz4framed.compress,
                "kargs": {"level": level},
            },
            "decompress": {
                "func": lz4framed.decompress,
            },
        }
    return test_methods
