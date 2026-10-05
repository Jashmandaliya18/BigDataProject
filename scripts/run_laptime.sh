#!/bin/bash
P=/project/src/processing
JAR=/opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar
for MODE in trend fastest; do
  OUT=/f1/output/lap_$MODE
  hdfs dfs -rm -r -f $OUT
  hadoop jar $JAR -D mapreduce.job.name="F1-laptime-$MODE" -D mapreduce.job.reduces=2 \
    -files $P/laptime_mapper.py,$P/stats_reducer.py,$P/lookups/sessions.txt,$P/lookups/participants.txt \
    -mapper "python3 laptime_mapper.py $MODE" \
    -combiner "python3 stats_reducer.py combine" \
    -reducer "python3 stats_reducer.py" \
    -input /f1/raw/racetime -output $OUT
done
