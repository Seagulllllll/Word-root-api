# -*- coding: utf-8 -*-
"""
from word_root import Segmentation

input:
    type: str
    an english word
output:
    type: list
    a list which describe the word's morphological segmentation
sample:
    input: morphological
    output: ['morph', 'ology', 'ic', 'al']
"""

from morpheme_finder import Morpheme
from derive_from import Stemming

def Segmentation(word):
    stemming_list = Stemming(word)
    stem = stemming_list[0]
    first_segmentation = stemming_list[1]
    morpheme_list_for_stem = Morpheme(stem)
    root_segmentation = []
    for s in first_segmentation:
        if s == stem:
            for morpheme in morpheme_list_for_stem:
                root_segmentation.append(morpheme)
        else: root_segmentation.append(s)
    return root_segmentation
if __name__ == "__main__":
    word = "morphological"
    stemming_list = Stemming(word)
    print(stemming_list)
    stem = stemming_list[0]
    morpheme_list = Segmentation(word)
    print(morpheme_list)

