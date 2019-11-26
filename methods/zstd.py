""" zstd

    description:
        Python bindings for interfacing with the Zstandard compression library
        supports compression level from 1 - 22

    source:
        https://github.com/sergey-dryabzhinsky/python-zstd
        code: lib/python-zstd
        fix: https://github.com/trichimtrich/python-zstd


    methods:
        python_zstd.compress(data, level...)
            level in 1 - 22

        python_zstd.decompress(data)
"""

def generate():
    test_methods = {}
    for level in range(1, 22 + 1):
        test_methods["zstd-{}".format(level)] = {
            "preload": "import python_zstd",
            "compress": {
                "func": "python_zstd.compress",
                "args": [level],
            },
            "decompress": {
                "func": "python_zstd.decompress",
            },
        }
    return test_methods
