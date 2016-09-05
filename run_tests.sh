#!/bin/bash

if [ "$1" = "dry" ]
then
  . ./nodeps/bin/activate
  python -m tests
  deactivate
  
  exit
fi

virtualenv nodeps
. ./nodeps/bin/activate
python setup.py install
./nodeps/bin/nosetests -w ./tests --with-coverage
deactivate
