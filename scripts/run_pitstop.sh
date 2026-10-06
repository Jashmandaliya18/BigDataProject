#!/bin/bash
P=/project/src/processing
JAR=/opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar

hdfs dfs -rm -r -f /f1/output/pit_laps
hadoop jar $JAR -D mapreduce.job.name="F1-pit-laps" -D mapreduce.job.reduces=2 \
  -files $P/pit_laps_mapper.py,$P/pit_laps_reducer.py \
  -mapper "python3 pit_laps_mapper.py" \
  -reducer "python3 pit_laps_reducer.py" \
  -input /f1/clean/telemetry -output /f1/output/pit_laps

hdfs dfs -rm -r -f /f1/output/pit_summary
hadoop jar $JAR -D mapreduce.job.name="F1-pit-summary" -D mapreduce.job.reduces=2 \
  -files $P/pit_summary_mapper.py,$P/stats_reducer.py \
  -mapper "python3 pit_summary_mapper.py" \
  -combiner "python3 stats_reducer.py combine" \
  -reducer "python3 stats_reducer.py" \
  -input /f1/output/pit_laps -output /f1/output/pit_summary
