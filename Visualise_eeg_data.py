import mne
import os
import numpy as np
import matplotlib.pyplot as plt

# Replace 'your_folder_path' with the actual path to your folder containing BDF files
folder_path = r'C:\Users\danie\OneDrive\Desktop\Biomedical_engineering_PHD\Argenina_pasantia\EEG_DATA\Pruebas_Bruno_Bioamp_281223'

# Get a list of all BDF files in the folder
bdf_files = [file for file in os.listdir(folder_path) if file.endswith('.bdf')]

# Initialize an empty list to store raw data objects
raw_list = []

# Loop through each BDF file and load EEG data
for bdf_file in bdf_files:
    # Construct the full path to the BDF file
    bdf_path = os.path.join(folder_path, bdf_file)

    # Load EEG data from the BDF file
    raw = mne.io.read_raw_bdf(bdf_path, preload=True)

    # Apply lighter filtering
    raw.filter(l_freq=1, h_freq=40)  # Adjust these values based on your data characteristics
    raw.notch_filter(freqs=[50], method='spectrum_fit')  # Use only a single frequency for notch

    # Optional: Resample to a lower sampling rate
    raw.resample(100)  # Adjust the resampling rate based on your needs

    # # Apply ICA for artifact removal
    ica = mne.preprocessing.ICA(n_components=min(5, len(raw.ch_names) - 1), random_state=97, max_iter=800)
    ica.fit(raw, reject=dict(eeg=200e-6))  # Adjust the rejection threshold based on your needs
    raw = ica.apply(raw)

    # Append the raw data object to the list and filename
    raw_list.append((raw, bdf_file))

# Plot the EEG data for each file
for raw, filename in raw_list:
    raw.plot(n_channels=30, scalings={'eeg': 75e-6}, title= f'Filtered EEG data - {filename}')

# Show the plots
plt.show()
