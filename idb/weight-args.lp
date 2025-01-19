% Compute the WEIGHT of move(x,y), i.e., number of value changes after deletion of move(x,y)
% Shell command: clingo 0 weight.lp edb/tapp24.lp 

% Positions in move/2 (disconnected nodes excluded)
pos(X) :- move(X,_).
pos(X) :- move(_,X).

% Position values BEFORE edge deletion
val(X,won)   :- move(X,Y), val(Y,lost).
val(X,lost)  :- pos(X), val(Y,won) : move(X,Y).
val(X,drawn) :- pos(X), not val(X,won), not val(X,lost).

% Pick exactly one edge to delete
{ del(X) : pos(X) } = 1.

% New move graph without deleted nodes
move1(X,Y) :- move(X,Y), not del(X), not del(Y).

% Position values AFTER edge deletion
val1(X,won)   :- move1(X,Y), val1(Y,lost).
val1(X,lost)  :- pos(X), val1(Y,won) : move1(X,Y).
val1(X,drawn) :- pos(X), not val1(X,won), not val1(X,lost).

% How have position values X changed?
delta(X,Old,New) :- val(X,Old), val1(X,New), Old!=New. 

% How many nodes have changed value?
delta_total(N) :- N = #count{ X : val(X,Old), val1(X,New), Old != New }.

% How many nodes have changed value (grouped by "Old=>New type")?
delta_type(Old,New, N) :- delta(_,Old, New), N = #count{ X : delta(X,Old,New) }.

% What is the *weight* of an edge X->Y? (= #values changed by deleting it)
weight(X, W) :- del(X), delta_total(W).

%#show del/2.
%#show delta/3.
%#show delta_total/1.
% #show delta_type/3.
#show weight/2.
