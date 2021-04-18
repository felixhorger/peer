"""

	Functionality to read and write json into compressed files.

"""

import json
import zlib

def read(filename):
	""" zlib compressed json file -> object """
	with open(filename, "rb") as f:
		obj = json.loads(zlib.decompress(f.read()).decode())
	#
	return obj
#

def write(filename, obj):
	""" object -> zlib compressed json file """
	with open(filename, "wb") as f:
		f.write(zlib.compress(json.dumps(obj).encode()))
	#
	return
#

