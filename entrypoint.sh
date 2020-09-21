#!/bin/sh -l

python3 --version
python3 -m venv env
. env/bin/activate
pip install -r requirements.txt

py_out=$(python3 main.py $1 $2)

echo "::set-output name=py_out::$py_out"
