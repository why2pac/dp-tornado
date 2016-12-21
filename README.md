# dp-tornado

[![Pypi Status](https://img.shields.io/pypi/v/dp-tornado.svg)](https://pypi.python.org/pypi/dp-tornado)
[![Build Status](https://travis-ci.org/why2pac/dp-tornado.svg?branch=master)](https://travis-ci.org/why2pac/dp-tornado)
[![Docs](https://readthedocs.org/projects/dp-tornado/badge/?version=latest)](http://dp-tornado.readthedocs.io)
[![Requirements Status (Master)](https://requires.io/github/why2pac/dp-tornado/requirements.svg?branch=master)](https://requires.io/github/why2pac/dp-tornado/requirements/?branch=master)
[![Requirements Status (Develop)](https://requires.io/github/why2pac/dp-tornado/requirements.svg?branch=develop)](https://requires.io/github/why2pac/dp-tornado/requirements/?branch=develop)
[![Coverage Status](https://coveralls.io/repos/github/why2pac/dp-tornado/badge.svg?branch=master)](https://coveralls.io/github/why2pac/dp-tornado?branch=master)

MVC Web Application Framework with Tornado, Python 2 and 3

To install the package run:

    pip install dp-tornado
    
    
## Environment Setup

Virtualenv:

    $ pip install virtualenv
    $ virtualenv ./venv
    $ . ./venv/bin/activate
    
Install dp-tornado:

    $ pip install dp-tornado


## Run
    
Startup:
    
    $ dp4p init app_dir
    $ dp4p run app_dir
    
or:
    
    $ dp4p init --path app_dir
    $ dp4p run --path app_dir
    
or:
    
    $ mkdir app_dir
    $ cd app_dir
    $ dp4p init
    $ dp4p run
    

## Run with Docker ([hub.docker](http://hub.docker.com/r/why2pac/dp4p))

Find out more information about dp4p docker, [Here.](http://hub.docker.com/r/why2pac/dp4p) 

    $ docker pull why2pac/dp4p:latest-py34  # py27, py34, py35, pypy27
    $ docker run --name "dp4p-example" -d -p 8080:52848 -v "$(pwd)/app_dir:/data/app" why2pac/dp4p:latest-py34
    


### Inspired by

[David](https://github.com/youngyoon), [Matthew](https://github.com/Matthew-Kwon) and [Max](https://github.com/leadermin)
