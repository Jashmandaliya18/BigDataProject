#!/bin/bash
# Builds session->track and (session,pilot)->driver lookup tables from the small CSVs
OUT=/project/src/processing/lookups
mkdir -p $OUT
echo "sessionId,trackId,totalLaps,trackLength,weather,trackTemp,airTemp" > $OUT/sessions.txt
echo "sessionId,pilot_index,driverId,teamId" > $OUT/participants.txt
for f in /project/dataset/SessionData_*.csv; do
  id=$(basename $f .csv); id=${id#SessionData_}
  tail -n +2 $f | tr -d '\r' | awk -F, -v id=$id '{print id","$6","$4","$5","$1","$2","$3}' >> $OUT/sessions.txt
done
for f in /project/dataset/ParticipantData_*.csv; do
  id=$(basename $f .csv); id=${id#ParticipantData_}
  tail -n +2 $f | tr -d '\r' | awk -F, -v id=$id '{print id","$1","$3","$4}' >> $OUT/participants.txt
done
wc -l $OUT/*.txt
