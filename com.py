#!/usr/bin/python3

""" Benchmark some common compression implemented in Python for your specific usage

- Compression ratio
- Compression speed
- Decompression speed
- CProfile (?): CPU + Memory + Disk

Note:
- Check only for single file compression
- Check only for frame, not stream mode, which maybe different a bit in production
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

# https://github.com/sergey-dryabzhinsky/python-quicklz
import quicklz

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

import time

def init_test():
    test_methods = {}

    # brotli
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

    # lz4
    for level in range(0, 16 + 1):
        test_methods["lz4-{}".format(level)] = {
            "compress": {
                "func": lz4.frame.compress,
                "kargs": {"compression_level": level},
            },
            "decompress": {
                "func": lz4.frame.decompress,
            },
        }

    # lz4framed
    for level in range(0, 16 + 1):
        test_methods["lz4framed-{}".format(level)] = {
            "compress": {
                "func": lz4framed.compress,
                "kargs": {"level": level},
            },
            "decompress": {
                "func": lz4framed.decompress,
            },
        }

    # zstandard
    test_methods["zstandard"] = {
        "compress": {"func": zstandard.compress},
        "decompress": {
            "func": zstandard.decompress,
        },
    }

    # zstd
    test_methods["zstd"] = {
        "compress": {"func": zstd.compress},
        "decompress": {
            "func": zstd.decompress,
        },
    }

    return test_methods

def measure_func(func, args, kargs):
    t0 = time.time()
    ret = func(*args, **kargs)
    t1 = time.time()
    return ret, t1 - t0


def run_single_test(method, data):
    compress_func = method["compress"]["func"]
    compress_args = method["compress"].get("args", []) # type: list
    compress_kargs = method["compress"].get("kargs", {}) # type: dict
    c_data, c_time = measure_func(compress_func, [data, *compress_args], compress_kargs)

    ratio = len(c_data) / len(data) * 100
    # c_time = c_time * 1000 # ms
    # print(">>> Compression: time {0:.3f} ms -- ratio {1:.2f}".format(c_time, ratio))


    decompress_func = method["decompress"]["func"]
    decompress_args = method["decompress"].get("args", []) # type: list
    decompress_kargs = method["decompress"].get("kargs", {}) # type: dict
    dc_data, dc_time = measure_func(decompress_func, [c_data, *decompress_args], decompress_kargs)

    # dc_time = dc_time * 1000 # ms
    # print(">>> Decompression: time {0:.3f} ms".format(dc_time))

    return ratio, c_time, dc_time



def main():
    data1 = open("com_data1.json", "rb").read()
    data2 = open("com_data2.exe", "rb").read()
    data3 = open("com_data3.bin", "rb").read()

    test_methods = init_test()
    for name, method in test_methods.items():
        ratio, c_time, dc_time = run_single_test(method, data1)
        c_mbs = len(data) / c_time / 1024 / 1024
        dc_mbs = len(data) / dc_time / 1024 / 1024
        print("[+] {0}: ratio {1:.2f}% , compress speed {2:.2f} MB/s , decompress speed {3:.2f} MB/s".format(name, ratio, c_mbs, dc_mbs))
        break


if __name__ == "__main__":
    main()