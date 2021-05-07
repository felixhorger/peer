import setuptools

with open("README.md", "r") as f:
	long_description = f.read()
#

setuptools.setup(
	name="celsus",
	version="1.1",
	description="Scientific reference manager for those with puristic taste.",
	long_description=long_description,
	author="Felix Horger",
	author_email="felix.horger@kcl.ac.uk",
	url="https://github.com/felixhorger/celsus.git",
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
		"Operating System :: POSIX :: Linux"
	],
	packages=["celsus"],
	py_modules=["celsus.utils", "celsus.latex", "celsus.bibtex"],
	scripts=["scripts/celsus"],
	install_requires=["requests", "pylatexenc", "pdfminer.six"],
	python_requires=">=3.6"
)

