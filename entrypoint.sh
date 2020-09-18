#!/bin/sh -l

python3 --version
py_out=$(python3 test_main.py $1)
echo "Hello $1"
time=$(date)
echo "::set-output name=time::$time"
echo "::set-output name=py_out::$py_out"
