#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 18:19:41 2018

@author: Emmanouil Theofanis Chourdakis

Various utility functions 

"""

from problog.extern import problog_export, problog_export_nondet, problog_export_raw
from problog.logic import Constant as c_

labels_dict = {}

@problog_export('+str', '-str')
def new_label(l):
    """ returns a new label with the prefix given by string l
        for example consecutive calls of  new_label(t, X) are
        satisfied with X = t1, t2, ... """
        
    global labels_dict
    
    if l not in labels_dict:
        labels_dict[l] = 0
    else:
        labels_dict[l] += 1
        
    return "{}{}".format(l, labels_dict[l])
        
    