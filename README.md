# F1 2020 Big Data Analytics Project

A Big Data Analytics project that analyzes **Formula 1 (F1) 2020 race data** using **Apache Hadoop, HDFS, and MapReduce**. The project demonstrates how large-scale racing datasets can be processed and analyzed using distributed computing technologies.

## Technologies Used

* **Apache Hadoop 3.3.6**
* **HDFS (Hadoop Distributed File System)**
* **MapReduce**
* **Python**
* **Docker**
* **Docker Compose**
* **F1 2020 Dataset**

## Dataset

The project uses a comprehensive **Formula 1 2020 dataset** containing different types of racing and session-related data, including:

* Participant Data
* Race Time Data
* Session Data
* Telemetry Data
* Race and Driver Information

The dataset is processed and stored using **HDFS** before being analyzed through MapReduce jobs.

## Project Objectives

The main objectives of this project are:

1. Store large-scale F1 2020 datasets using **HDFS**.
2. Process the dataset using **Hadoop MapReduce**.
3. Perform analytics on Formula 1 race and driver data.
4. Demonstrate distributed data processing using a Hadoop cluster.
5. Generate meaningful analytical results from the F1 dataset.

## Project Structure

```text
BigDataProject/
│
├── config/
│   └── Hadoop configuration files
│
├── dataset/
│   └── F1 2020 dataset files
│
├── docker/
│   └── Docker-related configuration
│
├── output/
│   └── MapReduce output files
│
├── scripts/
│   └── Hadoop/HDFS execution scripts
│
├── src/
│   └── MapReduce source code
│
├── docker-compose.yml
└── README.md
```

## Hadoop Components

The project uses the following Hadoop components:

### HDFS

HDFS is used for distributed storage of the F1 2020 dataset. Large files are divided into blocks and distributed across the Hadoop cluster.

### MapReduce

MapReduce is used to process and analyze the F1 data in a distributed manner.

The **Mapper** processes the input data and generates intermediate key-value pairs, while the **Reducer** aggregates and processes those results to produce the final output.

## Workflow

```text
F1 2020 Dataset
       │
       ▼
     HDFS
       │
       ▼
   MapReduce
       │
   ┌───┴───┐
   ▼       ▼
 Mapper  Reducer
   │       │
   └───┬───┘
       ▼
   Final Output
```

## Running the Project

### 1. Start the Hadoop Cluster

Start the required Hadoop services using Docker Compose:

```bash
docker-compose up -d
```

### 2. Verify Running Containers

```bash
docker ps
```

### 3. Create an HDFS Input Directory

```bash
hdfs dfs -mkdir -p /input
```

### 4. Upload the Dataset to HDFS

```bash
hdfs dfs -put dataset/* /input/
```

### 5. Run the MapReduce Job

Run the required MapReduce script from the `src/` directory.

```bash
python <mapreduce_script>.py
```

> Replace `<mapreduce_script>.py` with the name of the MapReduce program being used.

### 6. View the Output

```bash
hdfs dfs -cat /output/*
```

The generated results can also be stored in the local `output/` directory for further analysis.

## Expected Output

The MapReduce jobs generate analytical results based on the F1 2020 dataset. These results can be used to study:

* Driver performance
* Race results
* Lap and race times
* Session information
* Telemetry-related data
* Other Formula 1 racing statistics

## Conclusion

This project demonstrates the use of **Big Data technologies for Formula 1 analytics**. By combining **HDFS, MapReduce, Python, and Docker**, the project provides a practical example of storing and processing large-scale racing data using a distributed computing environment.
