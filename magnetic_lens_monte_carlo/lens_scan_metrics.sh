#!/bin/sh

# set python path
export PYTHONPATH="'':'/Library/Frameworks/Python.framework/Versions/3.7/lib/python37.zip':'/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7':'/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/lib-dynload':'/Users/andrewwinnicki/Library/Python/3.7/lib/python/site-packages':'/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages'";

# create range of values to scan lens distance over
lens_dist=($(seq 0 0.05 0.7));

# loop through and perform plot_propagation
for i in "${lens_dist[@]}";
do
  printf "Lens distance: %f\n" $i;
  python metrics.py $i;
  printf "";
done
