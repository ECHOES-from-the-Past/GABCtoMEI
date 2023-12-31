# https://docs.python.org/3/library/xml.dom.html
# https://www.geeksforgeeks.org/parsing-xml-with-dom-apis-in-python/
# https://lxml.de/xpathxslt.html#regular-expressions-in-xpath
# https://towardsdatascience.com/xpath-for-python-89f4423415e0
import argparse
import uuid
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

prefixes = ['@', 'º']
suffixes = ['~', '>', '<', 'o', 'w', 's', 'v', 'V', 'r', 'x', 'y', '#']
# Missing episema ('_')

clef_to_pitch = {
    'C1': ['g2', 'a2', 'b2', 'c3', 'd3', 'e3', 'f3', 'g3', 'a3', 'b3', 'c4', 'd4', 'e4'],
    'C2': ['e2', 'f2', 'g2', 'a2', 'b2', 'c3', 'd3', 'e3', 'f3', 'g3', 'a3', 'b3', 'c4'],
    'C3': ['c2', 'd2', 'e2', 'f2', 'g2', 'a2', 'b2', 'c3', 'd3', 'e3', 'f3', 'g3', 'a3'],
    'C4': ['a1', 'b1', 'c2', 'd2', 'e2', 'f2', 'g2', 'a2', 'b2', 'c3', 'd3', 'e3', 'f3'],
    'F2': ['a2', 'b2', 'c3', 'd3', 'e3', 'f3', 'g3', 'a3', 'b3', 'c4', 'd4', 'e4', 'f4'],
    'F3': ['f2', 'g2', 'a2', 'b2', 'c3', 'd3', 'e3', 'f3', 'g3', 'a3', 'b3', 'c4', 'd4'],
    'F4': ['d2', 'e2', 'f2', 'g2', 'a2', 'b2', 'c3', 'd3', 'e3', 'f3', 'g3', 'a3', 'b3'],
} # locs = [-3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# token is a neume (so everything separated by '/')
# get_gabc_ncs(gabc_token or gabc_neume)
# --------- #
# Functions #
# --------- #
def get_gabc_ncs(gabc_token):
    chars_in_token = list(gabc_token)
    ncs_in_token = [] # list of the neume components (ncs) in the neume (token)
    prevchar = '' # initializing variable

    # Evaluate each character to see if they fall in the following categories:
    for origchar in chars_in_token:
        # Prefixes
        if (origchar in prefixes):
            ncs_in_token.append(origchar)
        # Pitches
        elif (origchar in pitches):
            if (prevchar in prefixes):
                ncs_in_token[-1] = ncs_in_token[-1] + origchar
            else:
                ncs_in_token.append(origchar)
        # Suffixes
        elif (origchar in suffixes):
            ncs_in_token[-1] = ncs_in_token[-1] + origchar
        # Anything else
        else:
            print('unknown character: ', origchar)
        
        # Update previous character
        prevchar = origchar

    print('ncs in neume token:', ncs_in_token)
    return ncs_in_token


def get_nc_qualities(gabc_nc):
    characters = list(gabc_nc)
    features = []
    for charitem in characters:

        # Pitches
        if charitem in regular_pitches:
            # loc attribute
            locval = locs[regular_pitches.index(charitem)]
            attribute = ('loc', str(locval))
            features.append(attribute)
        elif charitem in inclinatum_pitches:
            # loc attribute
            locval = locs[inclinatum_pitches.index(charitem)]
            attribute = ('loc', str(locval))
            features.append(attribute)
            # tilt attribute
            attribute = ('tilt', 'se')
            features.append(attribute)

        # Prefixes
        elif charitem == '@':
            pass
        elif charitem == 'º':
            # first nc of the pair with @ligated = true
            attribute = ('ligated', 'true')
            features.append(attribute)
        # Suffixes
        elif charitem == '~':
            # liquescent
            nc_type = doc.createElement('liquescent_type_tilde') # LIBMEI METHOD
            features.append(nc_type)
        elif charitem == '>':
            # nc with @curve = c
            attribute = ('curve', 'c')
            features.append(attribute)
            # liquescent
            nc_type = doc.createElement('liquescent') # LIBMEI METHOD
            features.append(nc_type)
        elif charitem == '<':
            # nc with @curve = a
            attribute = ('curve', 'a')
            features.append(attribute)
            # liquescent
            nc_type = doc.createElement('liquescent') # LIBMEI METHOD
            features.append(nc_type)
        elif charitem == 'o':
            # oriscus
            nc_type = doc.createElement('oriscus') # LIBMEI METHOD
            features.append(nc_type)
        elif charitem == 'w':
            # quilisma
            nc_type = doc.createElement('quilisma') # LIBMEI METHOD
            features.append(nc_type)
        elif charitem == 's':
            # strophicus
            nc_type = doc.createElement('strophicus') # LIBMEI METHOD
            features.append(nc_type)
        elif charitem == 'v':
            # tilt attribute
            attribute = ('tilt', 's')
            features.append(attribute)
        elif charitem == 'V':
            # tilt attribute
            attribute = ('tilt', 'n')
            features.append(attribute)
        elif charitem == 'r':
            # cavum (empty note) - used for unclear neume components
            # <nc> <unclear/> </nc>
            nc_type = doc.createElement('unclear') # LIBMEI METHOD
            features.append(nc_type)
        # Elements that are not children of <nc>
        # They are either preceding siblings (like <accid>)
        # or parents of the <nc> (none at the moment)
        elif charitem == 'x':
            # flat: <accid accid="f"/>
            accid = doc.createElement('accid') # LIBMEI METHOD
            features.append(["accid", ('accid', 'f')])
        elif charitem == 'y':
            # natural: <accid accid="n"/>
            accid = doc.createElement('accid') # LIBMEI METHOD
            features.append(["accid", ('accid', 'n')])
        elif charitem == '#':
            # sharp: <accid accid="s"/>
            accid = doc.createElement('accid') # LIBMEI METHOD
            features.append(["accid", ('accid', 's')])
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
        elif (type(feature) == list):
            if (feature[0] == "accid"):
                mei_nc.tagName = "accid"
                mei_nc.setAttribute(feature[1][0], feature[1][1])
            else:
                print("WHAT IS THIS?!\n")
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


# ---------------------------------------- #
#  Flavoring MEI (to square or aquitanian) #
# ---------------------------------------- #
def encode_liquescent_curve_for_tilde():
    liquescent_tilde_elems = doc.getElementsByTagName("liquescent_type_tilde")

    for liquescent_tilde in liquescent_tilde_elems:
        nc2 = liquescent_tilde.parentNode
        nc1 = nc2.previousSibling

        loc1 = int(nc1.getAttribute('loc'))
        loc2 = int(nc2.getAttribute('loc'))

        # PES = Melody goes Up, ASCENDING pair of neume componentes
        if(loc2 > loc1):
            # If the second nc (the one with the liquescent) is a virga
            if((nc2.getAttribute('tilt')) and ('n' in nc2.getAttribute('tilt'))):
                # Then nc2 has @cuve=c (in addition to the @tilt="ne" and the <liquescent> child)
                nc2.setAttribute('curve', 'c')
            # Default
            else:
                # nc1 with @curve = a (while nc2 has the <liquescent> child)
                nc1.setAttribute('curve', 'a')

        # CLIVIS = Melody goes Down, DESCENDING pair of neume componentes
        else:
            # nc1 has nothing AND nc2 (with the <liquescent> child) has the @curve = c
            nc2.setAttribute('curve', 'c')

        # Change to a regular <liquescent> element
        liquescent_tilde.tagName = 'liquescent'


def encode_obliqua_ligatures():
    # Add the @ligated=true to the second neume component of the pair of obliqua ligated components
    square_neumes = doc.getElementsByTagName("neume")
    for sq_neume in square_neumes:
        save = -20
        sq_ncs = sq_neume.childNodes
        for i, nc in enumerate(sq_ncs):
            if (nc.getAttribute('ligated') and nc.getAttribute('ligated') == 'true'):
                save = i+1
        if (save > 0):
            sq_ncs[save].setAttribute('ligated', 'true')


def convert_to_square(general_mei, clef, neume_components):
    # Change @loc to @pname and @oct
    scale = clef_to_pitch[clef]
    for nc in neume_components:
        locval = nc.getAttribute('loc')
        pitch = scale[int(locval) + 3]          # pitch = scale[locs.index(locval)]
        nc.setAttribute('pname', pitch[0])
        nc.setAttribute('oct', pitch[1])
    # Still need to remove @loc
    for nc in neume_components:
        nc.removeAttribute('loc')


def convert_to_aquitanian(general_mei):
    # Create the one reference line
    staffDef = general_mei.getElementsByTagName("staffDef")[0]
    staffDef.setAttribute('lines', '1')
    # Change @loc value to be according to the 'reference line'
    ncomponents = general_mei.getElementsByTagName("nc")
    for nc in ncomponents:
        locval = int(nc.getAttribute('loc'))
        nc.setAttribute('loc', str(locval - 2))
        # Change @tilt=n to @tilt=ne
        if (nc.getAttribute('tilt') and nc.getAttribute('tilt')=='n'):
            nc.setAttribute('tilt', 'ne')


# ------------ #
# Main program #
# ------------ #
def gabc2mei(gabc_line, mei_file, notation_type):
    # Get the words from gabc
    words = gabc_line.split()
    print(words)

    # Process each gabc word
    for word in words:
        print('\nThe word is: ', word)
        syllables = word.split(')')
        
        # Process each gabc syllable and add it to the layer
        for gabc_syllable in syllables[:-1]:
            print()
            print(gabc_syllable)
            # Setting the clef as the child of layer
            if gabc_syllable in ['(c1', '(c2', '(c3', '(c4', '(f2', '(f3', '(f4']:
                clef_mei = doc.createElement('clef')
                clef_mei.setAttribute('shape', gabc_syllable[1].capitalize())
                clef_mei.setAttribute('line', gabc_syllable[2])
                layer1.appendChild(clef_mei)
                print('clef:', gabc_syllable[1].capitalize() + gabc_syllable[2])
            # Encoding the syllable
            else:
                syllable_mei = doc.createElement('syllable')
                layer1.appendChild(syllable_mei)
                
                # Extract the syllable text and the list of neumes
                syl_text, indiv_neumes_list = get_syl_and_neumes(gabc_syllable)
                print(syl_text)
                print(indiv_neumes_list)
                
                # Fill in the syllable with <syl> and <neume> elements
                syl_mei = doc.createElement('syl')
                text = doc.createTextNode(syl_text)
                syl_mei.appendChild(text)
                syllable_mei.appendChild(syl_mei)
                for gabc_neume in indiv_neumes_list:
                    if gabc_neume == '':
                        pass
                    else:
                        mei_neume = convert_to_mei_neume(gabc_neume)
                        syllable_mei.appendChild(mei_neume)

    encode_liquescent_curve_for_tilde()
    encode_obliqua_ligatures()

    # Assign UUID @xml:ids for all elements
    body = doc.getElementsByTagName('body')[0]
    for elem in body.getElementsByTagName("*"):
        elem.setAttribute('xml:id', 'm-' + str(uuid.uuid1()))

    # Write the general file (the one with @loc attributes)
    index = mei_file.index('/')
    filename = mei_file[:index+1] + "MEI_intermedfiles" + mei_file[index:]
    myfile = open(filename, "w")
    myfile.write(doc.toprettyxml())
    myfile.close()


    # Write the final files (for square or for aquitanian)

    # For Square notation:
    if notation_type == 'square':
        clefs = doc.getElementsByTagName('clef')
        clef0_elem = clefs[0]
        clef0_val = clef0_elem.getAttribute('shape') + clef0_elem.getAttribute('line') 
        mei_file = mei_file[:-4] + "_SQUARE" + mei_file[-4:]
        if clefs.length == 1:
            neume_components = doc.getElementsByTagName("nc")
            convert_to_square(doc, clef0_val, neume_components)
        else:
            # Initializing the clef_value with the value of the first clef
            clef_val = clef0_val
            print('\n'+clef_val)
            # Initializing the dictionary of syllabes_to_clefs_dict, 
            # which has as keys the clefs and as values the list of syllables_after_clef
            syllables_to_clefs_dict = {'C1': [], 'C2': [], 'C3': [], 'C4': [], 'F2': [], 'F3': [], 'F4': []}
            syllables_after_clef = []
            # Initializing the first element of the while cycle
            elem = clef0_elem.nextSibling
            # Iterating over elements 
            while(elem):
                print(elem)
                # Identifying syllables
                if(elem.tagName and elem.tagName == "syllable"):
                    syllables_after_clef.append(elem)
                # And clefs
                elif(elem.tagName and elem.tagName == "clef"):
                    # Update dictionary of syllables pertaining to the clef given until this moment
                    # We are not updating by simply doing dict[clef_val] = values, 
                    # but by doing dict[clef_val] = dict[clef_val] + values, 
                    # in case the clef has been found before and it already 
                    # contains a set of notes from a previous passage (this happens in Piece 07)
                    syllables_to_clefs_dict[clef_val] = syllables_to_clefs_dict[clef_val] + syllables_after_clef
                    # Getting the new clef
                    clef_val = elem.getAttribute('shape') + elem.getAttribute('line') 
                    print('\n'+clef_val)
                    # And initializing the list of syllables related to that clef
                    syllables_after_clef = []
                else:
                    pass
                # Continue to the next iteration of elements
                elem = elem.nextSibling
            # Update the dictionary of the syllables per clef for the last time (so, for the last clef)
            # We are not updating by simply doing dict[clef_val] = values, 
            # but by doing dict[clef_val] = dict[clef_val] + values, 
            # in case the clef has been found before and it already
            syllables_to_clefs_dict[clef_val] = syllables_to_clefs_dict[clef_val] + syllables_after_clef
            print()
            print(syllables_to_clefs_dict)

            for clef_val in syllables_to_clefs_dict:
                syllables_after_clef = syllables_to_clefs_dict[clef_val]
                for syllable in syllables_after_clef:
                    neume_components = syllable.getElementsByTagName("nc")
                    convert_to_square(doc, clef_val, neume_components)

    # For Aquitanian notation:
    elif notation_type == 'aquitanian':
        convert_to_aquitanian(doc)
        mei_file = mei_file[:-4] + "_AQUIT" + mei_file[-4:]

    # Write the MEI file
    myfile = open(mei_file, "w")
    myfile.write(doc.toprettyxml())
    myfile.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='GABC file to MEI Neumes file')
    parser.add_argument('gabc', help='GABC line')
    parser.add_argument('mei_output', help='MEI output file')
    parser.add_argument('-notation', choices=['square', 'aquitanian'], default='aquitanian')
    args = parser.parse_args()
    gabc_file = open(args.gabc, "r")
    gabc2mei(gabc_file.readline(), args.mei_output, args.notation)
    gabc_file.close()


# python3 gabc-tokens_to_mei-elements.py GABC_infiles/01_benedicte-omnes_pem82441_aquit.gabc MEI_outfiles/01_benedicte-omnes_pem82441_aquit.mei
# python3 gabc-tokens_to_mei-elements.py GABC_infiles/02_benedicte-omnes_pem85041_square.gabc MEI_outfiles/02_benedicte-omnes_pem85041_square.mei -notation square
# python3 gabc-tokens_to_mei-elements.py GABC_infiles/03_de-fructu-operum_pem56766_aquit.gabc MEI_outfiles/03_de-fructu-operum_pem56766_aquit.mei
# python3 gabc-tokens_to_mei-elements.py GABC_infiles/04_de-fructu-operum_pem84909_square.gabc MEI_outfiles/04_de-fructu-operum_pem84909_square.mei -notation square
# python3 gabc-tokens_to_mei-elements.py GABC_infiles/05_dicit-dominus_pem84540_aquit.gabc MEI_outfiles/05_dicit-dominus_pem84540_aquit.mei
# python3 gabc-tokens_to_mei-elements.py GABC_infiles/06_dicit-dominus_pem84623_aquit.gabc MEI_outfiles/06_dicit-dominus_pem84623_aquit.mei
# python3 gabc-tokens_to_mei-elements.py GABC_infiles/07_dicit-dominus_pem84873_square.gabc MEI_outfiles/07_dicit-dominus_pem84873_square.mei -notation square
# python3 gabc-tokens_to_mei-elements.py GABC_infiles/08_ecce-virgo_pem84614_aquit.gabc MEI_outfiles/08_ecce-virgo_pem84614_aquit.mei
# python3 gabc-tokens_to_mei-elements.py GABC_infiles/09_ecce-virgo_pem84548_aquit.gabc MEI_outfiles/09_ecce-virgo_pem84548_aquit.mei
# python3 gabc-tokens_to_mei-elements.py GABC_infiles/10_ecce-virgo_pem84882_square.gabc MEI_outfiles/10_ecce-virgo_pem84882_square.mei -notation square
# python3 gabc-tokens_to_mei-elements.py GABC_infiles/13_factus-est-repente_pem84630_aquit.gabc MEI_outfiles/13_factus-est-repente_pem84630_aquit.mei
# python3 gabc-tokens_to_mei-elements.py GABC_infiles/14_factus-est-repente_pem84881_square.gabc MEI_outfiles/14_factus-est-repente_pem84881_square.mei -notation square
# python3 gabc-tokens_to_mei-elements.py GABC_infiles/15_fili-quid_pem84534_aquit.gabc MEI_outfiles/15_fili-quid_pem84534_aquit.mei
# python3 gabc-tokens_to_mei-elements.py GABC_infiles/16_fili-quid_pem84863_square.gabc MEI_outfiles/16_fili-quid_pem84863_square.mei -notation square
# python3 gabc-tokens_to_mei-elements.py GABC_infiles/17_justorum-animae_pem83892_aquit.gabc MEI_outfiles/17_justorum-animae_pem83892_aquit.mei
# python3 gabc-tokens_to_mei-elements.py GABC_infiles/18_justorum-animae_pem85059_square.gabc MEI_outfiles/18_justorum-animae_pem85059_square.mei -notation square
# python3 gabc-tokens_to_mei-elements.py GABC_infiles/19_manducaverunt_pem84600_aquit.gabc MEI_outfiles/19_manducaverunt_pem84600_aquit.mei
# python3 gabc-tokens_to_mei-elements.py GABC_infiles/20_manducaverunt_pem83880_aquit.gabc MEI_outfiles/20_manducaverunt_pem83880_aquit.mei
# python3 gabc-tokens_to_mei-elements.py GABC_infiles/21_manducaverunt_pem84880_square.gabc MEI_outfiles/21_manducaverunt_pem84880_square.mei -notation square
# python3 gabc-tokens_to_mei-elements.py GABC_infiles/23_martinus-abrahe_pem85056_square.gabc MEI_outfiles/23_martinus-abrahe_pem85056_square.mei -notation square
# python3 gabc-tokens_to_mei-elements.py GABC_infiles/26_mitte-manum_pem84905_square.gabc MEI_outfiles/26_mitte-manum_pem84905_square.mei -notation square
# python3 gabc-tokens_to_mei-elements.py GABC_infiles/28_panem-de-caelo_pem84919_square.gabc MEI_outfiles/28_panem-de-caelo_pem84919_square.mei -notation square
# python3 gabc-tokens_to_mei-elements.py GABC_infiles/30_pater-si-non_pem84872_square.gabc MEI_outfiles/30_pater-si-non_pem84872_square.mei -notation square
# python3 gabc-tokens_to_mei-elements.py GABC_infiles/32_psallite-domino_pem84874_square.gabc MEI_outfiles/32_psallite-domino_pem84874_square.mei -notation square
# python3 gabc-tokens_to_mei-elements.py GABC_infiles/35_qui-manducat_pem84924_square.gabc MEI_outfiles/35_qui-manducat_pem84924_square.mei -notation square

# python3 gabc-tokens_to_mei-elements.py GABC_infiles/37_qui-vult_pem85065_square.gabc MEI_outfiles/37_qui-vult_pem85065_square.mei -notation square
# python3 gabc-tokens_to_mei-elements.py GABC_infiles/39_tu-es-petrus_pem85073_square.gabc MEI_outfiles/39_tu-es-petrus_pem85073_square.mei -notation square
# python3 gabc-tokens_to_mei-elements.py GABC_infiles/41_tu-mandasti_pem84946_square.gabc MEI_outfiles/41_tu-mandasti_pem84946_square.mei -notation square
# python3 gabc-tokens_to_mei-elements.py GABC_infiles/43_vos-qui-secuti_pem85037_square.gabc MEI_outfiles/43_vos-qui-secuti_pem85037_square.mei -notation square


# python3 gabc-tokens_to_mei-elements.py GABC_infiles/trial_14_liqpes.gabc MEI_outfiles/trial_14_liqpes.mei
# python3 gabc-tokens_to_mei-elements.py GABC_infiles/trial_3_emptysyllables.gabc MEI_outfiles/trial_3_emptysyllables.mei
# python3 gabc-tokens_to_mei-elements.py GABC_infiles/Aquit2_twoclefs.gabc MEI_outfiles/Aquit2_twoclefs.mei -notation square
# python3 gabc-tokens_to_mei-elements.py GABC_infiles/trial_accid.gabc MEI_outfiles/trial_accid.mei -notation square
