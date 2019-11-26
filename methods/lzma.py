""" lzma

    description:
        builtin python binding for LZMA compression algorithm

    source:
        https://docs.python.org/3/library/lzma.html

    methods:
        lzma.compress(data, preset=...)
            preset in:
                range 0-9
                lzma.PRESET_DEFAULT: 6

        lzma.decompress()
"""

def generate():
    test_methods = {}
    for preset in range(0, 9 + 1):
        test_methods["lzma-{}".format(preset)] = {
            "preload": "import lzma",
            "compress": {
                "func": "lzma.compress",
                "kargs": {
                    "preset": preset,
                },
            },
            "decompress": {
                "func": "lzma.decompress",
            },
        }
    return test_methods
