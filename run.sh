#!/bin/bash

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
sqlComp < test.txt

