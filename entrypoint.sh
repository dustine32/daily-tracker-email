#!/bin/sh -l

python3 --version
py_out=$(python3 main.py $1 $2)

echo "::set-output name=py_out::$py_out"
