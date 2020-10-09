# -*- coding: utf-8 -*-
"""
from morpheme_finder import morpheme

input:
    type: str
    an english word
output:
    type: list
    a list which describe the word's morphological segmentation
sample:
    input: morphological
    output: ['morph', 'ology', 'ical']

Files required:
    morphemes.probability.json
    combination.rule.json
    suffixes.txt
    prefixes.txt
    
"""
import json
import re

with open("morphemes.probability.json", "r", encoding = "utf-8") as file:
    p_root_dict = json.load(file)
    
with open("words.probability.json", "r", encoding = "utf-8") as file:
    p_word_dict = json.load(file)
    
#some rules for combining suffixes
with open("combination.rule.json", "r", encoding = "utf-8") as file:
    com_rule = json.load(file)

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
'''
f = open("data.for.testing.txt", "r", encoding = "utf-8")
data = f.readlines()
f.close()
data_dict = {}
data_list = [s.strip("\n").split() for s in data]
for l in data_list: 
    data_dict.update({l[0]:l[1:]})
data_word = [l[0] for l in data_list]
'''
root_list = [root for root in p_root_dict]

def Morpheme(word):
    """
    Parameters
    ----------
    word : str
        an english word.

    Returns
    -------
    morpheme_list: list
        a list which describes the word's morphological segmentation.
    """
    morpheme_list = Segment(word)
    return morpheme_list

#find possible segmentation of a word
def Segment(word): 
    """

    Parameters
    ----------
    word : str
        an english word.

    Returns
    -------
    seg_result: list
        a possible segmentation of the english word. 

    """
    if len(word) == 0:
        return []
    candidates = []
    for first, rem in Splits(word):
        candidates.append([first] + Segment(rem))
        
        #find original form
        for first2, rem2 in Restore_forms(first, rem):
            #mark of raising probability
            candidates.append([first2, 10] + Segment(rem2))
        
    #assign probabilities
    prob_candidates = []
    for segment_combination in candidates:
        
        if [word] in candidates:
            prob_sum = Prob_position(segment_combination)
        else: 
            prob_sum = Probability(segment_combination)
        prob_candidates.append(prob_sum)
    max_prob = max(prob_candidates)
    i = prob_candidates.index(max_prob)
    seg_result = [s for s in candidates[i] if s != 10]
    return seg_result

def Splits(word):
    """

    Parameters
    ----------
    word : str
        an english word.

    Returns
    -------
    possible_splits : list
        a list of all possible spliting pairs (first, rem).
    
    """
    possible_splits = [(word[:i+1], word[i+1:]) for i in range(len(word))]
    return possible_splits

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

#probability product
def Probability(segment_combination):
    """
    Parameters
    ----------
    segment_combination: list
        a list of a word's segmentation.

    Returns
    -------
    prob_product: float
        the probability of the segmentation being legitimate.
    
    """
    prob_product = 1
    for seg in segment_combination:
        if seg == 10:
            continue
        if seg in p_root_dict:
            #for segments restored by combination rules, give them higher probabilities
            index = segment_combination.index(seg)
            if index < len(segment_combination)-1:
                latter = segment_combination[index+1]
                if latter == 10 and len(seg) >= 3:
                    prob = p_root_dict[seg]*10
                else: prob = p_root_dict[seg]
            else: prob = p_root_dict[seg]
        elif re.search("[a|e|i|o|u]", seg) == None:
            prob = 0
        elif len(seg) <= 5 and seg in p_word_dict:
            prob = p_word_dict[seg]
        else:
            prob = P_long_word(seg)
        prob_product *= prob
    return prob_product
#the probability of a segmentation with considering positions
def Prob_position(segment_combination):
    """
    Parameters
    ----------
    segment_combination: list
        a list of a word's segmentation.

    Returns
    -------
    prob_product: float
        the probability of the segmentation being legitimate, considering the position of affixes.
    
    """
    prob_product = 1
    for seg in segment_combination:
        div = (segment_combination.index(seg)+1)/(len(segment_combination)+1)
        if seg == 10:
            continue
        if seg in p_root_dict:
            #for segments restored by combination rules, give them higher probabilities
            index = segment_combination.index(seg)
            if index < len(segment_combination)-1:
                latter = segment_combination[index+1]
                if latter == 10 and len(seg) >= 3:
                    prob = p_root_dict[seg]
                else: prob = p_root_dict[seg]
            else: prob = p_root_dict[seg]
        else:
            if len(seg) == 1 or re.search("[a|e|i|o|u]", seg) == None:
                prob = 0
            elif len(seg) <= 5 and seg in p_word_dict:
                prob = p_word_dict[seg]
            else: prob = P_long_word(seg)

        #consider the position of suffixes and prefixes
        if seg in prefix_list:
            if div >= 0.5:
                prob *= 0.1
            else: prob *= 10
        elif seg in suffix_list:
            if div <= 0.5:
                prob *= 0.1
            else: prob *= 10
        prob_product *= prob
    return prob_product
    
#give probability to the unknown segments       
def P_long_word(segment): 
    """
    Parameters
    ----------
    segment: str
        a string of letters

    Returns
    -------
    prob: float
        The probability of a certain unknown segment.
        The probability will be lower if the segment is longer.
    
    """
    root_list = [root for root in p_root_dict]
    prob = (1/len(root_list))*0.1**len(segment)
    return prob

if __name__ == "__main__":
    
    word = input("Enter: ")
    segmentation = Segment(word)
    print(segmentation)
    '''
    content = "{:15} {:18} {:1}".format("word", "result", "correct seg\n")
    words = []
    morpheme_result = []
    correct_seg = []
    for word in data_word:
        words.append(word)
        segmentation = Segment(word)
        seg = ""
        for s in segmentation:
            seg += s+" "
        morpheme_result.append(seg)
        corr_seg = ""
        for w in data_list:
            if word == w[0] and segmentation != w[1:]:
                for i in range(1,len(w)):
                    corr_seg += w[i]+" "
                correct_seg.append(corr_seg)
            elif word == w[0]: correct_seg.append("")
    for i in range(len(words)):
        content += "{:15} {:18} {:1}".format(words[i], morpheme_result[i], correct_seg[i])+"\n"
    f = open("eng.morpheme.result.txt", "w", encoding = "utf-8")
    f.write(content)
    f.close()
    '''
