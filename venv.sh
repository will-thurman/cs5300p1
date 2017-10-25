#!/bin/bash

if [[ "$(which python3)" == "" ]]
then
  echo "Install python 3 please!"
  exit 1
fi

if [ ! -d env ]
then
  echo "Setting up env"
  virtualenv --python='python3' env
fi

source env/bin/activate

if [ ! -f env/lib/python3.5/site-packages/lark ]
then
  echo "Installing lark"
  pip install lark-parser
fi
