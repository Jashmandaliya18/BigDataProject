#!/bin/bash
cd /project/src/processing/lookups
f=$(ls /project/dataset/RaceTimeData_*.csv | head -1)
export mapreduce_map_input_file=$f
echo "== mapper sample =="; python3 ../driver_mapper.py < $f 2>/dev/null | head -3
echo "== full pipeline: cat | mapper | sort | reducer =="
python3 ../driver_mapper.py < $f 2>/dev/null | sort | python3 ../driver_reducer.py
echo "== combiner check =="
diff <(python3 ../driver_mapper.py < $f 2>/dev/null | sort | python3 ../driver_reducer.py) \
     <(python3 ../driver_mapper.py < $f 2>/dev/null | sort | python3 ../driver_reducer.py combine | sort | python3 ../driver_reducer.py) \
  && echo "COMBINER OK (same result with and without)"
