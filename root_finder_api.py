from fastapi import FastAPI
from morpheme_finder import Morpheme
from derive_from import Stemming

app = FastAPI(debug = True)

# Usually in another .py file
def Stem(word):
    """
    find stem of the word
    """
    stemming_list = Stemming(word)
    return stemming_list[0]

def Find_roots(word):
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

# Post example
@app.post('/template_post/')
async def template_post(word: str):
    ans_dict = {}
    stem = Stem(word)
    root_list = Find_roots(word)
    ans_dict.update( {word: [stem, root_list]} )
    return ans_dict

'''
# Get example, with path parameter
@app.get('/template_get/{vocab}')
async def template_get(vocab: str):
    ans_dict = {}
    ans_dict.update( {vocab: my_function(vocab)} )

    return ans_dict
'''