# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 12:18:34 2023

@author: Daniel
"""

import mne
import yasa
import pandas as pd
import numpy as np
import os
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# Directory containing the EEG data files
eeg_folder = "C:/Users/danie/OneDrive/Desktop/Biomedical_engineering_PHD/Argenina_pasantia/EEG_DATA/EDF/"

# Directory containing the hypnogram CSV files
hypno_folder = "C:/Users/danie/OneDrive/Desktop/Biomedical_engineering_PHD/Argenina_pasantia/EEG_DATA/Hypnograms/"

# Get a list of all EEG files in the directory
eeg_files = [file for file in os.listdir(eeg_folder) if file.endswith(".edf")]


# Create a DataFrame to store accuracy information
accuracy_data = pd.DataFrame(columns=['Participant', 'Channel', 'Accuracy'])


# Loop over each EEG file
for eeg_file in eeg_files:
    eeg_path = os.path.join(eeg_folder, eeg_file)
    
    # Print information about the current EEG file
    print(f"\nProcessing EEG file: {eeg_file}")

    # Get corresponding hypnogram file
    hypno_file = eeg_file.replace("_eeg.edf", "_sleepStages.csv")
    hypno_path = os.path.join(hypno_folder, hypno_file)
    
    # Print information about the current hypnogram file
    print(f"Matching hypnogram: {hypno_file}")

    # Read hypnogram data using Pandas
    hypno = pd.read_csv(hypno_path)
    
    # Assuming 'sleep_stage' is the column containing sleep stage information
    hypno = np.array(hypno)
    hypno = np.array(hypno).flatten()
    
    # Convert sleep stage labels from string to integer using yasa.hypno_str_to_int
    hypno = yasa.hypno_str_to_int(hypno)
    
    # Read raw EEG data for each file
    raw = mne.io.read_raw_edf(eeg_path, preload=True)
    
    if not hasattr(raw, 'channels_dropped'):
        # Preprocessing steps for each file
        raw.resample(100)
        raw.filter(0.3, 45)
        sf = raw.info['sfreq']

        # # Drop specified channels
        # raw.drop_channels(['Marca', 'A1-A2', 'EMG', 'EOG1', 'EOG2'])
        # # Drop specified channels only if 'Marca' is present
        if 'Marca' in raw.ch_names:
            raw.drop_channels(['Marca', 'A1-A2', 'EOG1', 'EOG2'])
            raw.channels_dropped = True
        # chan = raw.ch_names
        chan = raw.ch_names if hasattr(raw, 'channels_dropped') else raw.ch_names + ['Marca']


        # Set flag to indicate that channels have been dropped
        raw.channels_dropped = True
        chan = raw.ch_names
    #get rid of Marca with try 
    channel_accuracies = {}
    # Sleep staging and prediction
    # Loop over each channel
    for channel in chan:
        try:
            # Sleep staging and prediction for the current channel
            sls = yasa.SleepStaging(raw, eeg_name=channel, emg_name="EMG")
            hypno_pred_channel = sls.predict()
            hypno_pred_channel = yasa.hypno_str_to_int(hypno_pred_channel)
            # Print lengths of hypno and hypno_pred_channel
            print(f"Length of hypno for {eeg_file} - {channel}: {len(hypno)}")
            print(f"Length of hypno_pred_channel for {eeg_file} - {channel}: {len(hypno_pred_channel)}")

            # Plot hypnograms for each channel
            fig, axes = plt.subplots(nrows=2, figsize=(12, 8))
            axes[0].set_title(f'Hypnogram - Prediction - {eeg_file} - {channel}')
            yasa.plot_hypnogram(hypno_pred_channel, ax=axes[0])

            axes[1].set_title(f'Hypnogram - Actual {eeg_file} - {channel}')
            yasa.plot_hypnogram(hypno, ax=axes[1])

            plt.tight_layout()
            plt.show()
            
            
            data = raw.get_data(units="uV")
            hypno_up = yasa.hypno_upsample_to_data(hypno, sf_hypno=1 / 30, data=raw)
            yasa.plot_spectrogram(data[chan.index(channel)], sf, hypno_up)
            plt.title(f"Spectrogram - {channel}")
            plt.show()


            # Calculate and print accuracy for each channel
            accuracy_channel = accuracy_score(hypno, hypno_pred_channel)
            # Update the channel accuracy dictionary
            if channel not in channel_accuracies:
                channel_accuracies[channel] = []
                channel_accuracies[channel].append(accuracy_channel)

        except ValueError as e:
               print(f"Warning: {e}. Skipping channel {channel} for file {eeg_file}")
               continue
               print(f"The accuracy for {eeg_file} - {channel} is {100 * accuracy_channel:.2f}%")
            
           
        except ValueError as e:
            print(f"Warning: {e}. Skipping channel {channel} for file {eeg_file}")
            continue

    mean_channel_accuracies = {channel: np.mean(accuracies) for channel, accuracies in channel_accuracies.items()}
    
    # Save accuracy information to a CSV file
    # Save accuracy information to a CSV file with percentage formatting
    accuracy_data.to_csv("C:/Users/danie/OneDrive/Desktop/Biomedical_engineering_PHD/Argenina_pasantia/EEG_DATA/accuracy_results_EMG_EEG.csv", 
                    index=False, float_format='%.0f%%')

        
#check for same length of hypnograms before code starts as sanity check 

#Don't open file whilst it's being edited 
   