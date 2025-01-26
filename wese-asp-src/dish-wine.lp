
% the AF as a WM game
move(meat, fish).
move(meat, pasta).
move(fish, meat).
move(fish, pasta).
move(pasta, meat).
move(pasta, fish).
move(red, white).
move(white, red).
move(white, meat).
move(white, pasta).


% there are four possible worlds

% PW1: won(red). won(pasta). won(meat). lost(white). lost(fish).
:- won(white).
:- won(fish).

% PW2:
% won(white). won(pasta). won(meat). lost(red). lost(fish).
% :- won(red).
% :- won(fish).

% PW3:
% won(white). won(pasta). won(fish). lost(red). lost(meat).
% :- won(red).
% :- won(meat).

% PW4:
% won(white). won(meat). won(fish). lost(red). lost(pasta).
% :- won(red).
% :- won(pasta).
