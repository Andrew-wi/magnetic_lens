#!/bin/sh

# dependencies
trials=5; # number of trials at each scan_point

# create list of values over which to scan z-deceleration
z_decels=($(seq -0 -10000 -170000));

# create new csv file and write header to it
touch manual_test.csv;
printf "z_decel," > manual_test.csv;
vals=($(seq 0 1 $trials));
printf "%s," "${vals[@]}" >> manual_test.csv;
printf "\n" >> manual_test.csv;

# loop through and perform plot_propagation
for i in ${z_decels[@]};
do
  printf "Z-axis deceleration: %f\n" $i;
  printf "%f," $i >> manual_test.csv;
  for j in ${vals[@]};
  do
    printf "Trial number: %i\n" $j;
    # python manual_prop.py $j >> log_manual_prop.txt;
    python manual_prop.py $i | grep "Success rate:" | sed 's/^.*: //' | tr -d '\n' >> manual_test.csv;
    printf "," >> manual_test.csv;
  done
  printf "\n" >> manual_test.csv;
  printf "";
done
