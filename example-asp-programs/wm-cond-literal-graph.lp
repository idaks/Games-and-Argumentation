
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

attr(graph_nodes, default, style, filled).

digraph(default).
