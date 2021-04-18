"""

	Load and write the config of celsus.

"""

import os
import json
from celsus import compressed_json

# Constants
CONFIG_FILE = os.path.expanduser("~/.celsusconfig")

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

def get_active_repository(config):
	""" Load the active repository.
	
	Arguments:
		> config: dictionary containing the celsus config.
	
	Returns:
		> repository: dictionary storing the references.
		> bibs_file: the path to the compressed json file
		  containing repository.
		> path: to the folder containing the repository.
	"""	
	path = config.get("active", None)
	if path is None:
		raise Exception("No active repository.")
	#
	bibs_file = os.path.join(path, "bibs")
	repository = compressed_json.read(bibs_file)
	return repository, bibs_file, path
#

def write_config(config):
	""" Write the celsus config into the respective user-unique file """
	with open(CONFIG_FILE, "w") as f:
		json.dump(config, f, sort_keys=True, indent='\t')
	#
	return
#

