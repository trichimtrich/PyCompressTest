#!/usr/bin/python3

""" Benchmark some common compression implemented in Python for your specific usage

- Compression ratio
- Compression speed
- Decompression speed
- memory-profiler / line-profiler / CProfile (?): CPU + Memory + Disk IO

Note:
- Check only for single file compression
- Check only for frame, not stream mode
- Check algorithms supporting stream mode
- Memory leakage might exists, separated library call is a good approach
- No threading involved
- No dictionary involed
- Some wrapper libraries don't provide level/quality selection

Manual:
- pyqlz
https://pypi.org/project/pyqlz/#files
s/malloc.h/stdlib.h/

"""

# - density
# - pithy
# - snappy

# https://pypi.org/project/zstandard/
import zstandard

# https://pypi.org/project/zstd/
import zstd

import timeit


def init_test():
    test_methods = {}

    
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
    # data3 = open("mft.bin", "rb").read()

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