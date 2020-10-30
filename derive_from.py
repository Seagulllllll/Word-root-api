# -*- coding: utf-8 -*-
"""
from derive_from import Stemming

Input
-----
    type: str
    an English word

Output
------
    type: list
    the stem of the given word and the segmentation of the word by segmenting its affixes.

Sample
------
    input: 'youthfulness'
    output: ['youth', ['youth', 'ful', 'ness']]
    
Files require
--------------
    suffixes.txt
    prefixes.txt
    conbination.rules.json

"""
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer 
import re
import json

f = open("suffixes.txt", "r", encoding = "utf-8")
suffix = f.readlines()
f.close()
suffix_1 = [s.strip("\n").split(", ") for s in suffix]
suffix_list = [s.strip("-") for l in suffix_1 for s in l]

f = open("prefixes.txt", "r", encoding = "utf-8")
prefix = f.readlines()
f.close()
prefix_1 = [s.strip("\n").split(", ") for s in prefix]
prefix_list = [s.strip("-") for l in prefix_1 for s in l]

with open("combination.rule.json", "r", encoding = "utf-8") as file:
    com_rule = json.load(file)

def Stemming(word):
    """

    Parameters
    ----------
    word : str
        an English word.

    Returns
    -------
    [stem, whole_segmentation] : list
        stem: the stem of the given word.
        whole_segmentation: the segmentation of the word by segmenting its affixes.

    """
    prefix_segment_first = Find_prefix(word)
    #print(prefix_segment_first)
    if prefix_segment_first[0] == "":
        prefix = []
    elif len(prefix_segment_first[1]) <= 3:
        prefix = []
    else: 
        prefix = [prefix_segment_first[0]]
        word = prefix_segment_first[1]
    whole_segmentation = []
    while True:
        '''
        if Stemmable(word) == word:
            whole_segmentation = [word] + whole_segmentation
            break
        '''
        segmentation = Find_suffix(word)
        #print(segmentation)
        new_word = segmentation[0]
        if new_word == word:
            whole_segmentation = [segmentation[0]] + whole_segmentation
            break
        elif new_word in prefix_list or re.search("[a|e|i|o|u]", new_word) == None:
            whole_segmentation = [word] + whole_segmentation
            break
        elif len(new_word) <= 5:
            whole_segmentation = segmentation + whole_segmentation
            break
        whole_segmentation = [segmentation[1]] + whole_segmentation
        word = new_word
    prefix_segment = Find_prefix(whole_segmentation[0])
    #print(prefix_segment)
    if prefix_segment[1] == whole_segmentation[0]:
        stem = whole_segmentation[0]
        whole_segmentation = prefix + whole_segmentation
    elif len(prefix_segment[1]) <= 5:
        stem = whole_segmentation[0]
        whole_segmentation = prefix + whole_segmentation
    else:
        stem = prefix_segment[1]
        whole_segmentation = prefix + prefix_segment + whole_segmentation[1:]
    return [stem, whole_segmentation] 

def Find_suffix(word):
    """

    Parameters
    ----------
    word : str
        a word

    Returns
    -------
    can : list
        [word, suffix]

    """
    candidates = []
    for suffix in suffix_list:
        if word[len(word)-len(suffix):len(word)] == suffix:
            first = word[0:len(word)-len(suffix)]
            rem = suffix
            if [first, rem] not in candidates:
                candidates.append([first, rem])
            
            if Restore_forms(first, rem):
                candidates += Restore_forms(first, rem)
            
    result_list = []
    for can in candidates:
        if Is_word(can[0]) and re.search("[a|e|i|o|u]", can[0]):
            result_list.append(can)
    if len(result_list) == 0:
        output = [word, ""]
    elif len(result_list) == 1:
        output = result_list[0]
    else:
        possible_suf = [possibility[1] for possibility in result_list]
        for s in possible_suf:
            if s != possible_suf[0]:
                mark = False
                break
            else: 
                mark = True
        if mark == False:
            for possibility in result_list:
                if possibility[1] == "ly" and possibility[0][len(possibility[0])-2:len(possibility[0])] == "le":
                    return possibility
            min_suf = min(possible_suf)
            min_suf_count = possible_suf.count(min_suf)
            if min_suf_count == 1:
                output = result_list[possible_suf.index(min_suf)]
                return output
            else:
                r_list = [possibility for possibility in result_list if possibility[1] == min_suf]
                result_list = r_list
        #if mark == True or if there are two or more possibility with the shortest suffix 
        if first[-1] == "i":
            for possibility in result_list:
                if re.match("[a-z]+y", possibility[0]):
                    return possibility
                else: continue
        for possibility in result_list:
            if re.match("[a-z]+e", possibility[0]):
                return possibility
        for possibility in result_list:
            if possibility[0] == first:
                return possibility
        #沒有特定規則就先隨意return一個可能性
        return result_list[0]
    return output

def Find_prefix(word):
    """
    Parameters
    ----------
    word : str
        a word

    Returns
    -------
    output : list
        [prefix, word]
        
    """
    candidates = []
    for prefix in prefix_list:
        if word[0:len(prefix)] == prefix:
            pre = prefix
            latter = word[len(prefix):len(word)]
            if [pre, latter] not in candidates:
                candidates.append([pre, latter])
    result_list = []
    for can in candidates:
        if Is_word(can[1]):
            result_list.append(can)
    if len(result_list) == 0:
        output = ["", word]
    elif len(result_list) == 1:
        output = result_list[0]
    else: 
        min_length_prefix = 100
        for possibility in result_list:
            if len(possibility[0]) < min_length_prefix:
                output = possibility
    return output
  
#combination rule application
def Restore_forms(first, rem):
    """

    Parameters
    ----------
    first: str
        a string of letters, possibly the wrong form of a root or word
    rem: str
        a string of letters, possibly a suffix
        
    Returns
    -------
    possible_forms : list
        a list of all possible pairs (first2, rem2) after restoring the root or word's original forms.
    
    """
    possible_forms = []
    for affix in com_rule:
        if affix == rem:
            if len(first) >= 2:
            #consider y and er
                if affix == "y" or affix == "er" or affix == "ing":
                    for l in com_rule[affix]:
                        #處理y或er前面重複字母的問題
                        if l[0] != "" and l[1] == "":
                            if first[-2] == l[0] and first[-1] == l[0]:
                                if l[0] == "":
                                    first_new = first + l[1]
                                else:
                                    if first[-1] == l[0]:
                                        first_new = first.strip(first[-1]) + l[1]
                                    else: continue
                                possible_forms.append([first_new, rem])
                        else:
                            if l[0] == "":
                                first_new = first + l[1]
                            else:
                                if first[-1] == l[0]:
                                    first_new = first.strip(first[-1]) + l[1]
                                else: continue
                            possible_forms.append([first_new, rem])
                else:
                    for l in com_rule[affix]:
                        if l[0] == "":
                            first_new = first + l[1]
                        else:
                            if first[-1] == l[0]:
                                first_new = first.strip(first[-1]) + l[1]
                            else: continue
                        possible_forms.append([first_new, rem])
    return possible_forms

def Is_word(word):
    """
    Test whether a string of letters is a word or not.
    If it is a word, return True; if not, return False.
    """
    if not wordnet.synsets(word):
        return False
    else: return True

def Stemmable(seg):
    """
    Test whether a certain segment is stemmable or not useing PorterStemmer
    If stemmable, return its stem; if not, return the segment back.
    """
    ps = PorterStemmer()
    stem = ps.stem(seg)
    if stem + "e" == seg:
        return seg
    return stem

if __name__ == "__main__":
    word = input("Enter: ")
    result = Stemming(word)
    print(result)
    '''
    f = open("data.for.testing_from.eng.txt", "r", encoding = "utf-8")
    celex = f.readlines()
    f.close()
    
    content = ""
    celex_use = [s.strip("\n").split() for s in celex]
    word_test_list = [l[0] for l in celex_use]
    for word in word_test_list:
        result = Stemming(word)
        print(result)

        content += str(result) + "\n"
    f = open("test_result4.txt", "w", encoding = "utf-8")
    f.write(content)
    f.close()
    '''
