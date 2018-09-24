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


    
