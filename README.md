# SPRL-Spacy

This repository implements an easy to use Spatial Role Labeling module trained on
three entities (`TRAJECTOR`, `SPATIAL_INDICATOR`, `LANDMARK`) and the relations appearing
on the SpRL 2013 IAPR TC-12 dataset. 

## Requirements

- `spacy >=2.0.0a18` and the necessary requirements
- `sklearn`
- `scipy`
- `pickle` for python 3.7.0
- `problog` for use with ProbLog.

## Usage

1. Clone this repository where you want to use it. 
2. Download the two models from the [releases](https://github.com/mmxgn/sprl-spacy/releases) page
3. Import `spacy` and `sprl` and use them like the following example:


```
import spacy
from sprl import *

nlp = spacy.load('models/en_core_web_lg-sprl')

sentence = "An angry big dog is behind us."

rel = sprl(sentence, nlp, model_relext_filename='models/model_svm_relations.pkl')

print(rel)
```

If everything went fine you should get something like:

```
[(An angry big dog, behind, us, 'direction')]
```

You can also run `sprl_cmd.py` to get a continuous input to test how well various
sentences are processed:

```
$ python3 sprl_cmd.py
```

## Problog

<!-- If you happen to have problog installed, you can see `example.pl` on how to use it from -->
<!-- within problog. **Note:** If you want to use it from within problog you need to append the `sprl` directory to `PYTHONPATH`, e.g: -->

<!-- ``` -->
<!-- $ PYTHONPATH="../sprl" problog example.pl -->
<!-- ``` -->

If you happen to have problog installed, I have made a library that allows you to process sentences and produce a set of first order predicates that express the spatial relations within it. For example you can do something like in `pl/test_sprl.pl`:

```
:-use_module('sprl.pl').

run_all :- sprl_process_sentence('An angry big dog is behind us.').
query(run_all).
query(trajector(X)).
query(landmark(X)).
query(spatial_indicator(X)).
query(type(X,Y)).
query(extent(X, Extent)).
query(spatial_relation(X)).
query(gtype(X,Y)).
query(srtype(X, Y)).
query(srtype(X)).

```

which you can run with:

```
$ PYTHONPATH="../sprl" problog test_sprl.pl
```

and get the following output:

```
              extent(lm0,us):	1
          extent(sp0,behind):	1
extent(tr0,An angry big dog):	1
        gtype(st0,direction):	1
               landmark(lm0):	1
                     run_all:	1
      spatial_indicator(sp0):	1
       spatial_relation(sr0):	1
             srtype(sr0,st0):	1
                 srtype(st0):	1
              trajector(tr0):	1
            type(lm0,person):	1
            type(tr0,animal):	1
```

We can see for example that it identified and labeled the trajector, landmark and spatial indicator in the sentence, assigned them an id, identified the spatial relation and assigned it a general type of *direction*. It also assigned a type of *person* to the landmark *us* and *animal* to the trajector *An angry big dog*. For what those predicates mean and how they are used please see `doc/sprl.html`.

## Credits

While the model has been trained by me, the relation extraction part uses features from
the paper for Sprl-CWW (see below), and the dataset from SemEval 2013 Task 3: Spatial Role Labeling.

The features for relation extraction:

```
Nichols, Eric, and Fadi Botros. 
"SpRL-CWW: Spatial relation classification with independent multi-class models." 
Proceedings of the 9th International Workshop on Semantic Evaluation.
```

Semeval 2013 task 3: Spatial Role Labeling

```
Kolomiyets, Oleksandr, et al. 
"Semeval-2013 task 3: Spatial role labeling." 
Second Joint Conference on Lexical and Computational Semantics
```

So please cite the papers above, as well as spacy and ProbLog (if you use it) in your work :)


