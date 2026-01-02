<<<<<<< HEAD
# Changelog
All notable changes to the NASCAR Driver Rating System project will be documented in this file.

## 📜 [v1.2] - Gamify Update

### Released: 11-26-2025

**"The Video Game Update"** - Added new system with logic to scale the top performer to a perfect 100, creating distinct "attribute" style ratings where the leader sets the curve.

#### Added

* **Gamified Scaling Engine:** implemented a dynamic adjustment system that identifies the highest-rated driver in every category (Overall, Superspeedway, etc.) and scales them to a perfect 100.00.
* **Curve Adjustment:** Automatically adjusts all other drivers' scores relative to the category leader (e.g., if Leader is 92, everyone gets +8), preserving statistical gaps while maximizing the scale.
* **Precision Formatting:** All ratings are now strictly rounded to 2 decimal places for cleaner console output.

#### Changed

* Modified the final DataFrame generation to apply the (100 - max_score) offset to every column before printing.
* analyze_all_tracks now performs a final pass over the aggregated data to normalize the top value.

## 📜 [v1.1] - Full Initial Release

### Released: 11-25-2025

**"Season Manager Edition"** - The shift from a single-script test to a comprehensive season management tool capable of handling multiple races and track types.

#### Added

* **Season Aggregation**: System now calculates an OVR (Overall) rating by averaging performance across multiple races.
* **Track Categorization:** Introduced columns to break down ratings by specific track types:
    * SSW (Superspeedway)
    * SW (Speedway)
    * INT (Intermediate)
    * RC (Road Course)
    * C (Concrete)
    * S.INT (Short Intermediate)

* **JSON Configuration**: Added support for `track_list.json` to manage the schedule, file paths, and track metadata dynamically.

* **Batch Processing**: Created analyze_all_tracks() to iterate through the schedule file automatically.

* **Directory Management**: implemented logic to read race data from a dedicated track_info/ folder.

* **Smart Fill**: Added logic to handle drivers who missed specific races (fills missing categories with x instead of crashing).

#### Removed

* Hardcoded file paths in the main execution block.

## 📜 [v0.1] - Daytona 500 Era 

### Released: 11-18-2025

**"Proof of Concept"** - Initial test run using raw data from the 2025 Daytona 500.

#### Added

* **Core Rating Algorithm**: Established the weighted 6-metric formula:
    * Finish Pos (30%)
    * Avg Running Pos (25%)
    * Pos Gained (15%)
    * Speed (15%)
    * Laps Led (10%)
    * Fastest Lap (5%)

* **Data Parsing**: Basic integration with LapRaptor .csv export format.

* **Normalization**: implemented Min-Max normalization to convert disparate units (mph, time, position) into a unified 0-100 scale.

=======
# Changelog
All notable changes to the NASCAR Driver Rating System project will be documented in this file.

## 📜 [v1.2] - Gamify Update

### Released: 11-26-2025

**"The Video Game Update"** - Added new system with logic to scale the top performer to a perfect 100, creating distinct "attribute" style ratings where the leader sets the curve.

#### Added

* **Gamified Scaling Engine:** implemented a dynamic adjustment system that identifies the highest-rated driver in every category (Overall, Superspeedway, etc.) and scales them to a perfect 100.00.
* **Curve Adjustment:** Automatically adjusts all other drivers' scores relative to the category leader (e.g., if Leader is 92, everyone gets +8), preserving statistical gaps while maximizing the scale.
* **Precision Formatting:** All ratings are now strictly rounded to 2 decimal places for cleaner console output.

#### Changed

* Modified the final DataFrame generation to apply the (100 - max_score) offset to every column before printing.
* analyze_all_tracks now performs a final pass over the aggregated data to normalize the top value.

## 📜 [v1.1] - Full Initial Release

### Released: 11-25-2025

**"Season Manager Edition"** - The shift from a single-script test to a comprehensive season management tool capable of handling multiple races and track types.

#### Added

* **Season Aggregation**: System now calculates an OVR (Overall) rating by averaging performance across multiple races.
* **Track Categorization:** Introduced columns to break down ratings by specific track types:
    * SSW (Superspeedway)
    * SW (Speedway)
    * INT (Intermediate)
    * RC (Road Course)
    * C (Concrete)
    * S.INT (Short Intermediate)

* **JSON Configuration**: Added support for `track_list.json` to manage the schedule, file paths, and track metadata dynamically.

* **Batch Processing**: Created analyze_all_tracks() to iterate through the schedule file automatically.

* **Directory Management**: implemented logic to read race data from a dedicated track_info/ folder.

* **Smart Fill**: Added logic to handle drivers who missed specific races (fills missing categories with x instead of crashing).

#### Removed

* Hardcoded file paths in the main execution block.

## 📜 [v0.1] - Daytona 500 Era 

### Released: 11-18-2025

**"Proof of Concept"** - Initial test run using raw data from the 2025 Daytona 500.

#### Added

* **Core Rating Algorithm**: Established the weighted 6-metric formula:
    * Finish Pos (30%)
    * Avg Running Pos (25%)
    * Pos Gained (15%)
    * Speed (15%)
    * Laps Led (10%)
    * Fastest Lap (5%)

* **Data Parsing**: Basic integration with LapRaptor .csv export format.

* **Normalization**: implemented Min-Max normalization to convert disparate units (mph, time, position) into a unified 0-100 scale.

>>>>>>> master
* **Single Race Output**: Simple console printout of driver ratings for one event.