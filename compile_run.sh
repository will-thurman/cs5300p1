#!/bin/bash

echo
bison -d sql_parser.y
if [ $? -ne 0 ]; then
  echo "Bison Failed! Stopping..."
  exit 1
fi

flex sql_parser.l
if [ $? -ne 0 ]; then
  echo "Flex Failed! Stopping..."
  exit 1
fi

g++ sql_parser.tab.c lex.yy.c -o sqlComp
if [ $? -ne 0 ]; then
  echo "Compiling Failed! Stopping..."
  exit 1
fi

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
