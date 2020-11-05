# -*- coding: utf-8 -*-
"""
from morpheme_meaning import Morpheme_meaning

input:
    seg_list: list, the list of all morpheme of an English word
    seg: str, the morpheme interested in
output:
    type: str
    the meaning of the input segment's meaning
sample:
    input: ['morph', 'ology', 'ic', 'al'], ology
    output: science

Files required:
    morpheme.meaning.json
"""

import json

with open("morpheme.meaning.json", "r", encoding = "utf-8") as file:
    mm_dict = json.load(file)
def Morpheme_meaning(seg_list, seg):
    possible_morpheme = [mor for mor in mm_dict  if mor.lstrip("-").rstrip("-") == seg]
    #print(possible_morpheme)
    if len(possible_morpheme) == 0:
        return ("")
    if len(possible_morpheme) == 1:
        meaning = mm_dict[possible_morpheme[0]] #"meaning" is a list
    else:
        morpheme_index = seg_list.index(seg)+1/len(seg_list)
        index_difference = []
        for candidate in possible_morpheme:
            if candidate == seg+"-":
                index_difference.append(abs((1/4)-morpheme_index))
            elif candidate == seg:
                index_difference.append(abs((2/4)-morpheme_index))
            elif candidate == "-"+seg:
                index_difference.append(abs((3/4)-morpheme_index))
        morpheme = possible_morpheme[index_difference.index(min(index_difference))]
        meaning = mm_dict[morpheme] 
        #print(meaning)
    content = ""
    for s in meaning:
        if meaning.index(s) != len(meaning)-1:
            content += s +", "
        else: content += s
    return(content)

if __name__ == "__main__":
    seg_list = ["morph", "ology", "ic", "al"]
    seg = "ology"
    print(Morpheme_meaning(seg_list, seg))
