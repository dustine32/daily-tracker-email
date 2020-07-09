#!/bin/sh -l

python3 --version
echo "Hello $1"
time=$(date)
echo "::set-output name=time::$time"
