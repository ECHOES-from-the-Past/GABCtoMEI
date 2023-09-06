# https://docs.python.org/3/library/xml.dom.html
# https://www.geeksforgeeks.org/parsing-xml-with-dom-apis-in-python/
# https://lxml.de/xpathxslt.html#regular-expressions-in-xpath
# https://towardsdatascience.com/xpath-for-python-89f4423415e0

from xml.dom import minidom

doc = minidom.parse("ReadyToGo_neumes.mei")
staff_elems = doc.getElementsByTagName("staff")
staff1 = staff_elems[0]

neume_elem = doc.createElement('neume')
neume_elem.setAttribute("syl", "primera")
nc_elem = doc.createElement('nc')
neume_elem.appendChild(nc_elem)


# ----------- #
# Definitions #
# ----------- #
regular_pitches = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm']
inclinatum_pitches = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
pitches = regular_pitches + inclinatum_pitches

prefixes = ['@']
suffixes = ['~', '>', '<', 'o', 'w', 's', 'v', 'V']

# --------- #
# Functions #
# --------- #
def get_gabc_ncs(gabc_token):
	chars_in_token = list(gabc_token)

	ncs_in_token = []
	for i, origchar in enumerate(chars_in_token):
		if ((origchar in pitches) or (origchar in prefixes)):
			ncs_in_token.append(origchar)
		elif (origchar in suffixes):
			ncs_in_token[i-1] = ncs_in_token[i-1] + origchar
		else:
			print('unknown character: ', origchar)

	return ncs_in_token


def get_nc_attributes(gabc_nc):
	characters = list(gabc_nc)
	attributes = []
	for item in characters:
		# Pitches
		if item in regular_pitches:
			attributes.append(('pname', item))
		elif item in inclinatum_pitches:
			attributes.append(('pname', item))
			attributes.append(('tilt', '"se"'))
		# Prefixes
		elif item == '@':
			pass
		# Suffixes
		elif item == '~':
			pass
		elif item == '>':
			pass
		elif item == '<':
			pass
		elif item == 'o':
			pass
		elif item == 'w':
			pass
		elif item == 's':
			pass
		elif item == 'v':
			attributes.append(('tilt', '"s"'))
		elif item == 'V':
			attributes.append(('tilt', '"n"'))
		else:
			print("this character is not included in the list of processing characters")
	return(attributes)

def convert_to_mei_nc(gabc_nc):
	# DEFINE (EMPTY) NC ELEMENT IN MEI
	mei_nc = MeiElement('nc') # LIBMEI METHOD
	# ADD ATTRIBUTES TO IT
	attriblist = get_nc_attributes(gabc_nc)
	for attrib in attriblist:
		mei_nc.addAttribute(attrib[0], attrib[1]) # LIBMEI METHOD
	
	return mei_nc


def convert_to_mei_neume(gabc_token):
	# DEFINE (EMPTY) NEUME ELEMENT IN MEI
	mei_neume = MeiElement('neume') # LIBMEI METHOD
	# FILL IT WITH <NC> CHILDREN
	gabc_ncs_of_neume = get_gabc_ncs(gabc_token)
	for gabc_nc in gabc_ncs_of_neume:
		mei_nc = convert_to_mei_nc(gabc_nc)
		mei_neume.addChild(mei_nc) # LIBMEI METHOD
	
	return mei_neume



# ------------ #
# Main program #
# ------------ #
line = "c3 gvFE gfge> ghg"
list_of_tokens = line.split()
clef = list_of_tokens[0]
mei_neumes = [convert_to_mei_neume(gabc_neume) for gabc_neume in list_of_tokens[1:]]
