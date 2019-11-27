#!/bin/bash

pip install -r requirements.txt
git submodule update --init --recursive

cd pyqlz
python setup.py install

cd ../python-quicklz
python setup.py install

cd ../python-zstd
python setup.py install

cd ..