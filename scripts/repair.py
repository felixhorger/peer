"""

	Rerun the pdftotext conversion on the currently active repository and make all keys lower case.

"""
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
for (key, (file, bib, _)) in repository.items():
	key = key.lower()
	file = os.path.join(path, file)
	write_celsus_file(file, key, bib)
#

