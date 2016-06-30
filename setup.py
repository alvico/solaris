# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

SRC_DIR = "src"
MODULE_NAME = "solaris"
__version__ = "0.1.1"

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name=MODULE_NAME,
    version=__version__,
    description="Environment for deploying trovit's solr",
    long_description=readme,
    author='Albert Vico-Oton',
    author_email='albertvico@trovit.com',
    url='https://github.com/alvico/solaris',
    license=license,
    Platform=['MacOs', 'Linux'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Testing :: Tools',
      ],
    packages=['solaris'],
    install_requires=['docker-py==1.8.1',
                      'docopt==0.6.2'],
    entry_points={
        'console_scripts': ['solaris=solaris.cli:main'],
    },
    include_package_data=True,
    zip_safe=False)
