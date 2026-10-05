#!/bin/bash
if [ ! -d /hadoop/dfs/name/current ]; then
  echo "Formatting NameNode (first run only)..."
  hdfs namenode -format -force
fi
start-dfs.sh
start-yarn.sh
mapred --daemon start historyserver
echo "--- jps (master) ---"; jps
