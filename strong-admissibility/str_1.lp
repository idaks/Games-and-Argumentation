
% From: Dvorak, Wallner. Computing Strongly Admissible Sets (2020)

attacks(b,a).
attacks(h,b).
attacks(i,h).
attacks(j,i).
attacks(k,j).
attacks(l,k).
attacks(g,f).
attacks(g,e).
attacks(g,d).
attacks(f,c).
attacks(e,c).
attacks(d,c).
attacks(c,b).


% What are the strongly admissible sets for a? 
:- not in(a).

