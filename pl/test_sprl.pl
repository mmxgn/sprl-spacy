:-use_module('sprl.pl').

run_all :- sprl_process_sentence('An angry big dog is behind us.').
query(run_all).
query(trajector(X)).
query(landmark(X)).
query(spatial_indicator(X)).
query(type(X,Y)).
query(extent(X, Extend)).
query(spatial_relation(X)).
query(gtype(X,Y)).
query(srtype(X, Y)).
query(srtype(X)).
