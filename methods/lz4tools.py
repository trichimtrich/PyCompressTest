""" lz4tools

    description:
        binding for lz4-frame algorithm in python
        doesn't support compression level at the moment
        supports interface for cli / tarfile

    source:
        https://pypi.org/project/lz4tools/
        pip install lz4tools

    methods:
        lz4f.compressFrame(data)
        
        lz4f.decompressFrame(data)

    note:
        doesn't work well on windows. ignore !
"""

try:
    import lz4f
except:
    pass
import os

def generate():
    test_methods = {}
    
    if os.name == "nt":
        return test_methods

    test_methods["lz4tools"] = {
        "compress": {
            "func": lz4f.compressFrame,
        },
        "decompress": {
            "func": lz4f.decompressFrame,
        },
    }
    return test_methods
