#!/bin/bash
VERSION=3.7.3

if [ ! -e Python-$VERSION.tgz ]; then
    wget https://www.python.org/ftp/python/$VERSION/Python-$VERSION.tgz
    tar -zxvf Python-$VERSION.tgz 
fi

cd Python-$VERSION
./configure
make
make test
sudo make altinstall

cd ..
rm -r Python-$VERSION.tgz Python-$VERSION
