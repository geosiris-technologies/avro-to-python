#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
import os

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Jinja2==3.1.2', 'Click==8.1.3', 'anytree==2.8.0',  'nested-lookup==0.2.25', 'typingx==0.6.0', 'wheel==0.33.6']

test_requirements = [
    'pip==19.2.3',
    'bump2version==1.0.1',
    'Click==8.1.3',
    'coverage==6.4.4',
    'flake8==5.0.4',
    'Jinja2==3.0.3',
    'pytest-runner==6.0.0',
    'pytest==7.1.3',
    'Sphinx==5.1.1',
    'tox==3.26.0',
    'twine==4.0.1',
    'watchdog==2.1.9'
]

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
elif os.environ.get('CI_JOB_ID'):
    version = os.environ['CI_JOB_ID']
else:
    version = '0.0.0'

setup(
    author="Scott Rothbarth",
    author_email='srserves85@gmail.com',
    python_requires='>3.5, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="avro-to-rust-etp is a light tool for compiling avro schema files (.avsc) to rust classes making using avro schemata easy.",
    entry_points={
        'console_scripts': [
            'avro-to-rust-etp=avro_to_rust_etp.cli:main',
            'avpr-to-avsc=avro_to_rust_etp.avpr_to_avsc:main'
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='avro-to-rust-etp',
    name='avro_to_rust_etp',
    packages=find_packages(include=['avro_to_rust_etp', 'avro_to_rust_etp.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/srserves85/avro-to-rust_etp',
    version=version,
    zip_safe=False,
)
