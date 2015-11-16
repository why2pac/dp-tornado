import os

from dp_tornado import __version__

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as README:
    long_description = README.read()

setup(
    name='dp-tornado',
    version=__version__,
    url='http://github.com/why2pac/dp-tornado',
    license='MIT',
    author='YoungYong Park',
    author_email='youngyongpark@gmail.com',
    maintainer='YoungYong Park',
    maintainer_email='youngyongpark@gmail.com',
    description='MVC Web Application Framework with Tornado.',
    long_description=long_description,
    packages=[
        'dp_tornado',
        'dp_tornado/engine',
        'dp_tornado/engine/driver',
        'dp_tornado/engine/plugin',
        'dp_tornado/engine/plugin/compressor',
        'dp_tornado/engine/plugin/compressor/uglifyjs2',
        'dp_tornado/engine/plugin/compressor/uglifyjs2/bin',
        'dp_tornado/engine/plugin/compressor/uglifyjs2/lib',
        'dp_tornado/engine/scheduler',
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
        'SQLAlchemy==1.0.9'
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
