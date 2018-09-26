#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


project_packages = find_packages(
    exclude=['tests']
)


package_data = {}


install_requirements = [
    'attrs>=18.2',
    'jsonschema>=2.6',
]


setup_requirements = [
    'pytest>=3.8',
    'pytest-cov',
    'pytest-pep8',
    'pytest-mypy'
]


extra_requirements = {}


classifiers = [
    "Development Status :: 1 - Planning"
    "Intended Audience :: Developers"
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7"
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]


setup(
    name='attrs-jsonschema',
    version='0.1.1',
    packages=project_packages,
    url='https://github.com/phuntimes/attrs-jsonschema',
    license='MIT License',
    author='Sean McVeigh',
    author_email='spmcveigh@gmail.com',
    description='Attribute validator for JSON data',
    install_requires=install_requirements,
    setup_requires=setup_requirements,
    extras_require=extra_requirements,
    # include_package_data=True,
    # package_data=package_data,
    classifiers=classifiers,
)
