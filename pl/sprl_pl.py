#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 13:51:33 2018

@author: Emmanouil Theofanis Chourdakis

Problog bindings for spacy-sprl 

"""

from problog.extern import problog_export, problog_export_nondet, problog_export_raw
from problog.logic import Constant as c_

import spacy
import sprl as mod_sprl

global lut_sprl # For memoization
lut_sprl = {}

global nlp_sprl # Initialize the model the first time it is neede
nlp_sprl = None

@problog_export_nondet('+str', '-str', '-str', '-str', '-str')
def sprl(sentence):
    global nlp_sprl, nlp, lut_sprl
    
    # Load NLP model if it is not loaded already
    if not nlp_sprl:
        print("[II] Loading NLP model for SpRL...")
        nlp_sprl = spacy.load('../models/en_core_web_lg-sprl')
        nlp = nlp_sprl
        print("[II] done.")
    
    # Remove "'"S
    sent = sentence
    if sent[0] == "'":
        sent = sent[1:]
    if sent[-1] == "'":
        sent = sent[:-1]
    
    if sentence in lut_sprl:
        return lut_sprl[sent]
    else:
        triples = mod_sprl.sprl(sent, nlp_sprl, model_relext_filename="../models/model_svm_relations.pkl")
        lut_sprl[sent] = [tuple([str(t) for t in l]) for l in triples]
        L = lut_sprl[sent] 
        return L

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
        

    
