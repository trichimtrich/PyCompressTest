""" pyquicklz

    description:
        quicklz binding
        doesn't support compression level, although c api has level from 1 - 3

    source:
        https://pypi.org/project/pyquicklz
        pip install pyquicklz

    methods:
        quicklz.compress(data)

        quicklz.decompress(data)
"""

import quicklz

def generate():
    test_methods = {}
    test_methods["pyquicklz"] = {
        "compress": {
            "func": quicklz.compress,
        },
        "decompress": {
            "func": quicklz.decompress,
        },
    }
    return test_methods
