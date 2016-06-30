# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='solaris',
    version='0.0.1',
    description='Enviromend for deploying trovit solr',
    long_description=readme,
    author='Albert Vico-Oton',
    author_email='albertvico@trovit.com',
    url='https://github.com/alvico/solaris',
    license=license,
    packages=find_packages(exclude=('tests'))
)
