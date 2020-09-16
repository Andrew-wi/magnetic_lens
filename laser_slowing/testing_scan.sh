#!/bin/sh

# set python path
export PYTHONPATH="'':'/Library/Frameworks/Python.framework/Versions/3.7/lib/python37.zip':'/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7':'/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/lib-dynload':'/Users/andrewwinnicki/Library/Python/3.7/lib/python/site-packages':'/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages'";

# dependencies
trials=0 ; # number of trials at each scan_point

# create new csv file and write header to it
touch manual_test.csv;
printf "l_cell_to_lens_aperture," > manual_test.csv;
vals=($(seq 0 1 $trials));
printf "%s," "${vals[@]}" >> manual_test.csv;
printf "\n" >> manual_test.csv;

# create range of values to scan lens distance over
lens_dist=($(seq 0 0.05 0.6));

# # create log file and overwrite old
# touch log_manual_prop.txt;
# printf "" > log_manual_prop.txt;

# loop through and perform plot_propagation
for i in "${lens_dist[@]}";
do
  printf "Lens distance: %f\n" $i;
  printf "%f," $i >> manual_test.csv;
  for j in "${vals[@]}";
  do
    printf "Trial number: %i\n" $j;
    # python manual_prop.py $j >> log_manual_prop.txt;
    python manual_prop.py $i | grep "Success rate:" | sed 's/^.*: //' | tr -d '\n' >> manual_test.csv;
    printf "," >> manual_test.csv;
  done
  python plot_propagation.py $i;
  printf "\n" >> manual_test.csv;
  printf "";
done
