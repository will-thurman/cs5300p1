#!/bin/bash
source env/bin/activate
echo "Enter the query, CTRL-D when done"

> test.txt

cat /dev/stdin >> test.txt

echo
echo "---------------------------------"
echo "Query"
cat test.txt
echo
echo "---------------------------------"
echo "Results"
python3 sql_parser.py < test.txt
