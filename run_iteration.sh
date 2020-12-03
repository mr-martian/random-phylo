#!/bin/bash

for i in $(seq $1)
do
  ./gentree.py $2 $3
  ./compare_reconstructions.R random_tree.nex random_matrix.nex
done
