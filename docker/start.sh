#!/bin/bash
LD_RUN_PATH=/usr/local/lib sqlite-autoconf-3380200/configure --enable-optimizations
export LD_LIBRARY_PATH="/usr/local/lib"
git clone http://github.com/Kevin-Duarte/link-router
python ./link-router/main.py
