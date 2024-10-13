#program base.
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
lost(X) :- position(X); won(Y): move(X,Y).
won(X) :- move(X,Y); lost(Y).
drawn(X) :- position(X); not won(X); not lost(X).
#show won/1.
#show lost/1.
#show drawn/1.
