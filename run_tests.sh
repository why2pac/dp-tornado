#!/bin/bash

if [ "$1" = "dry" ]
then
  . ./nodeps/bin/activate
  python -m tests
  deactivate
  
  exit
fi

if [ "$1" = "init" ] || [ "$1" = "all" ]
then
  virtualenv nodeps
fi

. ./nodeps/bin/activate

if [ "$1" = "install" ] || [ "$1" = "all" ]
then
  python setup.py install
fi

./nodeps/bin/nosetests -w ./tests --cover-erase --with-coverage
deactivate
