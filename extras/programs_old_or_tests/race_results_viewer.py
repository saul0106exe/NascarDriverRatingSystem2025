import tkinter as tk
from tkinter import ttk
import pandas as pd
import json
import os

class RaceResultsViewer(tk.Tk):
    def __init__(self, tracks_metadata):
        super().__init__()

        self.tracks_metadata = tracks_metadata
        self.race_map = {track['race_name']: track for track in self.tracks_metadata}

        self.title("NASCAR Race Results Viewer")
        self.geometry("800x600")

        # --- Widgets ---
        # Frame for dropdown
        top_frame = ttk.Frame(self)
        top_frame.pack(pady=10, padx=10, fill='x')

        # Label for the combobox
        race_label = ttk.Label(top_frame, text="Select a Race:")
        race_label.pack(side='left', padx=(0, 5))

        # Combobox (dropdown)
        self.race_selection = ttk.Combobox(
            top_frame,
            values=list(self.race_map.keys()),
            state="readonly"
        )
        self.race_selection.pack(expand=True, fill='x', side='left')
        self.race_selection.bind("<<ComboboxSelected>>", self.display_race_results)

        # Frame for the results table
        results_frame = ttk.Frame(self)
        results_frame.pack(pady=10, padx=10, expand=True, fill='both')

        # Treeview for displaying results
        self.results_tree = ttk.Treeview(
            results_frame,
            columns=('Finish', 'Driver', 'Start', 'Laps Led'),
            show='headings'
        )
        self.results_tree.heading('Finish', text='Finish Pos')
        self.results_tree.heading('Driver', text='Driver')
        self.results_tree.heading('Start', text='Start Pos')
        self.results_tree.heading('Laps Led', text='Laps Led')

        # Column widths
        self.results_tree.column('Finish', width=80, anchor='center')
        self.results_tree.column('Driver', width=250)
        self.results_tree.column('Start', width=80, anchor='center')
        self.results_tree.column('Laps Led', width=80, anchor='center')

        # Scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient='vertical', command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)

        self.results_tree.pack(side='left', expand=True, fill='both')
        scrollbar.pack(side='right', fill='y')

    def display_race_results(self, event=None):
        # Clear previous results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        selected_race_name = self.race_selection.get()
        track_info = self.race_map.get(selected_race_name)

        if not track_info:
            return

        csv_filename = os.path.basename(track_info['race_lap_info_file-path'])
        # Assuming the CSVs are in a 'track_info' subfolder relative to where the script is run
        csv_path = os.path.join('track_info', csv_filename)

        try:
            laps_df = pd.read_csv(csv_path)
            
            # Get final results for each driver
            results_df = laps_df.loc[laps_df.groupby('driver_name')['lap_number'].idxmax()]
            
            # Calculate laps led
            laps_led = laps_df[laps_df['running_position'] == 1].groupby('driver_name').size().reset_index(name='laps_led')
            
            # Merge results with laps led
            final_results = pd.merge(results_df, laps_led, on='driver_name', how='left').fillna(0)
            final_results['laps_led'] = final_results['laps_led'].astype(int)
            
            # Sort by finishing position
            final_results = final_results.sort_values(by='finish_position')

            # Populate the treeview
            for _, row in final_results.iterrows():
                self.results_tree.insert('', 'end', values=(row['finish_position'], row['driver_name'], row['starting_position'], row['laps_led']))

        except FileNotFoundError:
            self.results_tree.insert('', 'end', values=("", f"Results file not found: {csv_path}", "", ""))

if __name__ == '__main__':
    with open('track_list.json', 'r') as f:
        all_tracks_data = json.load(f)
    
    app = RaceResultsViewer(all_tracks_data)
    app.mainloop()