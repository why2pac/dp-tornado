# -*- coding: utf-8 -*-
"""
MVC Web Application Framework with Tornado, Python 2 and 3

To install the package run:

    pip install dp-tornado


Run
-----

    $ pip install virtualenv
    $ virtualenv ./venv
    $ . ./venv/bin/activate
    $ pip install dp-tornado
    $ dp4p init --path app

"""


import sys
import logging


from setuptools import find_packages, setup
import distutils.core as core

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

dp_requires_CyMySQL = 'CyMySQL==0.8.9'
dp_requires_futures = 'futures==3.0.5'


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

        dist = getattr(core, '_setup_distribution', None) if core else None

        if not dist:
            logging.warning('Aditional requires cannot installed.')
        else:
            if self.dp_without_mysql:
                dist.install_requires.remove(dp_requires_CyMySQL)

    def run(self):
        install.run(self)


install_requires = [
        'tornado==4.4.2',
        'redis==2.10.5',
        'requests==2.12.3',
        'croniter==0.3.13',
        'pytz==2016.10',
        'pycrypto==2.6.1',
        'boto3==1.4.2',
        'SQLAlchemy==1.1.4',
        'Pillow==3.4.2',
        'validate_email==1.3',
        'BeautifulSoup4==4.5.1',
        'lxml==3.6.4',
        'httpagentparser==1.7.8',
        'validators==0.11.1',
        dp_requires_CyMySQL,
        # , 'selenium'
    ]


if sys.version_info[0] <= 2:
    install_requires.append(dp_requires_futures)


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
    install_requires=install_requires,
    keywords=['MVC', 'Web Application Framework'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4'
    ],
    entry_points={
        'console_scripts': [
            'dp4p = dp_tornado.cli:main'
        ]
    }
)
