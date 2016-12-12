.. title:: dp-tornado

dp-tornado
==========

MVC Web Application Framework with Tornado, Python 2 and 3

Environment Setup
-----------------

Virtualenv::

    $ pip install virtualenv
    $ virtualenv ./venv
    $ . ./venv/bin/activate

Install dp-tornado::

    $ pip install dp-tornado


Run
---

Startup::

    $ dp4p init app_dir
    $ dp4p run app_dir

or::

    $ dp4p init --path app_dir --template=bbs
    $ dp4p run --path app_dir --template=bbs

or::

    $ mkdir app_dir
    $ cd app_dir
    $ dp4p init
    $ dp4p run


with Docker::

    $ docker pull why2pac/dp4p:latest-py34  # py27, py34, py35, pypy27
    $ docker run --name "dp4p-example" -d -p 8080:52848 -v "$(pwd)/app_dir:/data/app" why2pac/dp4p:latest-py34


Documentation
-------------

.. toctree::
   :titlesonly:

   mvc
   ini
   config
   helper
   scheduler
   schema
   cache
   m17n
   vars
   logging
   testing

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`