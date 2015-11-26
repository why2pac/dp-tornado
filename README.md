# dp-tornado

MVC Web Application Framework with Tornado, Python 2 and 3

To install the package run:

    pip install dp-tornado
    
    
## Bootstrap Code

    # -*- coding: utf-8 -*-
    # __init__.py
    
    
    import os
    
    from dp_tornado import Bootstrap
    
    kwargs = {
        'initialize': True,  # If this value specified True, create default directories and files.
        'application_path': os.path.join(os.path.dirname(os.path.realpath(__file__))),
        'scheduler': [
            ('* * * * *', 'scheduler.foo')
        ]
    }
    
    bootstrap = Bootstrap()
    bootstrap.run(**kwargs)
    
    
## Run

    $ pip install dp-tornado
    $ python __init__.py


## Requisites

- [Python 3.x](https://www.python.org)
- [Python 2.7](https://www.python.org)
- [Minifier](https://www.npmjs.com/package/minifier) Minify CSS, Javascript


## Dependencies

* [tornado](http://www.tornadoweb.org) Network Library
* [SQLAlchemy](http://www.sqlalchemy.org) Model Implementation
* [redis](https://github.com/andymccurdy/redis-py) Redis Cache
* [Croniter](https://pypi.python.org/pypi/croniter/) Scheduler
* [Boto](http://docs.pythonboto.org) AWS Helper
* [Requests](http://docs.python-requests.org) HTTP Reuqest