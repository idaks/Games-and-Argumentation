%======================================================================
% Taken from:
%   Dvorak, Wallner. Computing Strongly Admissible Sets (2020)
% Added:
%   Length computation.
% To run:
%   clingo str_adm.lp str_1.lp 0
% See str_1_graphs.pdf for corresponding AFs for each result
%======================================================================

% grab each argument from the attacks
arg(X) :- attacks(X,_).
arg(X) :- attacks(_,X).

% guess in/out such that conflict free
in(X) :- arg(X), not out(X).
out(X) :- arg(X), not in(X).

% consider models whose in-labels are justified_in
:- in(X), not justified_in(X).

% x is justified-in if it is in and everything that attacks it is
% defeated
justified_in(X) :- in(X), defeated(Y) : attacks(Y,X).

% x is defeated if it is attacked by at least one in argument that is
% justified-in
defeated(X) :- arg(X), justified_in(Y), attacks(Y,X).

% compute the lengths of the in and out labeled arguments
num(0 .. N) :- N = #count{X : arg(X)}.
len(X,0) :- in(X), not attacks(_,X).
len(X, N+1) :- out(X), N = #min{M : attacks(Y,X), in(Y), len(Y,M)}, num(N).
len(X, N+1) :- in(X), attacks(_,X), N = #min{M : attacks(Y,X), len(Y,M)}, num(N).

% extend in and out labels with the lengths
in(X,N) :- in(X), len(X,N).
out(X,N) :- out(X), len(X,N).

% display the extended in and out labels
#show in/2.
#show out/2.


