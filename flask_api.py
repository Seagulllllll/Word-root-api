# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 17:26:04 2020

@author: user
"""

from flask import Flask, request, render_template

from morpheme_finder import Morpheme
from PyDictionary import PyDictionary
from morpheme_meaning import Morpheme_meaning #Morpheme_meaning(seg_list, seg)

app = Flask(__name__)
app.config["DEBUG"] = True
dic = PyDictionary()

def Segmentation(word):
    morpheme_list = Morpheme(word)
    return morpheme_list

def Part_of_speech(word):
    dic_meaning = dic.meaning(word)
    if dic_meaning:
        part_of_speech = list(dic_meaning.keys())[0].lower()
    else: return "No result."
    return part_of_speech
    
def Word_meaning(word):
    dic_meaning = dic.meaning(word)
    if dic_meaning:
        part_of_speech = list(dic_meaning.keys())[0]
        meaning = dic_meaning[part_of_speech][0]
    else: return "No result."
    return meaning
    
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        word = str(request.form["word"])
        part_of_speech = Part_of_speech(word)
        meaning = Word_meaning(word)+"."
        list_items = []
        morpheme_list = Segmentation(word)
        for mor in morpheme_list:
            mor_meaning = Morpheme_meaning(morpheme_list, mor)
            list_items.append([mor, mor_meaning])
        segmentation = Segmentation(word)
        return render_template('index.html', word = word,
                               part_of_speech = part_of_speech, 
                               meaning = meaning,
                               segmentation = segmentation, 
                               l = list_items)
    return render_template("index.html")

app.run()
