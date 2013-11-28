#!/usr/bin/python
# -*- coding: utf-8 -*-

from imp import load_source
from setuptools import setup

radish_version = load_source("version", "radish/version.py")

setup(
    name="radish-bdd",
    version=radish_version.__version__,
    license="GPL",
    description="Behaviour-Driven-Development tool for python",
    author="Timo Furrer",
    author_email="tuxtimo@gmail.com",
    maintainer="Timo Furrer",
    maintainer_email="tuxtimo@gmail.com",
    platforms=["Linux", "Windows", "MAC OS X"],
    url="http://github.com/timofurrer/radish",
    download_url="http://github.com/timofurrer/radish",
    #install_requires=["docopt==0.6.1", "lxml==3.2.1"],
    install_requires=["docopt==0.6.1"],
    package_dir={"radish.singleton": "radish/pysingleton/singleton"},
    packages=["radish", "radish.singleton"],
    entry_points={"console_scripts": ["radish = radish.main:main"]},
    package_data={"radish": ["*.md"]},
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
