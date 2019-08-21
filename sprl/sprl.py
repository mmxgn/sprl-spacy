#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 17:14:47 2018

@author: Emmanouil Theofanis Chourdakis <e.t.chourdakis@qmul.ac.uk>

Functions that do spatial role labeling. Relation extraction is done
using sklearn with features extracted from the sentence based on the following paper:
cd
Nichols, Eric, and Fadi Botros.
"SpRL-CWW: Spatial relation classification with independent multi-class models."
Proceedings of the 9th International Workshop on Semantic Evaluation (SemEval 2015)
"""

from sklearn.externals import joblib
import spacy


def get_dep_path(span1, span2):
    assert span1.sent == span2.sent, "sent1: {}, span1: {}, sent2: {}, span2: {}".format(span1.sent, span1, span2.sent, span2)

    up = []
    down = []

    head = span1[0]
    while head.dep_ != 'ROOT':
        up.append(head)
        head = head.head
    up.append(head)

    head = span2[0]
    while head.dep_ != 'ROOT':
        down.append(head)
        head = head.head
    down.append(head)
    down.reverse()

    for n1, t1 in enumerate(up):
        for n2, t2 in enumerate(down):
            if t1 == t2:
                return ["{}::{}".format(u.dep_, 'up') for u in up[1:n1]] + ["{}::{}".format(d.dep_, 'down') for d in down[n2:]]

def extract_relation_features(relation):
    F = {} # Feature dict

    trigger = relation[1]
    args = [relation[0], relation[2]]

    # Extract features relating to trigger
    #trigger_head = get_head(trigger)

    for n, token in enumerate(trigger):
        F['TF1T{}'.format(n)] = token.text
        F['TF2T{}'.format(n)] = token.lemma_
        F['TF3T{}'.format(n)] = token.pos_
        F['TF4T{}'.format(n)] = "::".join([token.lemma_, token.pos_]) # RF.2 concat RF.1

    # Extract features relating to the two arguments
    for a, arg in enumerate(args):
        if arg is not None:
            for n, token in enumerate(arg):
                F['A{}F5T{}'.format(a, n)] = token.text
                F['A{}F6T{}'.format(a, n)] = token.lemma_
                F['A{}F7T{}'.format(a, n)] = token.pos_
                F['A{}F8T{}'.format(a, n)] = "::".join([token.lemma_, token.pos_])


            if arg[-1].i < trigger[0].i:
                F['A{}F12'.format(a)] = 'LEFT'
                F['A{}F22'.format(a)] = trigger[0].i - arg[-1].i
            elif arg[0].i > trigger[-1].i:
                F['A{}F12'.format(a)] = 'RIGHT'
                F['A{}F22'.format(a)] = arg[0].i - trigger[-1].i


            path = get_dep_path(arg, trigger)
            for np, p in enumerate(path):
                F['A{}F17E{}'.format(a, np)] = p
            F['A{}F20'.format(a)] = len(path)
            F['A{}F24'.format(a)] = False
        else:
            F['A{}F24'.format(a)] = True

    # Joint features
    if 'A0F12' in F and 'A1F12' in F:
        F['F13'] = "::".join([F['A0F12'],F['A1F12']])
        if F['A0F12'] == F['A1F12']:
            F['14'] = True
        else:
            F['14'] = False

    if 'F13' in F:
        for n, token in enumerate(trigger):
            F['14T{}'.format(n)] = '::'.join([F['F13'], token.lemma_])

    if 'A0F22' in F and 'A1F22' in F:
        F['F23'] = F['A0F22'] + F['A1F22']

    return F

def extract_candidate_relations_from_sents(sents, gold_relations):
    candidate_relations = []
    candidate_labels = []

    for sent in sents:

        triggers = [t for t in sent.ents if t.label_ == 'SPATIAL_INDICATOR']
        trajectors = [t for t in sent.ents if t.label_ == 'TRAJECTOR']
        landmarks = [t for t in sent.ents if t.label_ == 'LANDMARK']

      #  print(trajectors, triggers, landmarks)

        for trigger in triggers:
            for trajector in trajectors:
                for landmark in landmarks:
                    if not (trajector is None and landmark is None):
                        assert trajector.sent == trigger.sent == landmark.sent, "{}: {}".format(sent, sent.ents)
                        crel = (trajector, trigger, landmark)
                        if crel not in gold_relations:
                            candidate_relations.append(crel)
                            candidate_labels.append('NONE')
                        else:
                            #print("In gold relations already", crel)
                            pass
    return candidate_relations, candidate_labels

def sprl(sentence,
         nlp,
         model_relext_filename='model_svm_relations.pkl'):
    output = []
    doc = nlp(sentence)
    sents = [nlp(s.text) for s in doc.sents]
    candidate_relations, _ = extract_candidate_relations_from_sents(sents, [])
    clf, dv = joblib.load(model_relext_filename)
    for relation in candidate_relations:
        F = extract_relation_features(relation)
        feat_vec = dv.transform(F)
        general_type = clf.predict(feat_vec)[0]
        if general_type != 'NONE':
            output.append((relation[0], relation[1], relation[2], general_type))

    return output


def sprl_str(sentence,
             nlp,
             model_relext_filename='model_svm_relations.pkl'):
    """ Returns triples where every element is string """
    output = []
    doc = nlp(sentence)
    sents = [nlp(s.text) for s in doc.sents]
    candidate_relations, _ = extract_candidate_relations_from_sents(sents, [])
    clf, dv = joblib.load(model_relext_filename)
    for relation in candidate_relations:
        F = extract_relation_features(relation)
        feat_vec = dv.transform(F)
        general_type = clf.predict(feat_vec)[0]
        if general_type != 'NONE':
            output.append((str(relation[0]), str(relation[1]), str(relation[2]), general_type))

    return output
