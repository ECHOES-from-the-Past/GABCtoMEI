# https://docs.python.org/3/library/xml.dom.html
# https://www.geeksforgeeks.org/parsing-xml-with-dom-apis-in-python/
# https://lxml.de/xpathxslt.html#regular-expressions-in-xpath
# https://towardsdatascience.com/xpath-for-python-89f4423415e0
import argparse
from xml.dom import minidom

doc = minidom.parse("template.mei")

layer_elems = doc.getElementsByTagName("layer")
layer1 = layer_elems[0]


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


def get_nc_qualities(gabc_nc):
	characters = list(gabc_nc)
	features = []
	for item in characters:

		# Pitches
		if item in regular_pitches:
			# loc attribute
			locval = locs[regular_pitches.index(item)]
			attribute = ('loc', str(locval))
			features.append(attribute)
		elif item in inclinatum_pitches:
			# loc attribute
			locval = locs[inclinatum_pitches.index(item)]
			attribute = ('loc', str(locval))
			features.append(attribute)
			# tilt attribute
			attribute = ('tilt', 'se')
			features.append(attribute)

		# Prefixes
		elif item == '@':
			pass
		# Suffixes
		elif item == '~':
			# liquescent
			nc_type = doc.createElement('liquescent') # LIBMEI METHOD
			features.append(nc_type)
		elif item == '>':
			# liquescent
			nc_type = doc.createElement('liquescent') # LIBMEI METHOD
			features.append(nc_type)
		elif item == '<':
			# liquescent
			nc_type = doc.createElement('liquescent') # LIBMEI METHOD
			features.append(nc_type)
		elif item == 'o':
			# oriscus
			nc_type = doc.createElement('oriscus') # LIBMEI METHOD
			features.append(nc_type)
		elif item == 'w':
			# quilisma
			nc_type = doc.createElement('quilisma') # LIBMEI METHOD
			features.append(nc_type)
		elif item == 's':
			# strophicus
			nc_type = doc.createElement('strophicus') # LIBMEI METHOD
			features.append(nc_type)
		elif item == 'v':
			# tilt attribute
			attribute = ('tilt', 's')
			features.append(attribute)
		elif item == 'V':
			# tilt attribute
			attribute = ('tilt', 'n')
			features.append(attribute)
		else:
			print("this character is not included in the list of processing characters")

	return(features)

def convert_to_mei_nc(gabc_nc):
	# DEFINE (EMPTY) NC ELEMENT IN MEI
	mei_nc = doc.createElement('nc') # LIBMEI METHOD

	# ADD CHARACTERISTICS TO IT
	qualities = get_nc_qualities(gabc_nc)
	for feature in qualities:
		if (type(feature) == tuple):
			# Then it is an attribute, and you add it to the <nc>
			mei_nc.setAttribute(feature[0], feature[1]) # LIBMEI METHOD
		else:
			# Then it is an element, and you add it as a child of <nc>
			mei_nc.appendChild(feature) # LIBMEI METHOD

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

# gabc_line = "(c3) Chris(gvFE)te(gf/ge>) Na(ghg)"
# mei_file = out.mei

# gabc_line = "(f2) Be(e!E!fv)ne(dev)di(ghv)ci(g!E)te(fff!d/ed) om(g)nes(g) An(ijv)ge(h)li(g) Do(h)mi(g)ni(f) Do(h/ih)mi(g/hg)num(g) hym(g)num(g) di(ijv)ci(h!g)te(g!h!/iwjvi!i!h) et(h) su(i/ji)pe(g)re(h)xal(g)ta(f!ghv)te(h) e(g!e/f!ed!ev)um(e!d) in(e/f!f!f!d/ghv) se(g!f/g/hg)cu(e/gf!f)la(fe)"
# mei_file = aquit1_82441.mei

# gabc_line = "(f2) Ec(d)ce(c/fe) vir(fe~)go(d) con(cev)ci(ghv)pi(g!e)et(f!e/fd) et(dev) pa(g!ghv/j!jkv!h)ri(ghv)et(h) fi(h!g)li(hiwj!h)um(h) et(h) vo(h!g)ca(j!j)bi((h!g)tur(j!j!ih!iv) no(g!h/ih)men(f!f!E) e(g/ih)jus(h!g) Em(fgve!d)ma(d!f!ghv)nu(f!e!d)el(d)"
# mei_file = aquit10_84614.mei

# gabc_line = "(f2) Ec(d)ce(d/fe) vir(fg~)go(d) con(cev)ci(ghv)pi(g!e)et(f!e/fd) et(cev) pa(g!hjv/j/kh)ri(ghv)et(h) fi(h)li(h!ghv/i/jh)um(h) et(h/ih~) vo(jj)ca(h!g)bi(I!hiv)tur(g!hiv/ioh) no(f!E)men(ge~) ej(fhv/i!hg)us(h!g) Em(f/ge/eod)ma(d!fghv)nu(f!E)el(d)"
# mei_file = aquit11_84548.mei

def main(gabc_line, mei_file):
	words = gabc_line.split()
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

	myfile = open(mei_file, "w")
	myfile.write(doc.toxml())
	myfile.close()



# if __name__ == "__main__":
# 	parser = argparse.ArgumentParser(description='GABC file to MEI Neumes file')
# 	parser.add_argument('gabc', help='GABC line')
# 	parser.add_argument('mei_output', help='MEI output file')
# 	args = parser.parse_args()
# 	main(args.gabc, args.mei_output)

# 	# python3 gabc-tokens_to_mei-elements.py "(c3) Chris(gvFE)te(gf/ge>) Na(ghg)" out.mei
# 	# python3 gabc-tokens_to_mei-elements.py "(f2) Be(e!E!fv)ne(dev)di(ghv)ci(g!E)te(fff!d/ed) om(g)nes(g) An(ijv)ge(h)li(g) Do(h)mi(g)ni(f) Do(h/ih)mi(g/hg)num(g) hym(g)num(g) di(ijv)ci(h!g)te(g!h!/iwjvi!i!h) et(h) su(i/ji)pe(g)re(h)xal(g)ta(f!ghv)te(h) e(g!e/f!ed!ev)um(e!d) in(e/f!f!f!d/ghv) se(g!f/g/hg)cu(e/gf!f)la(fe)" aquit1_82441.mei
# 	# python3 gabc-tokens_to_mei-elements.py "(f2) Ec(d)ce(c/fe) vir(fe~)go(d) con(cev)ci(ghv)pi(g!e)et(f!e/fd) et(dev) pa(g!ghv/j!jkv!h)ri(ghv)et(h) fi(h!g)li(hiwj!h)um(h) et(h) vo(h!g)ca(j!j)bi((h!g)tur(j!j!ih!iv) no(g!h/ih)men(f!f!E) e(g/ih)jus(h!g) Em(fgve!d)ma(d!f!ghv)nu(f!e!d)el(d)" aquit10_84614.mei
# 	# python3 gabc-tokens_to_mei-elements.py "(f2) Ec(d)ce(d/fe) vir(fg~)go(d) con(cev)ci(ghv)pi(g!e)et(f!e/fd) et(cev) pa(g!hjv/j/kh)ri(ghv)et(h) fi(h)li(h!ghv/i/jh)um(h) et(h/ih~) vo(jj)ca(h!g)bi(I!hiv)tur(g!hiv/ioh) no(f!E)men(ge~) ej(fhv/i!hg)us(h!g) Em(f/ge/eod)ma(d!fghv)nu(f!E)el(d)" aquit11_84548.mei
