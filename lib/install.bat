pip install requirements.win.txt
git submodule update --init --recursive

cd pyqlz
python setup.py install

cd ../python-quicklz
python setup.py install

cd ../python-zstd
python setup.py install

cd ../python-snappy
python setup.py install

cd ..