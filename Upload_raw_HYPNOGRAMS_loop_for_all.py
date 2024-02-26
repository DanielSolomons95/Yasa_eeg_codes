import os
import pandas as pd
import numpy as np
import yasa
import mne

source_directory = r'C:\Users\danie\OneDrive\Desktop\Biomedical_engineering_PHD\Argenina_pasantia\EEG_DATA'

if not os.path.exists(source_directory):
    print(f"Source directory '{source_directory}' does not exist.")
else:
    hypnogram_directory = os.path.join(source_directory, 'Hypnograms')

    if not os.path.exists(hypnogram_directory):
        print(f"Hypnogram directory '{hypnogram_directory}' does not exist.")
    else:
        # Use os.walk to traverse through the hypnogram subdirectory and its subdirectories
        for root, dirs, files in os.walk(hypnogram_directory):
            for hypnogram_file in files:
                hypnogram_path = os.path.join(root, hypnogram_file)

                # Check if the file is a CSV file
                if hypnogram_file.endswith('.csv'):
                    hypno = yasa.hypno_str_to_int(np.array(pd.read_csv(hypnogram_path)).flatten())
                    print(f"Processed hypnogram from '{hypnogram_path}'.")
                else:
                    print(f"Ignored non-CSV file: '{hypnogram_path}'.")
