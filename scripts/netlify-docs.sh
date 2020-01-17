#!/usr/bin/env bash
set -x
set -e
# Install pip
cd /tmp
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.6 get-pip.py --user
cd -
# Install Flit to be able to install all
python3.6 -m pip install --user flit
# Install with Flit
python3.6 -m flit install --user --extras doc
# Finally, run mkdocs
python3.6 -m mkdocs build
