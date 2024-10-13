#!/bin/sh

clingo wm-cond-literal.lp matti-lpnmr-2024.lp wm-cond-literal-graph.lp --outf=2  > tmp.json
clinguin tmp.json --out=dot > tmp.dot
dot -Tpdf tmp.dot > tmp.pdf

