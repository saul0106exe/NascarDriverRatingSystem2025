import pandas as pd
import json
import os

def find_race_winner(csv_path):
    try:
        laps_df = pd.read_csv(csv_path)
        winner_df = laps_df[laps_df['finish_position'] == 1]
        if not winner_df.empty:
            return winner_df['driver_name'].iloc[0]
    except FileNotFoundError:
        return None
    except (KeyError, IndexError):
        return None
    return None

def detect_all_winners(tracks_metadata, base_folder='track_info'):
    print("--- NASCAR Race Winners ---")
    for track in tracks_metadata:
        csv_filename = os.path.basename(track['race_lap_info_file-path'])
        csv_path = os.path.join(base_folder, csv_filename)
        
        winner = find_race_winner(csv_path)
        
        if winner:
            print(f"{track['race_date_full']} | {track['track_name']} - {winner}")
            # print(f"On {track['race_date_full']}: {winner} won the {track['race_name']} @ {track['track_name']}")
        else:
            print(f"Could not determine a winner for {track['race_name']} from {csv_path}.")

if __name__ == '__main__':
    json_file_path = 'track_list.json'
    with open(json_file_path, 'r') as f:
        tracks_data = json.load(f)
    detect_all_winners(tracks_data)