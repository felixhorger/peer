'''

	Load the celsus config and repositories, write celsus files and other utilities.

'''

import os
import json
import zlib
import subprocess
import celsus
from celsus.bibtex import get_text
# Constants
CONFIG_FILE = os.path.expanduser('~/.celsusconfig')
ONLY_KEY = 0
BIB = 1
BIB_AND_CONTENT = 2


# Functions
def get_config():
	''' Returns the celsus config in a dictionary '''
	if not os.path.isfile(CONFIG_FILE):
		config = {}
	#
	else:
		with open(CONFIG_FILE, 'r') as f:
			config = json.load(f)
		#
	#
	if config.get('editor') is None: config['editor'] = 'vi'
	if config.get('viewer') is None: config['viewer'] = 'evince'
	# Check access to active directory if given
	path = config.get('active')
	if path is not None:
		for dir in [''] + os.listdir(path):
			if os.access(os.path.join(path, dir), os.R_OK | os.W_OK): continue
			raise Exception('Celsus needs r+w rights in the active repository.')
		#
	#
	return config
#

def write_config(config):
	''' Write the celsus config into the respective user-unique file '''
	with open(CONFIG_FILE, 'w') as f:
		json.dump(config, f, sort_keys=True, indent='\t')
	#
	return
#

def get_active_repository(config, load=ONLY_KEY):
	''' Load the active repository.
	
	Arguments:
		> config: dictionary containing the celsus config.
		> load=ONLY_KEY: what to load, one of ONLY_KEY, BIB, BIB_AND_CONTENT
		  or a list/tuple of keys for loading the bibtex only.
	
	Returns:
		> repository: dictionary storing the keys, bibtexs and contents
		  of the references/documents.
		> path: to the folder containing the repository.
	'''	
	path = config.get('active')
	if path is None:
		raise Exception('No active repository.')
	#

	# Define functions to load the information
	keys_to_load = None
	if isinstance(load, (tuple, list)):
		keys_to_load = load
		load = BIB
	#
	if load > ONLY_KEY:
		# Bib or contents must be loaded
		def load_bib(f):
			chars = int(f.readline())
			bib = f.read(chars).decode()
			return bib, chars
		#
	#
	else:
		# Dummy function
		load_bib = lambda f: ('', 0)
	#
	if load == BIB_AND_CONTENT:
		def load_content(filename, start):
			''' Reopen file with no buffering and read from start to end '''
			with open(filename, 'rb', buffering=0) as f:
				f.seek(start)
				content = zlib.decompress(f.read()).decode()
			#
			return content
		#
	#
	else:
		# Dummy function
		load_content = lambda f, start: ''
	#

	# Load
	repository = {}
	for year in os.listdir(path):
		dir = os.path.join(path, year)
		if not (os.path.isdir(dir) and year.isnumeric()):
			raise IOError('The repository must contain directories only (years).')
		#
		# Iterate over files in this dir (or year)
		for filename in os.listdir(dir):
			_, extension = os.path.splitext(filename)
			if extension != '.celsus': continue
			# Load from celsus file
			filename = os.path.join(dir, filename)
			# Key and bib
			with open(filename, 'rb', buffering=512) as f:
				key = f.readline()[:-1].decode()
				if keys_to_load is not None and key not in keys_to_load: continue
				bib, chars = load_bib(f)
			#
			# Content
			content = load_content(filename, len(key)+1 + len(str(chars))+1 + chars+1)
			# Add entry to repository
			filename = filename[len(path):-len(extension)]
			if filename[0] == '/': filename = filename[1:]
			repository[key] = (filename, bib, content)
		#
	#
	return repository, path
#

def write_celsus_file(path, key, bib, text=None):
	''' Augments path with .celsus and writes the required information.
		If text is not None, then the file is not reread.
	'''
	# Get reference as text
	if text is None:
		text = get_text(path)
	#
	text = text.encode()
	# Write to celsus file
	path = path + '.celsus'
	with open(path, 'wb') as f:
		f.write((
			key + '\n'
			+ str(len(bib)) + '\n'
			+ bib + '\n'
		).encode())
		f.write(zlib.compress(text))
	#
	return
#

def open_viewer(path, config):
	''' Opens the given file with the viewer defined in the celsus config.
		Returns the process Popen object.
	'''
	return subprocess.Popen(
		(config['viewer'], path),
		stdout=subprocess.DEVNULL,
		stderr=subprocess.DEVNULL
	)
#

def open_editor(path, config):
	''' Opens the given file in the editor defined in the celsus config.
		Returns the completed process object.
	'''
	return subprocess.run((config['editor'], path))
#

