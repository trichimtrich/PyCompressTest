#!/usr/bin/python3

import json
import sys
import re

def main():
    if len(sys.argv) < 3:
        print("Usage: python {} <json-path> <html-out>".format(sys.argv[0]))
        return

    y = open(sys.argv[1], "r").read()
    d = json.loads(y)

    new_data = {}
    keys = []
    max_mem = 0
    for codec, test_result in d.items():
        if re.match("^.+?-\d+", codec):
            # quality / level
            idx = codec.rfind("-")
            name = codec[:idx]
            level = codec[idx + 1 : ]
        else:
            name = codec
            level = ""

        if name not in new_data:
            new_data[name] = []
            keys.append(name)
    
        ratio = test_result["*"]["size"] / test_result["*"]["compressed_size"]
        c_speed = test_result["*"]["size"] / test_result["*"]["compressed_time"]
        dc_speed = test_result["*"]["size"] / test_result["*"]["decompressed_time"]

        mem_usage = test_result["?"]["mem_usage"]
        max_mem = max(max(mem_usage), max_mem)

        interval = test_result["?"]["interval"]

        start_process = test_result["?"]["start_process"]
        end_process = test_result["?"]["end_process"]

        # start time capture when spawning process
        start_process_idx = 0
        end_process_idx = int((end_process - start_process) / interval)
        if end_process_idx >= len(mem_usage):
            # in case we didn't capture full mem usage during the life of process
            end_process_idx = len(mem_usage) - 1
            print("[!] end_process not in range")

        start_test = test_result["*"]["start_test"]
        end_test = test_result["*"]["end_test"]

        # start_process < start_test < end_test < end_process
        start_test_idx = int((start_test - start_process) / interval)
        if start_test_idx < start_process_idx:
            # this is impossible, just to make sure. remember we delay 0.5 after read data into memory
            start_test_idx = start_process_idx
            print("[!] start_test < start_process")

        end_test_idx = int((end_test - start_process) / interval)
        if end_test_idx > end_process_idx:
            # this is impossible, just to make sure. we also delay 0.5 after tests are done
            end_test_idx = end_process_idx
            print("[!] end_test > end_process")

        comp_arr = []
        decomp_arr = []

        for fn, record in test_result.items():
            if fn in ("*", "?"):
                continue
            start_time = record["start_time"]
            mid_time = record["mid_time"]
            end_time = record["end_time"]

            # start_test < start_time < mid_time < end_time < end_test
            start_time_idx = int((start_time - start_process) / interval)
            if start_time_idx < start_test_idx:
                start_time_idx = start_test_idx
                print("[!] ... start_time < start_test")

            end_time_idx = int((end_time - start_process) / interval)
            if end_time_idx > end_test_idx:
                end_time_idx = end_test_idx
                print("[!] ... end_time > end_test")

            mid_time_idx = int((mid_time - start_process) / interval)
            if not (start_time_idx <= mid_time_idx and mid_time_idx <= end_time_idx):
                mid_time_idx = int((start_time_idx + end_time_idx) / 2)
                print("[!] ... mid_time not in [start_time, end_time]")

            comp_arr.append((start_time_idx, mid_time_idx))
            decomp_arr.append((mid_time_idx, end_time_idx))

        new_data[name].append({
            "codec": codec,
            "level": level,
            "compression_rate": c_speed,
            "decompression_rate": dc_speed,
            "ratio": ratio,
            "mem_usage": mem_usage,
            "mem_state": {
                "compression": comp_arr,
                "decompression": decomp_arr,
                "test": (start_test_idx, end_test_idx),
                "process": (start_process_idx, end_process_idx),
            },
        })

    max_mem = (max_mem / 100 + 1) * 100
    x = open("chart.html", "r").read()
    x = x.replace("replace_this_data", json.dumps(new_data))
    x = x.replace("replace_this_keys", json.dumps(keys))
    x = x.replace("replace_this_max", json.dumps(max_mem))

    open(sys.argv[2], "w").write(x)

    print("OK")



if __name__ == "__main__":
    main()