"""setup file for wir vs virus."""

import os

from setuptools import setup
import pathlib

tests_require = ["pytest", "coverage"]

check_requires = ["black", "isort", "flake8", "mypy"]

dev_requires = ["hupper", "pdbpp"] + check_requires + tests_require

def read(fname):
    """utility function to read the readme file.
    used for the long_description.  it's nice, because now 1) we have a top level
    readme file and 2) it's easier to type in the readme file than to put a raw
    string in below ...
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()



setup(
    name="wirvsvirus",
    version="0.0.1",
    author="bla",
    author_email="bla@example.com",
    description="wirvsvirus",
    packages=["wirvsvirus"],
    package_dir={"wirvsvirus": "wirvsvirus"},
    long_description=read("README.md"),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
    ],
    extras_require={"dev": dev_requires, "check": check_requires, "test": tests_require},
    tests_require=tests_require,
    entry_points={"console_scripts": "wirvsvirus=wirvsvirus.cli:cli"},
)
