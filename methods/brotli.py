""" brotli

    description:
        brotli algorithm, python binding implemented by Google
        supports quality from 0 to 11

    source:
        https://github.com/google/brotli/tree/master/python
        pip install brotli

    methods:
        brotli.compress(data, quality=...)
            quality: 0 - 11
        
        brotli.decompress(data)
"""

import brotli

def generate():
    test_methods = {}
    for quality in range(0, 11 + 1):
        test_methods["brotli-{}".format(quality)] = {
            "compress": {
                "func": brotli.compress,
                "kargs": {"quality": quality},
            },
            "decompress": {
                "func": brotli.decompress,
            },
        }
    return test_methods
