#!/usr/bin/env python

from distutils.core import setup
from shutil import rmtree

setup(
	name="celsus",
	version="1.0",
	description="Scientific reference manager for those with puristic taste.",
	author="Felix Horger",
	author_email="felix.horger@kcl.ac.uk",
	scripts=["scripts/celsus"]
)

