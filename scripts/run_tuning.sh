#!/bin/bash
# Driver job with 1/2/4 reducers, with and without combiner.
RES=/project/output/tuning_results.txt
echo "reducers combiner seconds combine_in combine_out shuffle_bytes" > $RES
for r in 1 2 4; do
  for c in yes no; do
    START=$SECONDS
    LOG=$(bash /project/scripts/run_driver.sh $r $c /f1/output/tuning/driver_r${r}_${c} 2>&1)
    T=$((SECONDS - START))
    CI=$(echo "$LOG" | grep "Combine input records" | grep -o '[0-9]*$')
    CO=$(echo "$LOG" | grep "Combine output records" | grep -o '[0-9]*$')
    SB=$(echo "$LOG" | grep "Reduce shuffle bytes" | grep -o '[0-9]*$')
    echo "$r $c $T ${CI:-0} ${CO:-0} ${SB:-0}" | tee -a $RES
  done
done
hdfs dfs -rm -r -f /f1/output/tuning
