"""

	Load the celsus config and repositories.

"""

import os
import json
import zlib
import pdftotext

# Constants
CONFIG_FILE = os.path.expanduser("~/.celsusconfig")
ONLY_KEY = 0
BIB = 1
BIB_AND_CONTENT = 2


# Functions
def get_config():
	""" Returns the celsus config in a dictionary """
	if not os.path.isfile(CONFIG_FILE):
		config = {}
	#
	else:
		with open(CONFIG_FILE, "r") as f:
			config = json.load(f)
		#
	#
	if config.get("editor") is None: config["editor"] = "vi"
	if config.get("viewer") is None: config["viewer"] = "evince"
	return config
#

def write_config(config):
	""" Write the celsus config into the respective user-unique file """
	with open(CONFIG_FILE, "w") as f:
		json.dump(config, f, sort_keys=True, indent='\t')
	#
	return
#

def get_active_repository(config, load=ONLY_KEY):
	""" Load the active repository.
	
	Arguments:
		> config: dictionary containing the celsus config.
		> load=ONLY_KEY: what to load, one of ONLY_KEY, BIB, BIB_AND_CONTENT.
	
	Returns:
		> repository: dictionary storing the keys, bibtexs and contents
		  of the references/documents.
		> path: to the folder containing the repository.
	"""	
	path = config.get("active")
	if path is None:
		raise Exception("No active repository.")
	#

	# Define functions to load the information
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
		load_bib = lambda f: ("", 0)
	#
	if load == BIB_AND_CONTENT:
		def load_content(filename, start):
			""" Reopen file with no buffering and read from start to end """
			with open(filename, "rb", buffering=0) as f:
				f.seek(start)
				content = zlib.decompress(f.read()).decode()
			#
			return content
		#
	#
	else:
		# Dummy function
		load_content = lambda f, start: ""
	#

	# Load
	repository = {}
	for year in os.listdir(path):
		dir = os.path.join(path, year)
		if not (os.path.isdir(dir) and year.isnumeric()):
			raise IOError("The repository must contain directories only (years).")
		#
		# Iterate over files in this dir (or year)
		for filename in os.listdir(dir):
			_, extension = os.path.splitext(filename)
			if extension != ".celsus": continue
			# Load from celsus file
			filename = os.path.join(dir, filename)
			# Key and bib
			with open(filename, "rb", buffering=512) as f:
				key = f.readline()[:-1].decode()
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

def write_celsus_file(path, key, bib):
	""" Augments path with .celsus and writes the required information. """
	# Get pdf as text
	with open(path, "rb") as f:
		pdf = pdftotext.PDF(f)
	#
	text = ('\n'.join(pdf)).encode()
	# Write to celsus file
	path = path + ".celsus"
	with open(path, "wb") as f:
		f.write((
			key + '\n'
			+ str(len(bib)) + '\n'
			+ bib + '\n'
		).encode())
		f.write(zlib.compress(text))
	#
	return
#

