# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 17:26:04 2020

@author: user
"""

from flask import Flask, request

from morpheme_finder import Morpheme
from derive_from import Stemming

app = Flask(__name__)
app.config["DEBUG"] = True

def Stem(word):
    stemming_list = Stemming(word)
    return stemming_list[0]

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
    ans = ""
    for r in root_segmentation:
        ans += r+" "
    return ans


@app.route("/", methods=["GET", "POST"])
def home():
    errors = ""
    if request.method == "POST":
        word = None
        try:
            word = str(request.form["word"])
        except:
            errors += "<p>{!r} is not a word.</p>\n".format(request.form["word"])
        if word is not None:
            stem = Stem(word)
            segmentation = Segmentation(word)
            return '''
                <html>
                    <body>
                        <p>The stem of the word is: {stem}</p>
                        <p>The word is segmented as: {segmentation}</p>
                        <p>Enter your word:</p>
                        <form method="post" action=".">
                            <p><input name="word" /></p>
                            <p><input type="submit" value="Find Root!" /></p>
                        </form>
                    </body>
                </html>
            '''.format(stem = stem, segmentation = segmentation)

    return '''
        <html>
            <body>
                {errors}
                <p>Enter your word:</p>
                <form method="post" action=".">
                    <p><input name="word" /></p>
                    <p><input type="submit" value="Find Root!" /></p>
                </form>
            </body>
        </html>
    '''.format(errors = errors)

app.run()