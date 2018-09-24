#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 22:38:03 2018

@author: Emmanouil Theofanis Chourdakis

Problog wrapper for NLP functions in spacy

"""

import spacy
from problog.extern import problog_export, problog_export_nondet

global nlp # Initialize the model the first time it is neede
nlp = None

def load_model_if_not_loaded():
    global nlp
    # Load NLP model if it is not loaded already
    if not nlp:
        print("[II] Loading simple NLP model...")
        nlp = spacy.load('en_vectors_web_lg')
        print("[II] done.") 
        
    return nlp

def remove_apostrophe(string):
    # Remove "'"S
    if string[0] == "'":
        string = string[1:]
    if string[-1] == "'":
        string = string[:-1]    
        
    return string
    

@problog_export_nondet('+str', '-str')
def sents(doc_str):
    """ Satisfied when sent is a sentence in doc_str """
    
    global nlp
    
    # Load NLP model if it is not loaded already
    nlp = load_model_if_not_loaded()

    
    # Remove "'"S
    doc_str = remove_apostrophe(doc_str)
        
    doc = nlp(doc_str)
        
    return [sent.text for sent in doc.sents]

@problog_export_nondet('+str', '-str')
def token(doc_str):
    """ Satisfied when token is a token in doc_str """
    
    global nlp
    
    # Load NLP model if it is not loaded already
    nlp = load_model_if_not_loaded()

    
    # Remove "'"S
    doc_str = remove_apostrophe(doc_str)
        
    doc = nlp(doc_str)
        
    return [token.text for token in doc]

    
@problog_export('+str', '-str')
def load_text(fname):
    
    # Remove "'"S
    fname = remove_apostrophe(fname) 
    
    with open(fname, 'r') as f:
        doc_str = f.read()
    
    return doc_str

@problog_export('+str', '-str')
def lemma(text):

    global nlp
    
    # Load NLP model if it is not loaded already
    nlp = load_model_if_not_loaded()
  
    
    # Remove "'"S
    text = remove_apostrophe(text) 
    
    return nlp(text)[0].lemma_.lower()
    
@problog_export('+str', '-str')
def root(sent):
    """ Unifies root(sent, X) with  subst X = the root of a sentence 
        e.g:
            root('An angry big dog', X), X='dog'
            
    """
    
    global nlp
    
    # Load NLP model if it is not loaded already
    nlp = load_model_if_not_loaded()
 
    
    # Remove "'"S
    sent = remove_apostrophe(sent) 
    
    return [s for s in nlp(sent).sents][0].root.text

@problog_export('+str', '+list', '-str')
def closest_type(obj, list_of_types):
    
    global nlp
    
    # Load NLP model if it is not loaded already
    nlp = load_model_if_not_loaded()

        
    
    obj = remove_apostrophe(obj)
    obj_tok = nlp(obj)
    
    similarity = 0
    closest_class = None
    
    for typ in list_of_types:
        typ = remove_apostrophe(typ.functor)
        typ_tok = nlp(typ)
        
        sim = obj_tok.similarity(typ_tok)
        
        if sim > similarity:
            similarity = sim
            closest_class = typ
            
    return closest_class
        
