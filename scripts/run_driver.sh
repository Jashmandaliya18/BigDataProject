#!/bin/bash
# Usage: run_driver.sh [reducers=2] [combiner yes|no = yes] [output=/f1/output/driver]
R=${1:-2}; C=${2:-yes}; OUT=${3:-/f1/output/driver}
P=/project/src/processing
JAR=/opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar
COMB=()
[ "$C" = "yes" ] && COMB=(-combiner "python3 driver_reducer.py combine")
hdfs dfs -rm -r -f $OUT
hadoop jar $JAR -D mapreduce.job.name="F1-driver-performance" -D mapreduce.job.reduces=$R \
  -files $P/driver_mapper.py,$P/driver_reducer.py,$P/lookups/participants.txt \
  -mapper "python3 driver_mapper.py" "${COMB[@]}" \
  -reducer "python3 driver_reducer.py" \
  -input /f1/raw/racetime -output $OUT
