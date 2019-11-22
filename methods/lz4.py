""" lz4

    description:
        Python standard handlers
        This Python interface currently supports the frame and block formats
        Supports compression elvel from 0 to 16

    source:
        https://pypi.org/project/lz4/
        pip install lz4

    methods:
        lz4.frame.compress(data, level=...)
            level in:
                lz4.frame.COMPRESSIONLEVEL_MIN: 0
                lz4.frame.COMPRESSIONLEVEL_MAX: 16

                lz4.frame.COMPRESSIONLEVEL_MINHC: 3
        
        lz4.frame.decompress(data)
"""

import lz4.frame

def generate():
    test_methods = {}
    for level in range(lz4.frame.COMPRESSIONLEVEL_MIN, lz4.frame.COMPRESSIONLEVEL_MAX + 1):
        test_methods["lz4-{}".format(level)] = {
            "compress": {
                "func": lz4.frame.compress,
                "kargs": {"compression_level": level},
            },
            "decompress": {
                "func": lz4.frame.decompress,
            },
        }
    return test_methods
