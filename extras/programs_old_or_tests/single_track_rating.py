import pandas as pd

def calculate_driver_ratings(csv_path):

    try:
        laps_df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: The file was not found at {csv_path}")
        return None

    drivers = laps_df['driver_name'].unique()
    
    driver_stats = []

    for driver in drivers:
        driver_laps = laps_df[laps_df['driver_name'] == driver].copy()
        
        if driver_laps.empty:
            continue

        start_pos = driver_laps['starting_position'].iloc[0]
        finish_pos = driver_laps['finish_position'].iloc[0]
        
        positions_gained = start_pos - finish_pos
        avg_pos = driver_laps['running_position'].mean()
        avg_speed = driver_laps['lap_speed'].mean()
        fastest_lap = driver_laps['lap_time'].min()
        laps_led = len(driver_laps[driver_laps['running_position'] == 1])

        driver_stats.append({
            'driver_name': driver,
            'finish_position': finish_pos,
            'positions_gained': positions_gained,
            'avg_running_position': avg_pos,
            'avg_lap_speed': avg_speed,
            'fastest_lap_time': fastest_lap,
            'laps_led': laps_led
        })

    stats_df = pd.DataFrame(driver_stats)

    for col in ['positions_gained', 'avg_lap_speed', 'laps_led']:
        min_val = stats_df[col].min()
        max_val = stats_df[col].max()
        if max_val - min_val > 0:
            stats_df[f'{col}_score'] = 100 * (stats_df[col] - min_val) / (max_val - min_val)
        else:
            stats_df[f'{col}_score'] = 100

    for col in ['finish_position', 'avg_running_position', 'fastest_lap_time']:
        min_val = stats_df[col].min()
        max_val = stats_df[col].max()
        if max_val - min_val > 0:
            stats_df[f'{col}_score'] = 100 * (max_val - stats_df[col]) / (max_val - min_val)
        else:
            stats_df[f'{col}_score'] = 100

    weights = {
        'finish_position_score': 0.30,
        'avg_running_position_score': 0.25,
        'positions_gained_score': 0.15,
        'avg_lap_speed_score': 0.15,
        'laps_led_score': 0.10,
        'fastest_lap_time_score': 0.05
    }

    stats_df['driver_rating'] = (
        stats_df['finish_position_score'] * weights['finish_position_score'] +
        stats_df['avg_running_position_score'] * weights['avg_running_position_score'] +
        stats_df['positions_gained_score'] * weights['positions_gained_score'] +
        stats_df['avg_lap_speed_score'] * weights['avg_lap_speed_score'] +
        stats_df['laps_led_score'] * weights['laps_led_score'] +
        stats_df['fastest_lap_time_score'] * weights['fastest_lap_time_score']
    )

    final_ratings = stats_df.sort_values(by='driver_rating', ascending=False)

    return final_ratings[['driver_name', 'driver_rating']]


if __name__ == '__main__':
    csv_file_path = "CODENAME_NSIGHT\\track_info\\2.16.25daytona.csv"
    
    driver_ratings_df = calculate_driver_ratings(csv_file_path)

    if driver_ratings_df is not None:
        print("--- NASCAR Driver Ratings ---")
        print(driver_ratings_df.to_string(index=False))

