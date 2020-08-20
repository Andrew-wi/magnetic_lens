#!/bin/sh

# create list of values over which to scan z-deceleration
distances=($(seq 0 0.1 0.6));

# loop through decelerations and run plot_propagation.py
for i in ${distances[@]};
do
  for j in ${distances[@]};
  do
    python plot_propagation.py $i $j;
  done
done
