% Shell command: clingo 0 min-rev.lp edb/tapp24.lp 

% Positions in move/2 (disconnected nodes excluded)
pos(X) :- move(X,_).
pos(X) :- move(_,X).

move_tc(X,Y) :- move(X,Y).
move_tc(X,Y) :- move(X,Z), move_tc(Z,Y).

% X and Y same connected component 
scc(X,Y) :- move_tc(X,Y), move_tc(Y,X).

on_cycle(X,Y) :- scc(X,Y), move(X,Y).

{ rev(X,Y) } :- on_cycle(X,Y). 

move1(X,Y) :- move(X,Y), not rev(X,Y).
move1(Y,X) :- rev(X,Y).

move1_tc(X,Y) :- move1(X,Y).
move1_tc(X,Y) :- move1(X,Z), move1_tc(Z,Y).

% No cycles in the new graph
:- move1_tc(X,X).

% Let's count how many edge reversals  we have
rev_cnt(N) :- N = #count{ (X,Y) : rev(X,Y)}.

% Let's reverse as few edges as possible!
#minimize {N : rev_cnt(N)}.

%% AFTER: 
%% % Let's delete as few edges as possible!
%% #minimize {1, (X,Y) : del(X,Y)}. 

% attack-cycle edges
ac(Y,X) :- on_cycle(X,Y).

#show ac/2.
#show rev/2.
