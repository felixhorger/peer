
Celsus - Scientific reference manager for those with puristic taste.
=====================================================

The name is derived from the ancient roman library of Celsus.

**Work in progress, bug reports welcome**

Aim
---
Stores documents and bibtex information of scientific references (papers, books, etc.) in a database.
Users can add documents alongside unique keys which can be DOIs, arXiv IDs or manually defined expressions.
Bibtex information is automatically loaded from doi.org, arxiv.org or can be added manually.
Files are moved into a user-defined directory and renamed consistently.
Functionality to open documents will follow.

Installation
------------

1. `git clone` this repository.
2. `cd` to the root directory of the repository.
3. `python3 setup.py install --user`

Usage
-----

Run `celsus` or `celsus --help`


To Do
-----
- Enable entry deletion and modification.
- Set up template for manual bibtex entry.
- Outsource functionality, create module which is used by the script.
- Incorporate automatic DOI and arXiv ID finder (from pdf).

