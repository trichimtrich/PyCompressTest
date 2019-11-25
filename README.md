# PyCompressTest

Simple script to test performance of some leading compressed algorithms implemented in `Python 3` with your specific data.

## Algorithms

- [brotli](https://brotli.org/)
- [bz2](https://en.wikipedia.org/wiki/Bzip2)
- [lz4](https://lz4.github.io/lz4/)
- [lzma](https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Markov_chain_algorithm)
- [lzo](http://www.oberhumer.com/opensource/lzo/)
- [quicklz](http://www.quicklz.com/)
- [zstandard](https://facebook.github.io/zstd/)
- [zlib](https://www.zlib.net/)

## Concerns

- Compression ratio
- Compression speed
- Decompression speed
- CPU + Memory + Disk IO: Memory-profiler / Line-profiler / CProfile (?)

> ?: Not available

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
- Memory leakage might exists, separated lib call is a good approach
- No threading involved
- No dictionary involed
- Some wrapper libraries don't provide level/quality selection

## Usage

- Create python 3 - `virtualenv` first
- Install libraries. Check `README` in `lib`
- Run test with your data

```bash
python main.py test.dat result1.json
python main.py test_directory/ result2.json
```

## Disclaimer

- Not a bold comparision between algorithms. Only check on Python wrapper level and your specific data
- No optimization and enhancement done