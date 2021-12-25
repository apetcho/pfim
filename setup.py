#!/usr/bin/env python3
from setuptools import setup
from pfim import PFIM_VERSION

with open("README.md", "r") as fd:
    LONG_DESCRCIPTION = fd.read()



setup(
    name="pfim",
    author="Eyram K. Apetcho",
    author_email="orion2dev@gmail.com",
    url="",
    version=f"{PFIM_VERSION}",
    python_requires=">=3.6",
    license="BSD-2",
    description="Personal Finance Manager",
    long_description=LONG_DESCRCIPTION,
    long_description_content_type="text/markdown",
    platforms=["Windows", "Linux", "Mac OS X"],
    classifiers=[
        "Development Status:: Pre-Alpha",
        "Intended Audience :: Customer Service",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Finance",],
    keywords=["Personal finance manager", "command-line application"],
    tests_require=["pytest"],
    package_dir={"pfim": "pfim"},
    packages=["pfim"],
    )
