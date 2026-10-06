# Distributed Formula 1 (2020) Telemetry & Race Analytics Pipeline

A distributed Big Data analytics platform processing over **23.6 Million telemetry records (~12.3 GB raw data)** across 22 Formula 1 Grand Prix sessions using **Apache Hadoop (HDFS & YARN)**, **Python Hadoop Streaming MapReduce**, and **MongoDB NoSQL**, fully containerized via **Docker**.

---

## 🏎️ Project Overview & Key Highlights

* **Scale:** 22 Race Sessions, 88 CSV datasets, **23,642,682 telemetry rows**, processed across 99 distributed splits.
* **Cluster:** 3-Node Hadoop 3.3.6 Cluster (1 Master + 2 Workers) orchestrated via Docker Compose with dedicated bridge networking.
* **Processing Framework:** Python 3 Hadoop Streaming MapReduce featuring distributed memory-efficient lookup joins, in-mapper combining, and custom statistics reducers.
* **Data Cleansing:** Map-only distributed ETL removing 1,920 malformed records and out-of-bounds telemetry values into tiered HDFS storage (`/f1/clean/`).
* **Serving & NoSQL:** MongoDB 7 document database storing 10 distinct analytical collections with indexes on `driver` and `track`.
* **Visual Analytics:** Matplotlib chart generation covering circuit speeds, driver maximum speeds, pit-stop totals, tyre compound performance, and lap progression trends.

---

## 🏗️ Cluster Architecture & Node Allocation

The cluster follows a strict multi-node topology distributed among three team roles:

| Node | Container Hostname | Hadoop / Database Services | Responsibilities & Ownership |
|---|---|---|---|
| **Node 1 (Master)** | `master` | NameNode, SecondaryNameNode, ResourceManager, JobHistoryServer | **Student 1 (Cluster & Data Engineer):** Infrastructure, HDFS topology, ingestion, ETL cleaning job, Circuit-wise analytics. |
| **Node 2 (Worker 1)** | `worker1` | DataNode, NodeManager | **Student 2 (MapReduce Developer):** MapReduce streaming pipeline, local test harnesses, Driver analytics, Lap-time analysis, Combiner tuning. |
| **Node 3 (Worker 2)** | `worker2` / `mongodb` | DataNode, NodeManager, MongoDB 7 Server | **Student 3 (NoSQL & Analytics Engineer):** Telemetry speed analytics, Pit-stop analysis, HDFS-to-Mongo loader, MongoDB aggregations, Visual dashboards. |

### Web Interfaces & Port Forwarding
* **HDFS NameNode Web UI:** `http://localhost:9870`
* **YARN ResourceManager Web UI:** `http://localhost:8088`
* **MapReduce JobHistory Server:** `http://localhost:19888`
* **MongoDB Server:** `localhost:27017`

---

## 📁 Repository Structure

```text
BigDataProject/
├── config/
│   └── hadoop/                 # core-site.xml, hdfs-site.xml, yarn-site.xml, mapred-site.xml, workers
├── dataset/                    # F1 2020 raw CSV files (Session, RaceTime, Telemetry, Participant)
├── docker/
│   └── Dockerfile              # Hadoop 3.3.6 image with Java 11 & Python 3 + PyMongo
├── docs/
│   ├── mongo_schema.md         # Schema documentation for MongoDB collections
│   └── SYSTEM_DESIGN.md        # Comprehensive distributed system architecture document
├── output/                     # Execution logs, tuning results, sample outputs, MongoDB results
├── screenshots/
│   ├── charts/                 # Generated analytical PNG charts (c1 through c6)
│   └── *.png                   # Cluster verification, YARN execution, and output screenshots
├── scripts/
│   ├── start_cluster.sh        # HDFS format & daemon initialization script
│   ├── run_clean.sh            # Distributed telemetry cleaning job
│   ├── run_circuit.sh          # Job 1: Circuit speed and lap-time analytics
│   ├── run_driver.sh           # Job 2: Driver consistency and lap time analysis
│   ├── run_laptime.sh          # Job 3: Lap-time progression and fastest laps
│   ├── run_speed.sh            # Job 4: Driver speed, speed distribution bands, tyre compound speed
│   ├── run_pitstop.sh          # Job 5: Pit-lane frame detection & summary analytics
│   ├── run_tuning.sh           # Reducer and Combiner benchmarking harness
│   └── mongo_queries.js        # MongoDB aggregation pipeline queries
├── src/
│   ├── analytics/
│   │   ├── load_to_mongo.py    # Type-casting HDFS-to-MongoDB ingestion loader
│   │   └── charts.py           # Visualization script producing publication-ready charts
│   ├── ingestion/
│   │   └── ingest_to_hdfs.sh   # Automated HDFS upload by data modality
│   └── processing/
│       ├── lookups/            # Broadcast lookups: sessions.txt, participants.txt
│       ├── clean_mapper.py     # Map-only cleaner & validator
│       ├── driver_mapper.py    # Driver analytics mapper
│       ├── driver_reducer.py   # Driver stats aggregator (mean, best, standard deviation)
│       ├── stats_reducer.py    # General reusable stats combiner/reducer (count, sum, min, max)
│       ├── laptime_mapper.py   # Lap trend & circuit fastest lap mapper
│       ├── speed_mapper.py     # Telemetry speed mapper (driver, band, tyre modes)
│       ├── pit_laps_mapper.py  # Pit lane frame detector
│       └── pit_summary_mapper.py
├── docker-compose.yml          # Multi-container orchestration definition
└── README.md
```

---

## 🔄 End-to-End Analytics Workflow

```text
[ Raw CSV Datasets (22 Sessions / 88 Files) ]
                       │
                       ▼  (ingest_to_hdfs.sh)
      [ HDFS: /f1/raw/ (Replication Factor = 2) ]
                       │
                       ▼  (run_clean.sh: Map-only MapReduce)
      [ HDFS: /f1/clean/telemetry (23.64M Valid Rows) ]
                       │
      ┌────────────────┼──────────────────────────────┐
      ▼                ▼                              ▼
[ Job 1: Circuit ] [ Jobs 2 & 3: Driver & Laps ] [ Jobs 4 & 5: Speed & Pitstop ]
(Speed & Laptime)   (Avg, StdDev, Trend)         (Bands, Tyres, In-pit Frames)
      └────────────────┬──────────────────────────────┘
                       ▼
          [ HDFS: /f1/output/* (TSV) ]
                       │
                       ▼  (load_to_mongo.py)
        [ MongoDB 7: f1db (10 Collections) ]
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
[ mongo_queries.js ]         [ charts.py ]
 (Aggregations & Viva)     (Visual Artifacts)
```

---

## ⚙️ MapReduce Jobs Summary

| Job Name | Script | Mapper | Combiner | Reducer | Input -> Output |
|---|---|---|---|---|---|
| **Data Cleaning** | `run_clean.sh` | `clean_mapper.py` | None | None (Map-only) | `/f1/raw/telemetry` -> `/f1/clean/telemetry` |
| **Circuit Analytics** | `run_circuit.sh` | `circuit_speed_mapper.py`<br>`circuit_laptime_mapper.py` | `stats_reducer.py combine` | `stats_reducer.py` (2 reducers) | `/f1/clean/telemetry` & `/f1/raw/racetime`<br>-> `/f1/output/circuit_*` |
| **Driver Performance**| `run_driver.sh` | `driver_mapper.py` | `driver_reducer.py combine` | `driver_reducer.py` (2 reducers) | `/f1/raw/racetime` -> `/f1/output/driver` |
| **Lap-time Analysis** | `run_laptime.sh` | `laptime_mapper.py` (`trend`/`fastest`) | `stats_reducer.py combine` | `stats_reducer.py` (2 reducers) | `/f1/raw/racetime` -> `/f1/output/lap_*` |
| **Speed Analytics**   | `run_speed.sh` | `speed_mapper.py` (`driver`/`band`/`tyre`)| `stats_reducer.py combine` | `stats_reducer.py` (2 reducers) | `/f1/clean/telemetry` -> `/f1/output/speed_*` |
| **Pit-Stop Analytics**| `run_pitstop.sh` | `pit_laps_mapper.py`<br>`pit_summary_mapper.py` | `stats_reducer.py combine` | `pit_laps_reducer.py`<br>`stats_reducer.py` | `/f1/clean/telemetry` -> `/f1/output/pit_*` |

---

## 🚀 Execution & Quick Start Guide

### Step 1: Start Docker Containers
```bash
docker compose up -d
docker ps
```

### Step 2: Initialize Cluster & Format HDFS (Run inside Master)
```bash
docker exec -it master bash
bash /project/scripts/start_cluster.sh
```
Verify daemons with `jps` on all nodes and check cluster status:
```bash
hdfs dfsadmin -report
yarn node -list
```

### Step 3: Ingest Dataset to HDFS
```bash
bash /project/src/ingestion/ingest_to_hdfs.sh
hdfs dfs -ls /f1/raw/
```

### Step 4: Run ETL Cleaning Job
```bash
bash /project/scripts/run_clean.sh
```

### Step 5: Execute Analytics MapReduce Jobs
```bash
bash /project/scripts/run_circuit.sh
bash /project/scripts/run_driver.sh
bash /project/scripts/run_laptime.sh
bash /project/scripts/run_speed.sh
bash /project/scripts/run_pitstop.sh
```

### Step 6: Ingest HDFS Results into MongoDB
```bash
python3 /project/src/analytics/load_to_mongo.py
```

### Step 7: Execute Analytical Queries & Generate Visualizations
Inside MongoDB container:
```bash
mongosh < /scripts/mongo_queries.js
```
On the host machine (generates charts in `screenshots/charts/`):
```bash
python src/analytics/charts.py Mexico
```

---

## 📊 Key Analytical Insights

1. **Top Circuit Speeds:** Silverstone (222.43 km/h average) and Spa-Francorchamps (222.30 km/h) are the fastest circuits on the 2020 calendar.
2. **Top Driver Speeds:** Valtteri Bottas recorded the peak speed of **346 km/h**, closely followed by Kimi Räikkönen (344 km/h).
3. **Tyre Compound Performance:** Soft tyres averaged **197.83 km/h** across 6.9M samples, Hard tyres averaged **195.00 km/h**, and Mediums averaged **191.04 km/h**.
4. **Driver Consistency:** George Russell recorded the lowest lap-time standard deviation (**11.98s** across 588 laps), proving exceptional consistency.
5. **Circuit Mastery:** Max Verstappen achieved the fastest lap on **5 separate circuits**, leading all drivers.

---

## 👥 Team Roles & Responsibilities

* **Student 1 (Cluster & Data Engineer - Master Node):** Cluster deployment, HDFS & YARN configurations, tiered ingestion, map-only telemetry cleaning pipeline, and Circuit-level MapReduce analytics.
* **Student 2 (MapReduce Developer - Worker 1):** Worker 1 node integration, local streaming test harnesses, Driver performance & consistency reducer algorithms, lap-time trend analysis, and Combiner/Reducer tuning benchmarks.
* **Student 3 (NoSQL & Analytics Engineer - Worker 2):** Worker 2 & MongoDB 7 integration, telemetry speed bands & tyre compound mappers, pit-lane frame detection, typed HDFS-to-Mongo loader with indexing, analytical aggregation queries, and visualization charts.
