""" pyqlz

    description:
        quicklz binding
        doesn't support compression level, although c api has level from 1 - 3

    source:
        https://pypi.org/project/pyqlz
        code: lib/pyqlz

    methods:
        pyqlz.compress(data)

        pyqlz.decompress(data)
"""

import pyqlz

def generate():
    test_methods = {}
    test_methods["pyqlz"] = {
        "compress": {
            "func": pyqlz.compress,
        },
        "decompress": {
            "func": pyqlz.decompress,
        },
    }
    return test_methods
