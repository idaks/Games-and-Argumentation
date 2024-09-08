
% example showing that the well-founded (decided) position lengths can
% change after a repair

move(a,b).
move(b,a).
move(c,b).
move(c,d).
move(d,e).
move(e,f).


% #show won_0/1.
% #show lost_0/1.
% #show drawn_0/1.