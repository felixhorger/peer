'''

	Get and parse bibtex entries.

	Bibtex entries can be retrieved from:
		- doi.org
		- arxiv.org

	Parsing:
		- Get the citation key, author and year
		  of the publication (LaTex expressions NOT supported).
		- Check if a code is DOI or arXiv ID.
		- Get DOI or arXiv ID from pdf.

	Regexes:
		- re_author, re_year: match author and year.
		- re_citation_key: match the citation key.
		- re_doi: match if the code is a DOI.
		- re_arxiv: match if the code is an arXiv ID, without the 'arXiv:' prefix.
		- re_(doi|arxiv)_in_text: match if DOI or arXiv ID is found in text,
		  delimited by whitespaces or in URL.

	For convenience, an empty bib entry (article) is provided.
	Also, the generator 'gen_letters' is useful to produce unique citation keys.

'''

import os
import re
import bs4
import string
import requests
import datetime
from math import log
import celsus
from celsus.latex import to_ascii

# Constants
empty_bib_article = (
	'@article{,\n'
		'\tdoi = {},\n'
		'\turl = {},\n'
		'\tyear = {},\n'
		'\tmonth = {},\n'
		'\tpublisher = {},\n'
		'\tvolume = {},\n'
		'\tnumber = {},\n'
		'\tpages = {},\n'
		'\tauthor = {},\n'
		'\ttitle = {},\n'
		'\tjournal = {}\n'
	'}'
)

# Regexes
re_author = re.compile(r'\s+author[\s={\']+([\w\-\s\.,]+?)(\s+and\s+|\s*[\'}]).*')
re_year = re.compile(r'\s*year[\s={\']+([0-9]+).*')
re_citation_key = re.compile(r'\s*@[a-zA-Z]+{(.*?),.*')
re_doi = re.compile(r'10\.[0-9\.]+/[-_;:\.<>/()0-9a-zA-Z]+$')
re_arxiv = re.compile(r'[0-9]{2}(0[1-9]|1[0-2])\.[0-9]{4,5}(v[1-9]{1}|)$')

# Functions
def doi2bib(doi):
	''' string DOI -> bibtex entry string

		Loads the bibtex entry from doi.org.
		Returns empty string if failing to do so.
	'''
	website = requests.get(
		'https://dx.doi.org/' + doi,
		headers={'accept': 'application/x-bibtex'}
	)
	if not website.ok:
		return ''
	#
	return website.text
#

def arxiv2bib(arxiv_id):
	''' string arxiv_id -> bibtex entry string, pdf url

		Loads the bibtex entry from arxiv.org.
		Returns an empty string if failing to do so.
		The prefix 'arXiv:' is to be omitted in the ID.
	'''
	website = requests.get('https://arxiv.org/abs/' + arxiv_id)
	if not website.ok:
		return ''
	#
	soup = bs4.BeautifulSoup(website.text, 'lxml')
	citation = {
		'archivePrefix': 'arXiv',
		'eprint': arxiv_id,
		'author': []
	}
	url = None
	for tag in soup.find_all('meta'):
		name = tag.get('name', None)
		if name is None or name.find('citation') == -1: continue
		name = name.replace('citation_', '')
		if name == 'pdf_url':
			url = tag.get('content')
			continue
		#
		if name not in ['title', 'author', 'date']: continue
		if name == 'author':
			citation['author'].append(tag.get('content'))
		#
		elif name == 'date':
			date = tag.get('content')
			date = datetime.datetime.strptime(date, '%Y/%m/%d')
			citation['year'] = date.strftime('%Y')
			citation['month'] = date.strftime('%b').lower()
		#
		else:
			citation[name] = tag.get('content')
		#
	#
	citation['author'] = ' and '.join(citation['author'])
	bib = (
		'@article{' + arxiv_id + ',\n'
		+ ',\n'.join(['\t{} = {{{}}}'.format(key, value) for key, value in citation.items()])
		+ '\n}'
	)
	return bib, url
#

def is_doi(doi):
	return True if re_doi.match(doi) is not None else False
#

def is_arxiv(id):
	return True if re_arxiv.match(id) is not None else False
#

def parse(bib):
	''' bib string -> citation key (index returned if the is no key), author, year ''' 
	author = None
	year = None
	citation_key = None
	bib = to_ascii(bib)
	for line in bib.split('\n'):
		if author is None:
			a = re_author.match(line)
			if a is not None:
				# Would be too easy if there was a single convention
				author = a.groups()[0]
				if ',' in author:
					author = author.split()[0].replace(',', '')
				#
				else:
					author = author.split()[-1]
				#
				continue
			#
		#
		if year is None:
			y = re_year.match(line)
			if y is not None:
				year = y.groups()[0]
			#
			continue
		#
		if citation_key is None:
			k = re_citation_key.match(bib)
			if k is not None:
				start = k.start(1)
				end = k.end(1)
				if start != end:
					citation_key = bib[start:end]
				#
				else:
					citation_key = start
					# If no key is present, give the index.
				#
			#
		#
	#
	return citation_key, author, year
#

# Useful for generating citation keys
def gen_letters():
	''' Generator for letter combinations: '', 'a', 'b', ... 'z', 'aa', 'ab', ... '''
	letters = ('',) + tuple(string.ascii_lowercase)
	L = len(letters)
	log_base = log(L)
	i = 0
	while True:
		order = int(log(max(i,1)) / log_base)
		for k in range(order, 0, -1):
			m = L**k
			if (i % m) == 0:
				i += m // L
			#
		#
		code = ''
		j = i
		for k in range(order, 0, -1):
			m = L**k
			code = letters[j // m] + code
			j = j % m
		#
		yield code + letters[j]
		i += 1
	#
	return # Never happening
#

