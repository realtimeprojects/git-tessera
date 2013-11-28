#!/usr/bin/python
# -*- coding: utf-8 -*-

from imp import load_source
from setuptools import setup

radish_version = load_source("version", "tessera/version.py")

setup(
    name="radish-bdd",
    version=radish_version.__version__,
    license="GPL",
    description="manage your issues in your repository",
    author="AndrÃ© Roth, Claudio Klingler",
    author_email="neolynx@gmail.com",
    maintainer="AndrÃ© Roth",
    maintainer_email="neolynx@gmail.com",
    platforms=["Linux", "Windows", "MAC OS X"],
    url="https://github.com/neolynx/git-tessera.git",
    download_url="https://github.com/neolynx/git-tessera.git",
    packages=["tessera"],
    entry_points={"console_scripts": ["git-tessera = tessera.main:main"]},
    package_data={"radish": ["tessera"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Operating System :: Microsoft :: Windows :: Windows XP",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: Implementation",
        "Topic :: Education :: Testing",
        "Topic :: Software Development",
        "Topic :: Software Development :: Testing"
    ],
)
