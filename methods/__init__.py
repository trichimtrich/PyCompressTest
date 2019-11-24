from importlib import import_module

def generate():
    test_methods = {}

    libs = [
        "brotli",
        "bz2",
        "lz4",
        "lz4framed",
        "lz4tools",
        "lzma",
        "lzo",
        "pyqlz",
        "pyquicklz",
        "python_quicklz",
        "zlib",
        "zstandard",
        "zstd",
    ]

    for lib in libs:
        imported_lib = import_module("." + lib, package="methods")
        imported_methods = imported_lib.generate()
        test_methods.update(imported_methods)
    
    return test_methods