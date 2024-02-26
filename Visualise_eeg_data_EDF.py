
import mne
import os
import numpy as np
import matplotlib.pyplot as plt

# Replace 'your_folder_path' with the actual path to your folder containing edf files
folder_path = r"C:\Users\danie\OneDrive\Desktop\Biomedical_engineering_PHD\Argenina_pasantia\EEG_DATA\prueba_Agus_BrainVision_160124"

# Get a list of all edf files in the folder
edf_files = [file for file in os.listdir(folder_path) if file.endswith('.edf')]

# Initialize an empty list to store raw data objects
raw_list = []

# Loop through each edf file and load EEG data
for edf_file in edf_files:
    # Construct the full path to the edf file
    edf_path = os.path.join(folder_path, edf_file)

    # Load EEG data from the edf file
    raw = mne.io.read_raw_edf(edf_path, preload=True)

    # Apply lighter filtering
    raw.filter(l_freq=1, h_freq=40)  # Adjust these values based on your data characteristics
    raw.notch_filter(freqs=[50], method='spectrum_fit')  # Use only a single frequency for notch

    # Optional: Resample to a lower sampling rate, but if its low enough not neccesary 
    #raw.resample(100)  # Adjust the resampling rate based on your needs

    # # Apply ICA for artifact removal
    ica = mne.preprocessing.ICA(n_components=min(5, len(raw.ch_names) - 1), random_state=97, max_iter=800)
    ica.fit(raw, reject=dict(eeg=200e-6))  # Adjust the rejection threshold based on your needs
    raw = ica.apply(raw)

    # Append the raw data object to the list and filename
    raw_list.append((raw, edf_file))

# Plot the EEG data for each file
for raw, filename in raw_list:
    raw.plot(n_channels=30, scalings={'eeg': 75e-6}, title= f'Filtered EEG data - {filename}')

# Show the plots
plt.show()
