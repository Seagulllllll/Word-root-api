# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 15:30:09 2020

@author: user
"""

from morpheme_finder import Morpheme
from derive_from import Stemming

word = "useful"
stemming_list = Stemming(word)
print(stemming_list)
stem = stemming_list[0]
morpheme_list = Morpheme(stem)
print(morpheme_list)

'''
f = open("data.for.testing_from.eng.txt", "r", encoding = "utf-8")
data = f.readlines()
f.close()
data_use = [s.strip("\n").split() for s in data]
word_test_list = [l[0] for l in data_use]

content = "{:15} {:15} {:15} {:1}".format("word", "seg 1", "segmentation", "correct seg")+"\n\n"
for word in word_test_list:
    stemming_list = Stemming(word)
    stem = stemming_list[0]
    first_segmentation = stemming_list[1]
    f_seg_str = ""
    for s in first_segmentation:
        f_seg_str += s+" "
    morpheme_list = Morpheme(stem)
    root_segmentation = []
    for s in first_segmentation:
        if s == stem:
            for morpheme in morpheme_list:
                root_segmentation.append(morpheme)
        else: root_segmentation.append(s) 
    r_seg_str = ""
    for s in root_segmentation:
        r_seg_str += s+" "
    cor_seg = ""
    for l in data_use:
        if l[0] == word:
            if l[1:] != morpheme_list:
                for i in range(1, len(l)):
                    cor_seg += l[i]+" "
    print(cor_seg)
    content += "{:15} {:15} {:15} {:1}".format(word, f_seg_str, r_seg_str, cor_seg)+"\n"
f = open("model.test.result_from.eng_before.improve.txt", "w", encoding = "utf-8")
f.write(content)
f.close()
'''