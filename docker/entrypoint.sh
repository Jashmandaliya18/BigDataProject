#!/bin/bash

set -e

service ssh start

if [ "$HOSTNAME" = "master" ]; then
    if [ ! -d "/hadoop/dfs/name/current" ]; then
        echo "Formatting NameNode..."
        hdfs namenode -format -force
    fi

    start-dfs.sh
    start-yarn.sh

    echo "Hadoop master started."
else
    echo "Hadoop worker started."
fi

tail -f /dev/null