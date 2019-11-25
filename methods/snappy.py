""" python-snappy

    description:
        snappy algorithm implemented in Python
        only 1 selection

    source:
        https://pypi.org/project/python-snappy/
        pip install python-snappy
        code: lib/python-snappy

    methods:
        snappy.compress(data)
        
        snappy.decompress(data)
"""

import snappy

def generate():
    test_methods = {}
    test_methods["python-snappy"] = {
        "compress": {
            "func": snappy.compress,
        },
        "decompress": {
            "func": snappy.decompress,
        },
    }
    return test_methods
