%----------------------------------------------------------------------
% An example program that provides minimal well-founded explanations
% of game graphs using Clingo's "conditional literal" syntax for
% solving win-move games. This program does not hard-code the decided
% portion of the corresponding well-founded solution. Instead, it
% precomputes the solved game, then only considers moves for deletion
% that are drawn (in the solved game). It then recomputes the solved
% game on the graph without the deleted edges. This program also
% computes the length of positions.
% 
% To run:
%   clingo wfs_wm_explanations_v2.lp GAME.lp --opt-mode=optN
% where GAME.lp contains move/2 facts. 
%----------------------------------------------------------------------

% positions in the graph
pos(X) :- move(X,_).
pos(X) :- move(_,X).

% solve the initial game
won_0(X) :- move(X,Y), lost_0(Y).
lost_0(X) :- pos(X), won_0(Y) : move(X,Y).
drawn_0(X) :- pos(X), not won_0(X), not lost_0(X).

% guess drawn edges to remove
{ del(X,Y) } :- move(X,Y), drawn_0(X), drawn_0(Y).

% keep all moves that aren't deleted
move_1(X,Y) :- move(X,Y), not del(X,Y).

% solve the win-move graph
won(X) :- move_1(X,Y), lost(Y).
lost(X) :- pos(X), won(Y) : move_1(X,Y).
drawn(X) :- pos(X), not won(X), not lost(X).

% select solutions without undecided positions
:- drawn(_).

% only select models with the fewest possible deletions
del_cnt(N) :- N = #count{ (X,Y) : del(X,Y)}.
#minimize {N : del_cnt(N)}.

% compute lengths of positions in the "repaired" answers
num(0 .. N) :- N = #count { X : pos(X) }.
len(X, 0) :- lost(X), not move_1(X,_).
len(X, N + 1) :- won(X), N = #min { M : move_1(X,Y), lost(Y), len(Y,M) }, num(N).
len(X, N + 1) :- lost(X), move_1(X,_), N = #max { M : move_1(X,Y), len(Y,M) }, num(N).

% output 
#show del/2.
#show won/1.
#show drawn/1.
#show lost/1.
#show len/2.

