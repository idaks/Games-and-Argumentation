pos(X) :- move(X,_).
pos(X) :- move(_,X).

won(X) :- move(X,Y), lost(Y).
lost(X) :- pos(X), won(Y) : move(X,Y).
drawn(X) :- pos(X), not won(X), not lost(X).

len(X, 0) :- lost(X), not move(X,_).
len(X, N+1) :- won(X),  N = #min{ M : move(X,Y), lost(Y), len(Y,M) }.
len(X, N+1) :- lost(X), N = #max{ M : move(X,Y), len(Y,M) }. 

#show won/1.
#show lost/1.
#show drawn/1.
#show len/2.
