'''

	Handle LaTex expressions

	- replace special LaTex expressions with ASCII characters.
	- replace unicode with LaTex expressions (from package pylatexenc).
	- check if ascii.

'''

import re
from pylatexenc.latexencode import unicode_to_latex

# Regexes
re_accent = re.compile(
	r'{\\('
		'`'
		'|\''
		'|^'
		'|"'
		'|H'
		'|~'
		'|c'
		'|k'
		'|='
		'|b'
		'|\\.'
		'|d'
		'|r'
		'|u'
		'|v'
	')('
		'{[a-zA-Z]}'
		'|[a-zA-Z]'
	')}'
)
re_special = re.compile(
	r'{\\('
	'l{}'
	'|l'
	'|t{[a-zA-Z]{2}}'
	'|o{}'
	'|o'
	'|[ij]'
	'|aa'
	'|AA'
	'|ae'
	'|AE'
	'|dh'
	'|DH'
	'|dj'
	'|DJ'
	'|L'
	'|l'
	'|o'
	'|O'
	'|oe'
	'|OE'
	'|ss'
	'|th'
	'|TH'
	')}'
)
re_paratheses = re.compile(r'{([a-zA-Z])}')

# Functions
def is_non_ascii(s):
	return any(ord(c) >= 128 for c in s)
#

def to_ascii(tex_string):
	''' Replace accented and other special LaTex expressions with ASCII letters. '''
	curated = re_accent.sub(r'\2', tex_string)
	curated = re_special.sub(r'\1', curated)
	curated = re_paratheses.sub(r'\1', curated)
	return curated
#

