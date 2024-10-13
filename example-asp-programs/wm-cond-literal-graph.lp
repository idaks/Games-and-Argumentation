
%----------------------------------------------------------------------
% Draw it
%
% To install clingraph: 
%    conda install -c potassco clingraph
%    conda install -c potassco/label/dev clingraph

node(X) :- won(X).
node(X) :- lost(X).
node(X) :- drawn(X).
edge((X,Y)) :- move(X,Y).

attr(edge, (X,Y), label, N+1) :- move(X,Y), won(X), lost(Y), len(Y,N).
attr(edge, (X,Y), label, N+1) :- move(X,Y), lost(X), won(Y), len(Y,N).
attr(edge, (X,Y), color, green3) :- move(X,Y), won(X), lost(Y).
attr(edge, (X,Y), color, red2) :- move(X,Y), lost(X), won(Y).
attr(edge, (X,Y), color, yellow2) :- move(X,Y), drawn(X), drawn(Y).
attr(edge, (X,Y), label, "&infin;") :- move(X,Y), drawn(X), drawn(Y).
attr(edge, (X,Y), style, dashed) :- move(X,Y), won(X), won(Y).
attr(edge, (X,Y), style, dashed) :- move(X,Y), won(X), drawn(Y).
attr(edge, (X,Y), style, dashed) :- move(X,Y), drawn(X), lost(Y).
attr(edge, (X,Y), color, darkgray) :- move(X,Y), won(X), won(Y).
attr(edge, (X,Y), color, darkgray) :- move(X,Y), won(X), drawn(Y).
attr(edge, (X,Y), color, darkgray) :- move(X,Y), drawn(X), lost(Y).

attr(edge, (X,Y), style, dashed) :- move(X,Y), won(X), lost(Y), len(Y,N), move(X,Z), lost(Z), len(Z,N0), N > N0. 
attr(edge, (X,Y), constraint, false) :- move(X,Y), won(X), lost(Y), len(Y,N), move(X,Z), lost(Z), len(Z,N0), N > N0.

attr(node, X, label, (X,N)) :- won(X), len(X,N).
attr(node, X, label, (X,N)) :- lost(X), len(X,N).
attr(node, X, label, (X,"&infin;")) :- drawn(X).

attr(node, X, style, filled) :- node(X).
attr(node, X, fillcolor, red2) :- lost(X).
attr(node, X, fillcolor, green3) :- won(X).
attr(node, X, fillcolor, yellow2) :- drawn(X).
