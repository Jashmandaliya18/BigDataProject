db = db.getSiblingDB("f1db");

print("\n== Q1: Drivers holding the fastest lap on the most circuits");
printjson(db.lap_fastest.aggregate([
  { $sort: { track: 1, fastest: 1 } },
  { $group: { _id: "$track", driver: { $first: "$driver" } } },
  { $group: { _id: "$driver", circuits: { $sum: 1 } } },
  { $sort: { circuits: -1 } }, { $limit: 10 }
]).toArray());

print("\n== Q2: Fastest circuits by average speed");
printjson(db.circuit_speed.find({}, { _id: 0, track: 1, avg_speed: 1 }).sort({ avg_speed: -1 }).limit(10).toArray());

print("\n== Q3: Top 10 drivers by maximum speed");
printjson(db.speed_driver.aggregate([
  { $group: { _id: "$driver", top_speed: { $max: "$max_speed" } } },
  { $sort: { top_speed: -1 } }, { $limit: 10 }
]).toArray());

print("\n== Q4: Pit-stop leaders (total stops)");
printjson(db.pit_stops.aggregate([
  { $group: { _id: "$driver", stops: { $sum: "$stops" } } },
  { $sort: { stops: -1 } }, { $limit: 10 }
]).toArray());

print("\n== Q5: Average speed by tyre compound");
printjson(db.tyre_speed.find({}, { _id: 0 }).sort({ avg_speed: -1 }).toArray());

print("\n== Q6: Most consistent drivers (lowest std)");
printjson(db.driver_stats.find({}, { _id: 0, driver: 1, std: 1, laps: 1 }).sort({ std: 1 }).limit(5).toArray());

print("\n== Q7: Lap-time trend, Mexico, first 10 laps");
printjson(db.lap_trend.find({ track: "Mexico" }, { _id: 0, lap: 1, avg_lap: 1 }).sort({ lap: 1 }).limit(10).toArray());
