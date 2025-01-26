
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

% PW1: won(red). lost(white). won(pasta). won(meat). lost(fish).
:- lost(red).
:- won(white).
:- lost(pasta).
:- lost(meat).
:- won(fish).

% PW2:
% lost(red). won(white). won(pasta). won(meat). lost(fish).
%% :- won(red).
%% :- lost(white).
%% :- lost(pasta).
%% :- lost(meat).
%% :- won(fish).

% PW3:
% lost(red). won(white). won(pasta). lost(meat). won(fish). 
%% :- won(red).
%% :- lost(white).
%% :- lost(pasta).
%% :- won(meat).
%% :- lost(fish).

% PW4:
% lost(red). won(white). lost(pasta). won(meat). won(fish). 
%% :- won(red).
%% :- lost(white).
%% :- won(pasta).
%% :- lost(meat).
%% :- lost(fish).

