#!/usr/bin/env python3
"""Reads MongoDB (published on localhost:27017) and saves PNG charts to screenshots/charts/.
Run on the host: python src/analytics/charts.py [track]"""
import os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pymongo import MongoClient

TRACK = sys.argv[1] if len(sys.argv) > 1 else "Mexico"
db = MongoClient("mongodb://localhost:27017")["f1db"]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "screenshots", "charts")
os.makedirs(OUT, exist_ok=True)

def barh(fname, title, rows, xlabel):
    if not rows:
        print("no data for", fname); return
    rows = rows[::-1]
    plt.figure(figsize=(9, 5))
    plt.barh([r[0] for r in rows], [r[1] for r in rows], color="#c0392b")
    plt.title(title); plt.xlabel(xlabel); plt.tight_layout()
    plt.savefig(os.path.join(OUT, fname), dpi=130); plt.close(); print("saved", fname)

barh("c1_avg_speed_by_circuit.png", "Average speed by circuit",
     [(d["track"], d["avg_speed"]) for d in db.circuit_speed.find().sort("avg_speed", -1)], "km/h")

barh("c2_top_speed_by_driver.png", "Top 10 drivers by maximum speed",
     [(d["_id"], d["v"]) for d in db.speed_driver.aggregate(
         [{"$group": {"_id": "$driver", "v": {"$max": "$max_speed"}}}, {"$sort": {"v": -1}}, {"$limit": 10}])], "km/h")

barh("c3_pit_stops_by_driver.png", "Pit stops by driver (all races)",
     [(d["_id"], d["v"]) for d in db.pit_stops.aggregate(
         [{"$group": {"_id": "$driver", "v": {"$sum": "$stops"}}}, {"$sort": {"v": -1}}, {"$limit": 10}])], "stops")

barh("c4_speed_by_tyre.png", "Average speed by tyre compound",
     [(d["tyre"], d["avg_speed"]) for d in db.tyre_speed.find().sort("avg_speed", -1)], "km/h")

trend = list(db.lap_trend.find({"track": TRACK}).sort("lap", 1))
if trend:
    plt.figure(figsize=(9, 4.5))
    plt.plot([d["lap"] for d in trend], [d["avg_lap"] for d in trend], marker="o")
    plt.title("Average lap time by lap number - " + TRACK); plt.xlabel("lap"); plt.ylabel("seconds")
    plt.tight_layout(); plt.savefig(os.path.join(OUT, "c5_lap_trend.png"), dpi=130); plt.close(); print("saved c5")

bands = list(db.speed_band.find({"track": TRACK}).sort("band", 1))
if bands:
    plt.figure(figsize=(9, 4.5))
    plt.bar([str(b["band"]) for b in bands], [b["samples"] for b in bands], color="#2c3e50")
    plt.title("Speed distribution (50 km/h bands) - " + TRACK); plt.xlabel("band start (km/h)"); plt.ylabel("telemetry frames")
    plt.tight_layout(); plt.savefig(os.path.join(OUT, "c6_speed_distribution.png"), dpi=130); plt.close(); print("saved c6")
