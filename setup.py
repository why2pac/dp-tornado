# -*- coding: utf-8 -*-
"""
MVC Web Application Framework with Tornado, Python 2 and 3

To install the package run:

    pip install dp-tornado


Bootstrap Code
-----

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


Run
-----

    $ pip install virtualenv  # if required.
    $ virtualenv ./venv
    $ . ./venv/bin/activate
    $ pip install dp-tornado
    $ python __init__.py

"""


import logging


try:
    from setuptools import setup

except ImportError:
    from distutils.core import setup

try:
    import distutils.core as core
except ImportError:
    core = None

try:
    from setuptools.command.install import install

except ImportError:
    from distutils.command.install import install


with open('dp_tornado/version.py', 'r') as fp_v:
    for c in fp_v.read().split('\n'):
        exec(c)


dp_project_name = 'dp-tornado'
dp_version = __version__
dp_github_url = 'http://github.com/why2pac/dp-tornado'
dp_license = 'MIT'

dp_author = 'Parker'
dp_author_email = 'oss@dp.farm'

dp_maintainer = dp_author
dp_maintainer_email = dp_author_email

dp_description = 'MVC Web Application Framework with Tornado.'

dp_requires_additional = []

CyMySQL = 'CyMySQL==0.8.9'


class CustomInstallCommand(install):
    user_options = install.user_options + [
        ('dp-identifier=', None, 'Specify identifier for dp.'),
        ('dp-without-mysql', None, 'Specify this option if you do not want to install mysql dependency.')
    ]

    def initialize_options(self):
        install.initialize_options(self)

        self.dp_identifier = None
        self.dp_without_mysql = False

    def finalize_options(self):
        install.finalize_options(self)

        if self.dp_without_mysql:
            dp_requires_additional.remove(CyMySQL)

        dist = getattr(core, '_setup_distribution', None) if core else None

        if not dist:
            logging.warning('Aditional requires cannot installed.')
        else:
            if dist.install_requires:
                dist.install_requires += dp_requires_additional
            else:
                dist.install_requires = dp_requires_additional

    def run(self):
        install.run(self)
        install.do_egg_install(self)


setup(
    name=dp_project_name,
    version=dp_version,
    url=dp_github_url,
    license=dp_license,
    author=dp_author,
    author_email=dp_author_email,
    maintainer=dp_maintainer,
    maintainer_email=dp_maintainer_email,
    description=dp_description,
    long_description=__doc__,
    packages=['dp_tornado'],
    include_package_data=True,
    cmdclass={'install': CustomInstallCommand},
    install_requires=[
        'argparse',
        'tornado==4.4.2',
        'redis==2.10.5',
        'requests==2.11.1',
        'croniter==0.3.12',
        'pytz==2016.7',
        'pycrypto==2.6.1',
        'boto3==1.4.1',
        'SQLAlchemy==1.1.2',
        'futures==3.0.5',
        'Pillow==3.4.2',
        'validate_email==1.3',
        'BeautifulSoup4==4.5.1',
        'lxml==3.6.4',
        'httpagentparser==1.7.8',
        'validators==0.11.0',
        CyMySQL
    ],
    keywords=['MVC', 'Web Application Framework'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4'
    ],
)
