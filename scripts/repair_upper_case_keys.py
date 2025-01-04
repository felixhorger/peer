import re
import sys
import os
from celsus.utils import (
	get_config,
	get_active_repository,
	BIB,
	write_celsus_file,
	get_text
)

config = get_config()
repository, path = get_active_repository(config, load=BIB)

keys = [k.lower() for k in repository.keys()]
assert(len(set(keys)) == len(keys))


for (key, (file, bib, content)) in repository.items():
	file = os.path.join(path, file)
	if any(c.isupper() for c in key):
		key = key.lower()
		text = get_text(file)
		write_celsus_file(file, key, bib, text)
		print(key, file, bib)
	#
#

