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