%----------------------------------------------------------------------
% wm-cond-literal.lp
%
% Basic program and test game for 3-valued well-founded solutions of
% win-move games using Clingo's support for conditional iterals.
%
% TO RUN: clingo wm-cond-literal.lp GAME.lp 0
%
%----------------------------------------------------------------------


position(X) :- move(X,_).
position(X) :- move(_,X).

lost(X) :- position(X), won(Y) : move(X,Y).
won(X) :- move(X,Y), lost(Y).
drawn(X) :- position(X), not won(X), not lost(X).

num(0 .. N) :- N = #count { X : position(X) }.
len(X, 0) :- lost(X), not move(X,_).
len(X, N + 1) :- won(X), N = #min { M : move(X,Y), lost(Y), len(Y,M) }, num(N).
len(X, N + 1) :- lost(X), move(X,_), N = #max { M : move(X,Y), len(Y,M) }, num(N).

