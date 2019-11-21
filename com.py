#!/usr/bin/python3

""" Benchmark some common compression implemented in Python for your specific usage

- Compression ratio
- Compression speed
- Decompression speed
- memory-profiler / line-profiler / CProfile (?): CPU + Memory + Disk IO

Note:
- Check only for single file compression
- Check only for frame, not stream mode, which maybe different a bit in production
- Memory leakage might exists, separated library call is a good approach

Manual:
- pyqlz
https://pypi.org/project/pyqlz/#files
s/malloc.h/stdlib.h/

"""

# https://github.com/google/brotli/tree/master/python
import brotli

# - density

# https://pypi.org/project/lz4/
import lz4.frame

# https://pypi.org/project/py-lz4framed/
import lz4framed

# https://pypi.org/project/python-lzo/
import lzo

# - pithy

# TODO: check which version
# https://pypi.org/project/pyquicklz/#files
# https://github.com/robottwo/quicklz
# https://github.com/sergey-dryabzhinsky/python-quicklz
import quicklz

# https://pypi.org/project/pyqlz/
import pyqlz

# - snappy

# builtins
import lzma
import bz2
import zlib
# - zlib-ng

# https://pypi.org/project/zstandard/
import zstandard

# https://pypi.org/project/zstd/
import zstd


import timeit


def init_test():
    test_methods = {}

    """ brotli

        brotli.compress(data, quality=...)
            quality: 0 - 11
        
        brotli.decompress(data)
    """
    for quality in range(0, 11 + 1):
        test_methods["brotli-{}".format(quality)] = {
            "compress": {
                "func": brotli.compress,
                "kargs": {"quality": quality},
            },
            "decompress": {
                "func": brotli.decompress,
            },
        }


    """ lz4

        lz4.frame.compress(data, level=...)
            level in:
                lz4.frame.COMPRESSIONLEVEL_MIN: 0
                lz4.frame.COMPRESSIONLEVEL_MAX: 16

                lz4.frame.COMPRESSIONLEVEL_MINHC: 3
        
        lz4.frame.decompress(data)
    """
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


    """ py-lz4framed

        lz4framed.compress(data, level=...)
            level in:
                lz4framed.LZ4F_COMPRESSION_MIN: 0
                lz4framed.LZ4F_COMPRESSION_MAX: 12

                lz4framed.LZ4F_COMPRESSION_MIN_HC: 3

        lz4framed.decompress(data)
    """
    for level in range(lz4framed.LZ4F_COMPRESSION_MIN, lz4framed.LZ4F_COMPRESSION_MAX + 1):
        test_methods["py-lz4framed-{}".format(level)] = {
            "compress": {
                "func": lz4framed.compress,
                "kargs": {"level": level},
            },
            "decompress": {
                "func": lz4framed.decompress,
            },
        }


    """ python-lzo
    
        lzo.compress(data, level)
            level: 1 - 9

        lzo.decompress(data)
    """
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


    """ pyqlz

        pyqlz.compress(data)

        pyqlz.decompress(data)
    """
    test_methods["pyqlz"] = {
        "compress": {
            "func": pyqlz.compress,
        },
        "decompress": {
            "func": pyqlz.decompress,
        },
    }


    """ zstandard

        zstandard.compress(data)

        zstandard.decompress(data)
    """
    test_methods["zstandard"] = {
        "compress": {
            "func": zstandard.compress,
        },
        "decompress": {
            "func": zstandard.decompress,
        },
    }


    """ zstd

        zstd.compress(data)

        zstd.decompress(data)
    """
    test_methods["zstd"] = {
        "compress": {
            "func": zstd.compress,
        },
        "decompress": {
            "func": zstd.decompress,
        },
    }

    return test_methods


def measure_func(func, args, kargs):
    t0 = timeit.default_timer()
    ret = func(*args, **kargs)
    t1 = timeit.default_timer()
    return ret, t1 - t0


def run_single_test(method, data):
    compress_func = method["compress"]["func"]
    compress_args = method["compress"].get("args", []) # type: list
    compress_kargs = method["compress"].get("kargs", {}) # type: dict
    c_data, c_time = measure_func(compress_func, [data, *compress_args], compress_kargs)

    decompress_func = method["decompress"]["func"]
    decompress_args = method["decompress"].get("args", []) # type: list
    decompress_kargs = method["decompress"].get("kargs", {}) # type: dict
    dc_data, dc_time = measure_func(decompress_func, [c_data, *decompress_args], decompress_kargs)

    ratio = len(c_data) / len(data) * 100

    return ratio, c_time, dc_time



def main():
    data1 = open("com_data1.json", "rb").read()
    # data2 = open("com_data2.exe", "rb").read()
    # data3 = open("com_data3.bin", "rb").read()
    data3 = open("mft.bin", "rb").read()

    test_methods = init_test()
    data = data1

    data = b"a" * (10 * 1024 * 1024)

    for name, method in test_methods.items():
        ratio, c_time, dc_time = run_single_test(method, data)
        c_mbs = len(data) / c_time / 1024 / 1024
        dc_mbs = len(data) / dc_time / 1024 / 1024
        print("[+] {0}: ratio {1:.3f}% , compress speed {2:.3f} MB/s , decompress speed {3:.3f} MB/s".format(name, ratio, c_mbs, dc_mbs))


if __name__ == "__main__":
    main()