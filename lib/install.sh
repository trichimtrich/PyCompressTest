#!/bin/bash

cat <<EOF
0. alr installed them
1. sudo apt install libsnappy-dev zlib1g-dev liblzo2-dev
2. sudo yum install libsnappy-devel epel-release lzo-devel lzo-minilzo
3. brew install snappy
Choice [0-3] (default 0)?
EOF

read varname

if [ $varname == "1" ]
then
    sudo apt install libsnappy-dev zlib1g-dev liblzo2-dev
elif [ $varname == "2" ]
then
    sudo yum install libsnappy-devel epel-release lzo-devel lzo-minilzo
elif [ $varname == "3" ]
then
    brew install snappy
else
    exit 1
fi



pip install -r requirements.txt
git submodule update --init --recursive

cd pyqlz
python setup.py install

cd ../python-quicklz
python setup.py install

cd ../python-zstd
python setup.py install

cd ..