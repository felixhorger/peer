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

i = 0
for (key, (file, bib, content)) in repository.items():
	file = os.path.join(path, file)
	#print(bib)
	m = re.search("pages\s*=\s*{[0-9A-z-]*}", bib)
	m2 = re.search("pages\s*=\s*", bib)
	if m is not None or m2 is None: continue
	#
	print(bib)
	print("----------------------")
	print(m2)
	i += 1
	nl = bib.find("\n", m2.end())
	raise Exception("this is not good, as it requires pages to be last, while this seems to be the case for everything I encountered, it's not guaranteed")
	bib = bib[:m2.end()] + "{" + bib[m2.end():nl] + "}" + bib[nl:]
	print(bib)
	text = get_text(file)
	s = input("Replace? (type 'y' for yes, everything else doesn't do anything)")
	if s == "y": write_celsus_file(file, key, bib, text)
#

