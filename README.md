# 2025 NASCAR Driver Rating System (NDRS25)
### *Version 1.0 - Daytona 500 Era*

## 🏁 System Overview
This Python-based rating system evaluates NASCAR driver performance for the 2025 season. Unlike simple points standings, this model utilizes raw, lap-by-lap data to generate a comprehensive **Driver Rating (0-100)**. 

The system currently processes data from the **Daytona 500 (Feb 16, 2025)** but is being developed to scale for the full season.

## 📊 Data Sources & Requirements
The system ingests raw CSV data provided by **[LapRaptor.com](https://www.lapraptor.com)**.

### Required CSV Columns
The input file must contain the following headers:
`driver_name`, `driver_id`, `manufacturer`, `car_number`, `lap_number`, `running_position`, `lap_speed`, `lap_time`, `team`, `playoffs`, `points_ineligible`, `starting_position`, `finish_position`, `statuses`

## 🧮 Methodology

The rating is calculated in three stages: **Aggregation**, **Normalization**, and **Weighting**.

### 1. Metric Aggregation
For every driver, the script calculates six key performance metrics:

| Metric | Description |
| :--- | :--- |
| **Finish Position** | The final position of the driver at the end of the race. |
| **Avg Running Position** | The mean of the driver's position across all completed laps. |
| **Positions Gained** | The difference between `starting_position` and `finish_position`. |
| **Avg Lap Speed** | The mean speed (mph) across all valid laps. |
| **Laps Led** | The total number of laps where the driver's `running_position` was 1. |
| **Fastest Lap Time** | The single lowest lap time recorded by the driver. |

### 2. Score Normalization (0-100 Scale)
To make different units comparable (e.g., speed vs. position), all metrics are normalized to a 0-100 scale using **Min-Max Normalization**.

* **Standard Metrics:** (Higher is Better)
    * *Positions Gained, Avg Lap Speed, Laps Led*
    * Formula: `100 * (Value - Min) / (Max - Min)`
* **Inverted Metrics:** (Lower is Better)
    * *Finish Position, Avg Running Position, Fastest Lap Time*
    * Formula: `100 * (Max - Value) / (Max - Min)`

### 3. The Weighted Formula
The final **Driver Rating** is a weighted sum of the normalized scores. The system prioritizes finishing well and running up front consistently.

| Metric Component | Weight | Impact |
| :--- | :--- | :--- |
| **Finish Position** | **30%** | High |
| **Avg Running Position** | **25%** | High |
| **Positions Gained** | **15%** | Medium |
| **Avg Lap Speed** | **15%** | Medium |
| **Laps Led** | **10%** | Medium |
| **Fastest Lap Time** | **05%** | Low |

> **The Master Formula:**
> 
> `Rating = 0.30(Finish) + 0.25(AvgPos) + 0.15(PosGained) + 0.15(Speed) + 0.10(Led) + 0.05(Fastest)`

---

## 💻 Usage Guide

### Prerequisites
* Python 3.x
* pandas library (`pip install pandas`)

### Running the Script
1.  Ensure your CSV file is located in the directory.
2.  Update the `csv_file_path` variable in the `__main__` block if necessary.
3.  Run the script:

```bash
python rating_system_test.py
