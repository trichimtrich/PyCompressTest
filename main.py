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

import os
import sys
import timeit
import methods
import json
import logging


def measure_func(func, args, kargs):
    t0 = timeit.default_timer()
    ret = func(*args, **kargs)
    t1 = timeit.default_timer()
    return ret, t1 - t0


def run_single_test(method, data_array):
    len_data = 0
    len_c_data = 0
    sum_c_time = 0
    sum_dc_time = 0

    results = {}

    count = 0
    for fn, data in data_array:
        compress_func = method["compress"]["func"]
        compress_args = method["compress"].get("args", []) # type: list
        compress_kargs = method["compress"].get("kargs", {}) # type: dict
        c_data, c_time = measure_func(compress_func, [data, *compress_args], compress_kargs)

        decompress_func = method["decompress"]["func"]
        decompress_args = method["decompress"].get("args", []) # type: list
        decompress_kargs = method["decompress"].get("kargs", {}) # type: dict
        dc_data, dc_time = measure_func(decompress_func, [c_data, *decompress_args], decompress_kargs)

        assert len(dc_data) == len(data), "Wtf, decompress bi khung ?"

        results[fn] = {
            "size": len(data),
            "compressed_size": len(c_data),
            "compressed_time": c_time,
            "decompressed_time": dc_time,
        }

        count += 1
        ratio = len(c_data) / len(data) * 100
        c_speed = len(data) / c_time
        dc_speed = len(data) / dc_time
        logging.debug("{:3d}/{:<3d}: ratio {:6.3f}% , compress speed {:7.3f} MB/s , decompress speed {:7.3f} MB/s".format(count, len(data_array), ratio, c_speed / (1024 ** 2), dc_speed / (1024 ** 2)))

        len_data += len(data)
        len_c_data += len(c_data)
        sum_c_time += c_time
        sum_dc_time += dc_time

    # avoid conflict with path
    results["*"] = {
        "size": len_data,
        "compressed_size": len_c_data,
        "compressed_time": sum_c_time,
        "decompressed_time": sum_dc_time,
    }

    return results


def read_folder_or_file(path):
    data_array = []
    if os.path.isdir(path):
        for root, folders, files in os.walk(path):
            for f in files:
                fn = os.path.join(root, f)
                data = open(fn, "rb").read()
                if not data:
                    continue
                data_array.append([fn, data])
    else:
        data_array.append([path, open(path, "rb").read()])

    return data_array


def main():
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.DEBUG)

    if len(sys.argv) < 3:
        logging.error("Usage: python {} <data-path> <json-out>".format(sys.argv[0]))
        return

    path = sys.argv[1]
    # path = os.path.abspath(sys.argv[1])
    if not os.path.exists(path):
        logging.error("Not exists path")
        return

    data_array = read_folder_or_file(path)
    test_methods = methods.generate()

    results = {}
    for name, method in test_methods.items():
        logging.info("[+] " + name)
        test_result = run_single_test(method, data_array)
        results[name] = test_result

        ratio = test_result["*"]["compressed_size"] / test_result["*"]["size"] * 100
        c_speed = test_result["*"]["size"] / test_result["*"]["compressed_time"]
        dc_speed = test_result["*"]["size"] / test_result["*"]["decompressed_time"]

        logging.info(">>> SUM: ratio {:6.3f}% , compress speed {:7.3f} MB/s , decompress speed {:7.3f} MB/s".format(ratio, c_speed / (1024 ** 2), dc_speed / (1024 ** 2)))

    json_path = sys.argv[2]
    with open(json_path, "w") as f:
        json.dump(results, f)
    
    logging.info("[!] Done")


if __name__ == "__main__":
    main()