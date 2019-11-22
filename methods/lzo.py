""" python-lzo

    description:
        Python bindings for the LZO data compression library
        compression level from 1 - 9

    source:
        https://github.com/jd-boyd/python-lzo
        pip install python-lzo

    methods:
        lzo.compress(data, level)
            level: 1 - 9

        lzo.decompress(data)
"""

import lzo

def generate():
    test_methods = {}
    for level in range(1, 9 + 1):
        test_methods["python-lzo-{}".format(level)] = {
            "compress": {
                "func": lzo.compress,
                "args": [level],
            },
            "decompress": {
                "func": lzo.decompress,
            },
        }
    return test_methods
