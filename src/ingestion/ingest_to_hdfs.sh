#!/bin/bash
# Run inside master. Uploads F1 2020 CSVs to HDFS grouped by type.
SRC=/project/dataset
hdfs dfs -mkdir -p /f1/raw/participant /f1/raw/racetime /f1/raw/session /f1/raw/telemetry /f1/clean /f1/output

declare -A MAP=( [ParticipantData]=participant [RaceTimeData]=racetime [SessionData]=session [TelemetryData]=telemetry )

for prefix in "${!MAP[@]}"; do
  dest=/f1/raw/${MAP[$prefix]}
  for f in $SRC/${prefix}_*.csv; do
    echo "Uploading $(basename $f) -> $dest"
    hdfs dfs -put -f "$f" "$dest/"
  done
done

echo "=== HDFS usage ==="
hdfs dfs -du -h /f1/raw