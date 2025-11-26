# 2025 NASCAR Driver Rating System (NDRS25)
### *Version 1.1 (Full Initial Release) - 2025 NCS*

## 🏁 System Overview
This Python-based rating system evaluates NASCAR driver performance for the 2025 season. Unlike simple points standings, this model utilizes raw, lap-by-lap data to generate a comprehensive **Driver Rating (0-100)**. 

At first **(v.1.0)** this program just processed data from the Daytona 500 but now **(v.1.1)**, it processes data from all races from the full **2025 NASCAR Cup Series**. Not just that, drivers arent just given a rating for the whole season but a **rating for each type of track**, from superspeedways to road courses.

## 📊 Data Sources & Requirements
The system uses raw CSV data provided by **[LapRaptor.com](https://www.lapraptor.com)**.

### Required File Structure
```text 
/project_root
 │
 ├── rating_system.py       # The main script
 ├── track_list.json        # Configuration file for the schedule
 └── track_info/            # Folder containing all race CSV files
      ├── 2.02.25bowman_gray.csv
      ├── 2.13.25daytona_duel_1.csv
      └── ...
```

### Required CSV Columns
The input file must contain the following headers:
`driver_name`, `driver_id`, `manufacturer`, `car_number`, `lap_number`, `running_position`, `lap_speed`, `lap_time`, `team`, `playoffs`, `points_ineligible`, `starting_position`, `finish_position`, `statuses`

### Required Config. keys
- `race_num`: Number to easily identify in the .json file
- `race_name`:  Name of the race 
- `race_date`:  Date of the race
- `track_category`: Defines what type of track rating is going to go into
- `point_race`: Defines if the race is going or not going to be used in  ratings
- `race_lap_info_file-path`: The file path for .csv files  
### **Hint**: Other config. keys may be used for future updates😊

## 🧮 Methodology

The system operates in two distinct phases: **Individual Race Scoring** (calculating the 0-100 score for a single event), **Season Aggregation** (combining those scores into an Overall Rating to Season Overall or Track Category Overall), and for `rating_system_gamify`, **Gamify Scaling** (boosting ratings by adding the diffence of 100 minus the highest rating for each category to all ratings)

---

### Phase 1: Individual Race Scoring
For every specific race, the rating is calculated in three stages: **Aggregation**, **Normalization**, and **Weighting**.

#### 1. Metric Aggregation
For every driver, the script calculates six key performance metrics:

| Metric | Description |
| :--- | :--- |
| **Finish Position** | The final position of the driver at the end of the race. |
| **Avg Running Position** | The mean of the driver's position across all completed laps. |
| **Positions Gained** | The difference between `starting_position` and `finish_position`. |
| **Avg Lap Speed** | The mean speed (mph) across all valid laps. |
| **Laps Led** | The total number of laps where the driver's `running_position` was 1. |
| **Fastest Lap Time** | The single lowest lap time recorded by the driver. |

#### 2. Score Normalization (0-100 Scale)
To make different units comparable (e.g., speed vs. position), all metrics are normalized to a 0-100 scale using **Min-Max Normalization**.

* **Standard Metrics:** (Higher is Better)
    * *Positions Gained, Avg Lap Speed, Laps Led*
    * Formula: `100 * (Value - Min) / (Max - Min)`
* **Inverted Metrics:** (Lower is Better)
    * *Finish Position, Avg Running Position, Fastest Lap Time*
    * Formula: `100 * (Max - Value) / (Max - Min)`

#### 3. The Weighted Formula
The final **Driver Rating** is a weighted sum of the normalized scores. The system prioritizes finishing well and running up front consistently.

| Metric Component | Weight | Impact |
| :--- | :--- | :--- |
| **Finish Position** | **30%** | High |
| **Avg Running Position** | **25%** | High |
| **Positions Gained** | **15%** | Medium |
| **Avg Lap Speed** | **15%** | Medium |
| **Laps Led** | **10%** | Medium |
| **Fastest Lap Time** | **5%** | Low |

> **Raw Formula:**
> 
> `Rating = 0.30(Finish) + 0.25(AvgPos) + 0.15(PosGained) + 0.15(Speed) + 0.10(Led) + 0.05(Fastest)`

---

### Phase 2: Season Aggregation
Once individual races are scored, the system aggregates the data to track long-term performance.

#### 4. Global Metrics
The system groups the individual race ratings to generate the following high-level stats:

| Aggregated Metric | Description |
| :--- | :--- |
| **OVR (Overall Rating)** | The simple average of the driver's rating across *all* points-paying races. |
| **Track Category Rating** | The average rating for specific track types (e.g., "Superspeedway"). |

#### 5. Aggregation Logic
The system dynamically calculates averages based on the `track_category` defined in `track_list.json`.

* **Overall Formula:**
    * `OVR = Sum(All Ratings) / Count(All Races)`
* **Category Formula:**
    * `Category Score = Sum(Ratings in Category) / Count(Races in Category)`
* **Exclusions:**
    * Races marked `point_race: "false"` are excluded from OVR.
    * Drivers who did not compete in a category receive an `'x'` placeholder.

---

### Phase 3: Gamified Scaling (The Curve) 
#### **This applies for `rating_system_gamify.py` only.**

To create the final ratings, the system identifies the "Class Leader" for each category and shifts the curve so the leader sits at 100.

The Logic:
1. Find the highest Raw Score in a specific column (e.g., Superspeedways).
2. Calculate the `Adjustment Factor = 100 - Leader's Score`.
3. Add the `Adjustment Factor` to every driver's score in that column.


## 💻 Usage Guide

### Prerequisites
* Python 3.x
* pandas library (`pip install pandas`)

### Ensure your `track_list.json` has the following
```
[
    {
        "race_num": "1",
        "race_name": "Daytona 500",
        "race_date": "2.16.25",
        "track_category": "Superspeedway",
        "point_race": "true",
        "race_lap_info_file-path": "2.16.25daytona_laps.csv"
    }
]
```

### Execution
Run  the **Orginal** script from your Terminal:
```
python rating_system.py
```

Rub the **Gamified** script from your Terminal:
```
python rating_system_gamify.py
```
### Understand the Output
#### Legend:
|  | Description |
| :--- | :--- |
OVR | Overall  Rating
SSW | Superspeedway (Daytona, Talladega, Atlanta)
SW | Speedway (Large ovals)
INT| Intermediate (1.5-mile tracks)
S.INT | Short-Intermediate (e.g., Darlington, Gateway)
C | Concrete (Bristol, Dover, Nashville)
RC | Road Course
x | Indicates the driver has not competed in this track category yet.
