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
    version="0.8.9.1",
    url='http://github.com/why2pac/dp-tornado',
    license='MIT',
    author='YoungYong Park',
    author_email='oss@dp.farm',
    maintainer='YoungYong Park',
    maintainer_email='oss@dp.farm',
    description=description,
    long_description=long_description,
    packages=[
        'dp_tornado',
        'dp_tornado/engine',
        'dp_tornado/engine/driver',
        'dp_tornado/engine/scheduler',
        'dp_tornado/engine/schema',
        'dp_tornado/engine/schema/driver',
        'dp_tornado/engine/plugin',
        'dp_tornado/helper',
        'dp_tornado/helper/archive',
        'dp_tornado/helper/aws',
        'dp_tornado/helper/i18n',
        'dp_tornado/helper/image',
        'dp_tornado/helper/image/resize',
        'dp_tornado/helper/validator'],
    include_package_data=True,
    install_requires=[
        'argparse',
        'tornado==4.4.1',
        'redis==2.10.5',
        'requests==2.11.1',
        'croniter==0.3.12',
        'pytz==2016.6.1',
        'boto==2.42.0',
        'boto3==1.4.0',
        'SQLAlchemy==1.0.15',
        'futures==3.0.5',
        'Pillow==3.3.1'
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
