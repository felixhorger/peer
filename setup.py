#!/usr/bin/env python

from distutils.core import setup
from shutil import rmtree

setup(
	name="Peer",
	version="1.0",
	description="Puristic, easy and enjoyable reference-manager.",
	author="Felix Horger",
	author_email="felix.horger@kcl.ac.uk",
	scripts=["scripts/peer"]
)

rmtree("build")
