##############################################################################
#
# Copyright (c) 2008 Agendaless Consulting and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the BSD-like license at
# http://www.repoze.org/LICENSE.txt.  A copy of the license should accompany
# this distribution.  THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL
# EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND
# FITNESS FOR A PARTICULAR PURPOSE
#
##############################################################################

from setuptools import setup, find_packages


def readfile(name):
    with open(name) as f:
        return f.read()


README = readfile("README.rst")
CHANGES = readfile("CHANGES.rst")

tests_require = [
    "zope.testrunner",
]

setup(
    name="repoze.sphinx.autointerface",
    version="1.0.0",
    description="Sphinx extension: auto-generates API docs from Zope interfaces",
    long_description=README + "\n\n" + CHANGES,
    long_description_content_type='text/x-rst',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    keywords="web wsgi zope Sphinx",
    author="Agendaless Consulting",
    author_email="repoze-dev@lists.repoze.org",
    url="https://github.com/repoze/repoze.sphinx.autointerface/",
    project_urls={
        "Documentation": "https://github.com/repoze/repoze.sphinx.autointerface/",
        "Changelog": "https://github.com/repoze/repoze.sphinx.autointerface/blob/master/CHANGES.rst",
        "Issue Tracker": "https://github.com/repoze/repoze.sphinx.autointerface/issues",
    },
    license="BSD-derived (Repoze)",
    packages=find_packages(),
    include_package_data=True,
    namespace_packages=["repoze", "repoze.sphinx"],
    zip_safe=False,
    python_requires=">=3.6",
    tests_require=tests_require,
    install_requires=[
        "zope.interface",
        "Sphinx >= 4.0",
        "setuptools",
    ],
    extras_require={
        "test": tests_require,
    },
)
