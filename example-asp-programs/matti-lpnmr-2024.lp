
attack(b,e).
attack(c,e).
attack(e,e).
attack(a,d).
attack(d,a).
attack(c,d).
attack(d,c).

move(X,Y) :- attack(Y,X).