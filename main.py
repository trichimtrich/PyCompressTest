#!/usr/bin/python3


import os
import sys
import time
import tempfile

import json
import logging

import subprocess
import psutil

import methods

template = """
import os
import sys
import time
import timeit
import json

%(preload)s

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

def run_test(data_array):
    # cache function
    compress_func = %(c_func)s
    decompress_func = %(dc_func)s
    f_time = timeit.default_timer

    # vars
    len_data = 0
    len_c_data = 0
    sum_c_time = 0
    sum_dc_time = 0

    results = {}
    for fn, data in data_array:
        start_time = time.time()

        # compress
        c_time0 = f_time()
        c_data = compress_func(data%(c_args)s)
        c_time1 = f_time()

        mid_time = time.time()

        # decompress
        dc_time0 = f_time()
        dc_data = decompress_func(c_data%(dc_args)s)
        dc_time1 = f_time()

        end_time = time.time()

        # assume len(dc_data) == len(data)
        if len(dc_data) != len(data):
            continue

        c_len = len(c_data)
        c_time = c_time1 - c_time0 # second
        dc_time = dc_time1 - dc_time0 # second

        del dc_data
        del c_data


        results[fn] = {
            "size": len(data),
            "compressed_size": c_len,
            "compressed_time": c_time,
            "decompressed_time": dc_time,
            "start_time": start_time,
            "mid_time": mid_time,
            "end_time": end_time,
        }

        len_data += len(data)
        len_c_data += c_len
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


def main():
    path = sys.argv[1]
    data_array = read_folder_or_file(path)

    time.sleep(0.5)
    start_test = time.time()
    results = run_test(data_array)
    end_test = time.time()
    results["*"].update({
        "start_test": start_test,
        "end_test": end_test,
    })

    print(json.dumps(results))
    time.sleep(0.5)

if __name__ == "__main__":
    main()
"""


def merge_args_kargs(sub_method):
    # args: list(str)
    # kargs: dict(str: )
    args = sub_method.get("args", [])
    for key, value in sub_method.get("kargs", {}).items():
        args.append("{}={}".format(key, value))
    args.insert(0, "")
    args = map(str, args)

    # data, args0, args1, kargs0=value0, kargs1=value1, ...
    return ", ".join(args)


def run_test(method, path):
    data = template % {
        "preload": method["preload"],
        "c_func": method["compress"]["func"],
        "c_args": merge_args_kargs(method["compress"]),
        "dc_func": method["decompress"]["func"],
        "dc_args": merge_args_kargs(method["decompress"]),
    }
    
    tmp_fn = tempfile.mktemp(".py")
    open(tmp_fn, "w").write(data)

    start_process = time.time()

    program = [sys.executable, tmp_fn, path]
    proc = subprocess.Popen(program, stdout=subprocess.PIPE)

    mem_usage = []
    p = psutil.Process(proc.pid)
    _TWO_20 = float(2 ** 20)
    interval = 0.1

    # https://github.com/pythonprofilers/memory_profiler/blob/1a853e5b1342788fdd6ab55cfe6c568e3b307349/memory_profiler.py#L367
    while True:
        # https://github.com/pythonprofilers/memory_profiler/blob/1a853e5b1342788fdd6ab55cfe6c568e3b307349/memory_profiler.py#L133
        mem = p.memory_info()[0] / _TWO_20
        mem_usage.append(mem)
        time.sleep(interval)
        if proc.poll() is not None:
            break

    stdout = proc.communicate()[0]
    end_process = time.time()

    os.remove(tmp_fn)

    mem_dict = {
        "?": {
            "start_process": start_process,
            "end_process": end_process,
            "mem_usage": mem_usage,
            "interval": interval,
        }
    }

    if stdout.startswith(b"{"):
        test_result = json.loads(stdout)
        if isinstance(test_result, dict) and "*" in test_result:
            test_result.update(mem_dict)
            return test_result
    return mem_dict



def main():
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.DEBUG)

    if len(sys.argv) < 3:
        logging.error("Usage: python {} <data-path> <json-out>".format(sys.argv[0]))
        return

    path = sys.argv[1]
    if not os.path.exists(path):
        logging.error("Not exists path")
        return
 
    test_methods = methods.generate()

    results = {}
    for name, method in test_methods.items():
        logging.info("[+] " + name)
        test_result = run_test(method, path)
        results[name] = test_result

        if "*" in test_result:
            ratio = test_result["*"]["compressed_size"] / test_result["*"]["size"] * 100
            c_speed = test_result["*"]["size"] / test_result["*"]["compressed_time"]
            dc_speed = test_result["*"]["size"] / test_result["*"]["decompressed_time"]

            logging.info(">>> SUM: ratio {:6.3f}% , compress speed {:7.3f} MB/s , decompress speed {:7.3f} MB/s".format(ratio, c_speed / (1024 ** 2), dc_speed / (1024 ** 2)))
        else:
            logging.error("Uknown")

    json_path = sys.argv[2]
    with open(json_path, "w") as f:
        json.dump(results, f)
    
    logging.info("[!] Done")


if __name__ == "__main__":
    main()