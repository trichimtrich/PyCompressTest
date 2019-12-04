# PyCompressTest

Simple script to test performance of some leading compressed algorithms implemented in `Python 3` with your specific data.

## Algorithms

- [brotli](https://brotli.org/)
- [bz2](https://en.wikipedia.org/wiki/Bzip2)
- [lz4](https://lz4.github.io/lz4/)
- [lzma](https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Markov_chain_algorithm)
- [lzo](http://www.oberhumer.com/opensource/lzo/)
- [quicklz](http://www.quicklz.com/)
- [snappy](https://github.com/google/snappy)
- [zstandard](https://facebook.github.io/zstd/)
- [zlib](https://www.zlib.net/)

## Concerns

- Compression ratio
- Compression speed
- Decompression speed
- Memory usage during compressing/decompressing
- Memory leakage ?

> ?: Manual by generating chart

## Scenarios

### 1. Single file

- Simple compress
- Simple decompress

### 2. Single directory

#### a) Compress -> Archive

- Compress/Decompress each files
- Combine result (size / time) together
- Same as `zipfile` module in theory

#### b) Archive -> Compress

- Not implemented yet
- Same as `tarfile` module in theory

## Notes

- Check only for single file compression
- Check only for frame, not stream mode
- Haven't checked if algorithms/libs support stream mode
- No threading involved
- No dictionary involed
- Some wrapper libraries don't provide level/quality selection
- Time measuring is the most precise timer in Python, use `timeit.default_timer`. Can get rid of several opcode circles (in between assign operator and calling function) by using C implementation, but no need if test data is big enough
- Memory measuring is not precise (0.1s interval), because using `psutil` method. Can use `tracemalloc` for native measuring but will affect clock timing
- Charts are directly cloned from [squash-benchmark-result](https://quixdb.github.io/squash-benchmark/#ratio-vs-decompression)

## Usage

- Create python 3 - `virtualenv` first
- Install libraries. Check `README` in `lib`
- Run test with your data

```bash
python main.py test.dat result1.json
python main.py test_directory/ result2.json
```

- Visualization

```bash
python chart.py result1.json result1.html
python chart.py result2.json result2.html
```

## Disclaimer

- Not a bold comparision between algorithms. Only check on Python wrapper level and your specific data
- The results are not consistent between small and large test data. Better use data that needs at least 2s of computing for each codec
- No optimization and enhancement have made