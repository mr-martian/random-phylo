#!/bin/bash

for args in {50,100,200}\ {0.05,0.10,0.15,0.20}
do
  echo $args
  date
  time ./run_iteration.sh 1000 $args > "results_$args.tsv"
done

for args in {0.05,0.10,0.15,0.20}
do
  echo $args
  date
  time ./run_iteration.sh 10000 $args > "results_$args.tsv"
done
