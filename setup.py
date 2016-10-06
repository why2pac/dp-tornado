import os
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


description = 'MVC Web Application Framework with Tornado.'

if os.path.exists('README.md'):
    long_description = open('README.md').read()
else:
    long_description = description

dp_requires_additional = []


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

        if not self.dp_without_mysql:
            dp_requires_additional.append('CyMySQL==0.8.9')

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
    name='dp-tornado',
    version="0.8.9",
    url='http://github.com/why2pac/dp-tornado',
    license='MIT',
    author='YoungYong Park',
    author_email='oss@dp.farm',
    maintainer='YoungYong Park',
    maintainer_email='oss@dp.farm',
    description=description,
    long_description=long_description,
    packages=[
        'dp_tornado'],
    include_package_data=True,
    cmdclass={
        'install': CustomInstallCommand,
    },
    install_requires=[
        'argparse',
        'tornado==4.4.2',
        'redis==2.10.5',
        'requests==2.11.1',
        'croniter==0.3.12',
        'pytz==2016.7',
        'boto==2.42.0',
        'boto3==1.4.0',
        'SQLAlchemy==1.1.0',
        'futures==3.0.5',
        'Pillow==3.4.1'
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
