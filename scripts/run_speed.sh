#!/bin/bash
# Usage: run_speed.sh [modes...]   default: driver band tyre
P=/project/src/processing
JAR=/opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar
MODES=${*:-driver band tyre}
for MODE in $MODES; do
  OUT=/f1/output/speed_$MODE
  hdfs dfs -rm -r -f $OUT
  hadoop jar $JAR -D mapreduce.job.name="F1-speed-$MODE" -D mapreduce.job.reduces=2 \
    -files $P/speed_mapper.py,$P/stats_reducer.py \
    -mapper "python3 speed_mapper.py $MODE" \
    -combiner "python3 stats_reducer.py combine" \
    -reducer "python3 stats_reducer.py" \
    -input /f1/clean/telemetry -output $OUT
done
