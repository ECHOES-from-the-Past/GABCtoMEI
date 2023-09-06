# https://docs.python.org/3/library/xml.dom.html
# https://www.geeksforgeeks.org/parsing-xml-with-dom-apis-in-python/
# https://lxml.de/xpathxslt.html#regular-expressions-in-xpath
# https://towardsdatascience.com/xpath-for-python-89f4423415e0

from xml.dom import minidom

doc = minidom.parse("ReadyToGo_neumes.mei")

layer_elems = doc.getElementsByTagName("layer")
layer1 = layer_elems[0]
# staff_elems = doc.getElementsByTagName("staff")
# staff1 = staff_elems[0]
#
# neume_elem = doc.createElement('neume')
# neume_elem.setAttribute("syl", "primera")
# nc_elem = doc.createElement('nc')
# neume_elem.appendChild(nc_elem)


# ----------- #
# Definitions #
# ----------- #
regular_pitches = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm']
inclinatum_pitches = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
locs = [-3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
pitches = regular_pitches + inclinatum_pitches

prefixes = ['@']
suffixes = ['~', '>', '<', 'o', 'w', 's', 'v', 'V']
# Missing episema ('_')

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
			locval = locs[regular_pitches.index(item)]
			attributes.append(('loc', str(locval)))
		elif item in inclinatum_pitches:
			locval = locs[inclinatum_pitches.index(item)]
			attributes.append(('loc', str(locval)))
			attributes.append(('tilt', 'se'))
		# Prefixes
		elif item == '@':
			pass
		# Suffixes
		elif item == '~':
			# THE LITTLE ONES ???
			pass
		elif item == '>':
			# liquescent
			pass
		elif item == '<':
			# liquescent
			pass
		elif item == 'o':
			# oriscus
			pass
		elif item == 'w':
			# quilisma
			pass
		elif item == 's':
			# strophicus
			pass
		elif item == 'v':
			attributes.append(('tilt', 's'))
		elif item == 'V':
			attributes.append(('tilt', 'n'))
		else:
			print("this character is not included in the list of processing characters")
	return(attributes)

def convert_to_mei_nc(gabc_nc):
	# DEFINE (EMPTY) NC ELEMENT IN MEI
	mei_nc = doc.createElement('nc') # LIBMEI METHOD
	# ADD ATTRIBUTES TO IT
	attriblist = get_nc_attributes(gabc_nc)
	for attrib in attriblist:
		mei_nc.setAttribute(attrib[0], attrib[1]) # LIBMEI METHOD
	
	return mei_nc


def convert_to_mei_neume(gabc_token):
	# DEFINE (EMPTY) NEUME ELEMENT IN MEI
	mei_neume = doc.createElement('neume') # LIBMEI METHOD
	# FILL IT WITH <NC> CHILDREN
	gabc_ncs_of_neume = get_gabc_ncs(gabc_token)
	for gabc_nc in gabc_ncs_of_neume:
		mei_nc = convert_to_mei_nc(gabc_nc)
		mei_neume.appendChild(mei_nc) # LIBMEI METHOD
	
	return mei_neume

def get_syl_and_neumes(gabc_syllable):
	syl_neumes_pair = gabc_syllable.split('(')
	syl = syl_neumes_pair[0]
	neumes = syl_neumes_pair[1]

	indiv_neumes_list = neumes.split('/')
		
	return syl, indiv_neumes_list


# ------------ #
# Main program #
# ------------ #
line = "(c3) Chris(gvFE)te(gf/ge>) Na(ghg)"

words = line.split()
clef = words[0]

for word in words[1:]:
	#print('The word is: ', word)
	syllables = word.split(')')
	#print(syllables[:-1])
	for gabc_syllable in syllables[:-1]:
		#print(gabc_syllable)
		syllable_mei = doc.createElement('syllable')
		layer1.appendChild(syllable_mei)

		syl_text, indiv_neumes_list = get_syl_and_neumes(gabc_syllable)
		#print(syl)
		#print(indiv_neumes_list)

		syl_mei = doc.createElement('syl')
		text = doc.createTextNode(syl_text)
		syl_mei.appendChild(text)
		syllable_mei.appendChild(syl_mei)
		for gabc_neume in indiv_neumes_list:
			mei_neume = convert_to_mei_neume(gabc_neume)
			syllable_mei.appendChild(mei_neume)


myfile = open("output.mei", "w")
myfile.write(doc.toxml())
myfile.close()