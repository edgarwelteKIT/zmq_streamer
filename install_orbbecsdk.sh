#!/bin/bash

# check if .venv directory exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi
# Activate the virtual environment
source .venv/bin/activate

# Follow the instructions to install the Orbbec SDK: 
# https://orbbec.github.io/pyorbbecsdk/source/2_installation/build_the_package.html

git clone https://github.com/orbbec/pyorbbecsdk.git
cd pyorbbecsdk
git checkout v2-main
pip install -r requirements.txt
mkdir -p build && cd build
cmake -Dpybind11_DIR=$(pybind11-config --cmakedir) ..
make -j$(nproc)
make install