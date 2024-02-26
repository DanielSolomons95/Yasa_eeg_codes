import numpy as np
import mne
import yasa
from sklearn.metrics import accuracy_score
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os

# Base directory where all participant data is stored
base_directory = r'C:\Users\danie\OneDrive\Desktop\Biomedical_engineering_PHD\Argenina_pasantia\EEG_DATA'

# Loop through each participant
for root, dirs, files in os.walk(base_directory):
    # Check if the current directory contains 'EDF' and 'Hypnograms'
    if 'EDF' in dirs and 'Hypnograms' in dirs:
        participant_directory = os.path.join(root)

        # Full paths to EEG file
        eeg_data_directory = os.path.join(participant_directory, 'EDF')
        eeg_files = [file for file in os.listdir(eeg_data_directory) if file.endswith(".edf")]

        # Check if EEG data directory contains at least one .edf file
        if not eeg_files:
            print(f"Skipping participant in '{participant_directory}' due to missing or empty 'EDF' directory.")
            continue

        eeg_file_path = os.path.join(eeg_data_directory, eeg_files[0])

        # Full paths to Hypnogram file
        hypnogram_directory = os.path.join(participant_directory, 'Hypnograms')
        hypnogram_files = [file for file in os.listdir(hypnogram_directory) if file.endswith("sleepStages.csv")]

        # Check if Hypnograms directory contains at least one sleepStages.csv file
        if not hypnogram_files:
            print(f"Skipping participant in '{participant_directory}' due to missing or empty 'Hypnograms' directory.")
            continue

        hypnogram_file_path = os.path.join(hypnogram_directory, hypnogram_files[0])

        # Check if the hypnogram file exists
        if os.path.exists(hypnogram_file_path):
            # Read hypnogram
            hypno = yasa.hypno_str_to_int(np.array(pd.read_csv(hypnogram_file_path)).flatten())

            # Assuming the prediction is done here
            sls = yasa.SleepStaging(...)  # Replace ... with your parameters
            hypno_pred = sls.predict()
            hypno_pred = yasa.hypno_str_to_int(hypno_pred)

            print(f"Processed hypnogram from '{hypnogram_file_path}'.")
        else:
            print(f"Hypnogram file not found for participant in '{participant_directory}'. Skipping.")
            continue  # Skip the rest of the loop if hypnogram file is not found

        # Rest of your code goes here (after the 'if' block)
        # ...

        # Print accuracy
        print(f"The accuracy for participant in '{participant_directory}' is {100 * accuracy_score(hypno, hypno_pred):.2f}%\n")
