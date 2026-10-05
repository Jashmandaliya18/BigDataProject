#!/bin/bash
P=/project/src/processing
JAR=/opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar

hdfs dfs -rm -r -f /f1/output/circuit_speed
hadoop jar $JAR -D mapreduce.job.name="F1-circuit-speed" -D mapreduce.job.reduces=2 \
  -files $P/circuit_speed_mapper.py,$P/stats_reducer.py \
  -mapper "python3 circuit_speed_mapper.py" \
  -combiner "python3 stats_reducer.py combine" \
  -reducer "python3 stats_reducer.py" \
  -input /f1/clean/telemetry -output /f1/output/circuit_speed

hdfs dfs -rm -r -f /f1/output/circuit_laptime
hadoop jar $JAR -D mapreduce.job.name="F1-circuit-laptime" -D mapreduce.job.reduces=2 \
  -files $P/circuit_laptime_mapper.py,$P/stats_reducer.py,$P/lookups/sessions.txt \
  -mapper "python3 circuit_laptime_mapper.py" \
  -combiner "python3 stats_reducer.py combine" \
  -reducer "python3 stats_reducer.py" \
  -input /f1/raw/racetime -output /f1/output/circuit_laptime

echo "== speed (track, samples, avg, min, max) =="; hdfs dfs -cat /f1/output/circuit_speed/part-*
echo "== laptime (track, laps, avg, fastest, slowest) =="; hdfs dfs -cat /f1/output/circuit_laptime/part-*
