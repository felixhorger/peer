.PHONY: publish

dist/celsus-%.tar.gz:
	python3 setup.py sdist
#

dist/celsus-%-py3-none-any.whl:
	python3 setup.py bdist_wheel
#

publish: dist/celsus-%.tar.gz dist/celsus-%-py3-none-any.whl
	python3 -m twine upload --repository testpypi dist/*
#

