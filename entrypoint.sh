#!/bin/sh -l

python3 --version
python3 -m venv env
. env/bin/activate
pip install -r requirements.txt

issue_email_body=$(python3 main.py $1 $2)
issue_email_body=$(cat $issue_email_body | sed 's/\n/%0A/g')

echo "::set-output name=issue_email_body::$issue_email_body"
