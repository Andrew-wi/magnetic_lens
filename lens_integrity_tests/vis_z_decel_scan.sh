#!/bin/sh

# create list of values over which to scan z-deceleration
z_decels=($(seq -0 -10000 -170000));

# loop through decelerations and run plot_propagation.py
for decel in ${z_decels[@]};
do
  python plot_propagation.py $decel;
done
