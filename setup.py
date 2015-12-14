import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

description = 'MVC Web Application Framework with Tornado.'

if os.path.exists('README.md'):
    long_description = open('README.md').read()
else:
    long_description = description

setup(
    name='dp-tornado',
    version="0.2.7",
    url='http://github.com/why2pac/dp-tornado',
    license='MIT',
    author='YoungYong Park',
    author_email='youngyongpark@gmail.com',
    maintainer='YoungYong Park',
    maintainer_email='youngyongpark@gmail.com',
    description=description,
    long_description=long_description,
    packages=[
        'dp_tornado',
        'dp_tornado/engine',
        'dp_tornado/engine/driver',
        'dp_tornado/engine/scheduler',
        'dp_tornado/engine/plugin',
        'dp_tornado/helper',
        'dp_tornado/helper/archive',
        'dp_tornado/helper/aws',
        'dp_tornado/helper/i18n',
        'dp_tornado/helper/validator'],
    include_package_data=True,
    install_requires=[
        'tornado==4.3',
        'redis==2.10.3',
        'requests==2.8.1',
        'croniter==0.3.8',
        'boto==2.38.0',
        'SQLAlchemy==1.0.9',
        'futures==3.0.3'
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
