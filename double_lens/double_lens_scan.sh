#!/bin/sh

# dependencies
trials=10; # number of trials at each scan_point

# create list of values over which to lens distances
distances=($(seq 0 0.05 0.5));

# create new csv file and write header to it
touch manual_test.csv;
printf "lens_1_dist,lens_2_dist," > manual_test.csv;
vals=($(seq 0 1 $trials));
printf "%s," "${vals[@]}" >> manual_test.csv;
printf "\n" >> manual_test.csv;

# loop through and perform plot_propagation
for i in ${distances[@]};
do
  for j in ${distances[@]};
  do
    printf "lens positions: %f, %f\n" $i $j;
    printf "%f,%f," $i $j >> manual_test.csv;
    for k in ${vals[@]};
    do
      printf "Trial number: %i\n" $k;
      # python manual_prop.py $j >> log_manual_prop.txt;
      python manual_prop.py $i $j | grep "Success rate:" | sed 's/^.*: //' | tr -d '\n' >> manual_test.csv;
      printf "," >> manual_test.csv;
    done
    printf "\n" >> manual_test.csv;
  done
done
