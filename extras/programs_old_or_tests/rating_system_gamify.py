import pandas as pd
import json
import os
import tkinter as tk
from tkinter import ttk

def calculate_driver_ratings(csv_path):
    try:
        laps_df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f" Error | The file was not found at {csv_path}")
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

    # metric scores
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

    # calc weights
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

    min_rating = stats_df['driver_rating'].min()
    max_rating = stats_df['driver_rating'].max()
    
    # *avoiding division by 0
    if max_rating - min_rating > 0:
        stats_df['driver_rating'] = 75 + (stats_df['driver_rating'] - min_rating) * (100 - 75) / (max_rating - min_rating)
    else:
        stats_df['driver_rating'] = 100 # If all ratings are equal, set all to 100

    # sort, decending
    final_ratings = stats_df.sort_values(by='driver_rating', ascending=False)

    return final_ratings[['driver_name', 'driver_rating']]


def get_all_ratings_data(tracks_metadata):
    all_ratings = []
    for track in tracks_metadata:

        if str(track.get('point_race')).lower() != 'true':
            print(f"--- {track ['race_num']} |-{track['race_date']}-| Skipping {track['race_name']}")
            continue

        csv_file_path = os.path.join('track_info', os.path.basename(track['race_lap_info_file-path']))
        
        print(f"--- {track ['race_num']} | {track['race_date']} | Analyzing {track['race_name']}")
        ratings_df = calculate_driver_ratings(csv_file_path)

        if ratings_df is not None:
            ratings_df['track_category'] = track['track_category']
            all_ratings.append(ratings_df)
        else:
            print(f" Error | Could not calculate ratings for {track['race_name']}.")

    if not all_ratings:
        print("\nNo ratings could be calculated from the provided files.")
        return None

    # single df
    combined_ratings_df = pd.concat(all_ratings)

    # calcs----
    # ovr
    overall_ratings = combined_ratings_df.groupby('driver_name')['driver_rating'].mean().reset_index()
    overall_ratings = overall_ratings.rename(columns={'driver_rating': 'Overall_rating'})

    # category
    category_ratings_pivot = combined_ratings_df.pivot_table(
        index='driver_name',
        columns='track_category',
        values='driver_rating',
        aggfunc='mean'
    ).reset_index()

    # merge ovr and cat. ratings
    final_df = pd.merge(overall_ratings, category_ratings_pivot, on='driver_name', how='outer')

    # rounder
    for col in final_df.columns:
        if final_df[col].dtype in ['float64', 'int64']:
            final_df[col] = final_df[col].round(2)

    final_df = final_df.sort_values(by='Overall_rating', ascending=False)

    # columns 
    # | OVR | SSW | SW | INT | S.INT | C | RC |
    final_df = final_df.rename(columns={
        'driver_name': 'Driver',
        'Overall_rating': 'OVR',
        'Superspeedway': 'SSW',
        'Speedway': 'SW',
        'Intermediate': 'INT',
        'Short Intermediate': 'S.INT',
        'Concrete': 'C',
        'Road Course': 'RC',
    })

    # fill value for missing ratings
    final_df.fillna('x', inplace=True)

    return final_df


class DriverRatingsViewer(tk.Tk):
    def __init__(self, ratings_df):
        super().__init__()

        self.ratings_df = ratings_df
        self.title("Saul's Nascar Driver Ratings")
        self.geometry("900x700")

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#2E2E2E",
                        foreground="white",
                        fieldbackground="#2E2E2E",
                        rowheight=25)
        style.configure("Treeview.Heading",
                        background="#4A4A4A",
                        foreground="white",
                        font=('Calibri', 10, 'bold'))
        style.map('Treeview.Heading',
                  background=[('active', '#6A6A6A')])

        results_frame = ttk.Frame(self, padding="10")
        results_frame.pack(expand=True, fill='both')

        columns = list(self.ratings_df.columns)
        self.results_tree = ttk.Treeview(
            results_frame,
            columns=columns,
            show='headings'
        )

        for col in columns:
            self.results_tree.heading(col, text=col, command=lambda c=col: self.sort_by_column(c, False))
            self.results_tree.column(col, width=80, anchor='center')

        self.results_tree.column('Driver', width=150, anchor='w')

        scrollbar = ttk.Scrollbar(results_frame, orient='vertical', command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)

        self.results_tree.pack(side='left', expand=True, fill='both')
        scrollbar.pack(side='right', fill='y')

        self.populate_treeview()

    def populate_treeview(self):
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        for _, row in self.ratings_df.iterrows():
            self.results_tree.insert('', 'end', values=list(row))

    def sort_by_column(self, col, reverse):
        for c in self.ratings_df.columns:
            self.results_tree.heading(c, text=c)

        sortable_series = pd.to_numeric(self.ratings_df[col], errors='coerce').fillna(0)

        if reverse:
            self.ratings_df = self.ratings_df.iloc[sortable_series.argsort()]
        else:
            self.ratings_df = self.ratings_df.iloc[sortable_series.argsort()[::-1]]

        self.populate_treeview()

        arrow = ' ▲' if not reverse else ' ▼'
        self.results_tree.heading(col, text=col + arrow)

        self.results_tree.heading(col, command=lambda c=col: self.sort_by_column(c, not reverse))

if __name__ == '__main__': 
    json_file_path = 'track_list.json'

    try:
        with open(json_file_path, 'r') as f:
            tracks_metadata = json.load(f)
        
        final_ratings_data = get_all_ratings_data(tracks_metadata)

        if final_ratings_data is not None:
            app = DriverRatingsViewer(final_ratings_data)
            app.mainloop()

    except FileNotFoundError:
        print(f" Error | The file was not found at {json_file_path}")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from the file at {json_file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
