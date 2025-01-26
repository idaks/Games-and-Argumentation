
% no stable solution

move(a, b).
move(b, a).
move(b, c).
move(c, c).


% preferred: lost(a), won(b), lost(c)

:- won(a).
:- lost(b).
:- won(c).