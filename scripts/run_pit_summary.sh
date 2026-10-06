#!/bin/bash
P=/project/src/processing
JAR=/opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar
hdfs dfs -rm -r -f /f1/output/pit_summary
hadoop jar $JAR -D mapreduce.job.name="F1-pit-summary" -D mapreduce.job.reduces=2 \
  -files $P/pit_summary_mapper.py,$P/pit_summary_reducer.py \
  -mapper "python3 pit_summary_mapper.py" \
  -reducer "python3 pit_summary_reducer.py" \
  -input /f1/output/pit_laps -output /f1/output/pit_summary
