#!/bin/sh

clingo wm-cond-literal.lp tapp24.lp wm-cond-literal-graph.lp --outf=2  > tmp.json
clingraph --type=digraph tmp.json --out=dot > tmp.dot
dot -Tpdf tmp.dot > tmp.pdf
open tmp.pdf
