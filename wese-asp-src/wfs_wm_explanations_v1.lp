%----------------------------------------------------------------------
% An example program that provides minimal well-founded explanations
% of a simple game graph using Clingo's "conditional literal" syntax
% for solving win-move games. This program hard-codes the decided
% portion of the corresponding well-founded solution to ensure only
% undecided (i.e., drawing) moves are removed.
% 
% To run:
%   clingo wfs_wm_explanations_v1.lp --opt-mode=optN
%----------------------------------------------------------------------

% simple move graph
m(a,b). m(b,a). m(b,c). m(c,d). 

% positions in the graph
pos(X) :- m(X,_).
pos(X) :- m(_,X).

% guess edges to remove
{ del(X,Y) } :- m(X,Y).

% keep all moves that aren't deleted
move(X,Y) :- m(X,Y), not del(X,Y).

% solve the win-move graph
won(X) :- move(X,Y), lost(Y).
lost(X) :- pos(X), won(Y) : move(X,Y).
drawn(X) :- pos(X), not won(X), not lost(X).

% select solutions without undecided positions
:- drawn(_).

% These constraints should not be hard-wired: 
:- not won(c).      % the WF values .. 
:- not lost(d).     % .. shall be respected!
:- del(b,c).        % no actual provenance edges should be deleted
:- del(c,d).        % ...

% only select models with the fewest possible deletions
del_cnt(N) :- N = #count{ (X,Y) : del(X,Y)}.
#minimize {N : del_cnt(N)}.

% output 
#show del/2.
#show won/1.
#show drawn/1.
#show lost/1.


% Modal Logic checks: 
% [] won(c), lost(d).
