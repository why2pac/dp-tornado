#!/bin/bash

if [ "$1" = "" ]
then
  mode="install"
else
  mode="$1"
fi

if [ "$mode" = "dry" ]
then
 
  for py_ver in 2.7 3.6; do

    . ./nodeps/$py_ver/bin/activate
    python -m tests
    deactivate
  
  done  

  return
fi

if [ "$mode" = "init" ] || [ "$mode" = "all" ]
then
  rm -rf builds
  rm -rf dist
  rm -rf dp_tornado.egg-info
  rm -rf nodeps
  virtualenv nodeps/2.7 --python=python2.7
  virtualenv nodeps/3.6 --python=python3.6
  brew install phantomjs
fi

for py_ver in 2.7 3.6; do

  . ./nodeps/$py_ver/bin/activate

  if [ "$mode" = "install" ] || [ "$mode" = "all" ] || [ "$mode" = "init" ]
  then
    python setup.py install > /dev/null 2>&1
    pip install nose > /dev/null 2>&1
    pip install selenium > /dev/null 2>&1
  fi

  ./nodeps/$py_ver/bin/nosetests -w ./tests --cover-erase
  deactivate

done
