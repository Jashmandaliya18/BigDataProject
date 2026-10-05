#!/bin/bash
# Usage: run_clean.sh [input_path] [output_path]
IN=${1:-/f1/raw/telemetry}
OUT=${2:-/f1/clean/telemetry}
P=/project/src/processing
hdfs dfs -rm -r -f $OUT
hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
  -D mapreduce.job.name="F1-clean-telemetry" \
  -D mapreduce.job.reduces=0 \
  -files $P/clean_mapper.py,$P/lookups/sessions.txt,$P/lookups/participants.txt \
  -mapper "python3 clean_mapper.py" \
  -input $IN -output $OUT
hdfs dfs -du -h $OUT | tail -3
