#!/bin/sh

clingo wm-cond-literal.lp tapp24.lp wm-cond-literal-graph.lp --outf=2  > tapp24.json
clingraph --type=digraph tapp24.json --out=dot > tapp24.dot
dot -Tpdf tapp24.dot > tapp24.pdf
