:-use_module(library(assert)).
:-use_module('sprl_pl.py').
:-use_module('util_pl.py').

% Types we cluster objects to.
sp_types(['animal', 'person', 'building', 'nature',  'vehicle', 'insect', 'area']).

sprl_process_sentence(X) :- % Get spatial entity types
                            sp_types(Types),
    
			    % Resolve sentence to relation
                            sprl(X, Tr, Sp, Lm, Type),
			    
			    % Create spatial relation
			    new_label(sr, SRId),
			    assertz(spatial_relation(SRId)),

			    % Assign type
			    new_label(st, STId),
			    assertz(srtype(STId)),
			    assertz(srtype(SRId, STId)),
			    assertz(gtype(STId, Type)),
			    

			    % Add trajector
			    new_label(tr, TrId),
			    assertz(trajector(TrId)),
			    assertz(extend(TrId, Tr)),
			    assertz(trajector(SRId, TrId)),
			    closest_type(Tr, Types, TrType),
			    assertz(type(TrId, TrType)),
			    
			    % Add landmark
			    new_label(lm, LmId),
			    assertz(landmark(LmId)),
			    assertz(extend(LmId, Lm)),
			    assertz(landmark(SRId, LmId)),
			    closest_type(Lm, Types, LmType),
			    assertz(type(LmId, LmType)),

			    % Add spatial indicator
			    new_label(sp, SpId),
			    assertz(spatial_indicator(SpId)),
			    assertz(extend(SpId, Sp)),
			    assertz(spatial_indicator(SRId, SpId)).
