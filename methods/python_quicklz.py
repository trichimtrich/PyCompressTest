""" python-quicklz

    description:
        quicklz binding
        doesn't support compression level, although c api has level from 1 - 3

    source:
        https://github.com/sergey-dryabzhinsky/python-quicklz
        code: lib/python-quicklz
        fix: https://github.com/trichimtrich/python-quicklz


    methods:
        python_quicklz.compress(data, state)

        python_quicklz.decompress(data, state)
"""

def generate():
    test_methods = {}

    test_methods["python-quicklz"] = {
        "preload": "import python_quicklz",
        "compress": {
            "func": "python_quicklz.qlz_compress",
            "args": ["python_quicklz.QLZStateCompress()"],
        },
        "decompress": {
            "func": "python_quicklz.qlz_decompress",
            "args": ["python_quicklz.QLZStateDecompress()"]
        },
    }
    return test_methods
