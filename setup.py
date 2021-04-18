#!/usr/bin/env python

from distutils.core import setup

setup(
	name="celsus",
	version="1.0",
	description="Scientific reference manager for those with puristic taste.",
	author="Felix Horger",
	author_email="felix.horger@kcl.ac.uk",
	packages=["celsus"],
	py_modules=["celsus.config", "celsus.latex", "celsus.bibtex", "celsus.compressed_json"],
	scripts=["scripts/celsus"],
	install_requires=["requests", "pylatexenc"]
)

