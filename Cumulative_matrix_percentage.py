import mne 
import os 
import yasa 
import numpy as np
from sklearn.metrics import confusion_matrix 
import seaborn as sns
import matplotlib.pyplot as plt

eeg_folder = "C:/Users/danie/OneDrive/Desktop/Biomedical_engineering_PHD/Argenina_pasantia/EEG_DATA/EDF/"
hypno_folder = "C:/Users/danie/OneDrive/Desktop/Biomedical_engineering_PHD/Argenina_pasantia/EEG_DATA/Hypnograms/"

eeg_files = [file for file in os.listdir(eeg_folder)]

# Initialize an empty cumulative confusion matrix for each channel
num_classes = None
channels = []
cumulative_matrices = []

for eeg_file in eeg_files:
    eeg_path = os.path.join(eeg_folder, eeg_file)
    raw = mne.io.read_raw_edf(eeg_path, preload=True)
    raw.resample(100)
    raw.filter(0.3, 45)
    sf = raw.info['sfreq']
    chan = raw.ch_names
    raw.drop_channels(['A1-A2', 'EMG', 'EOG1', 'EOG2'])  # might show error

    # Load hypnogram data
    hypno_path = os.path.join(hypno_folder, f"{eeg_file.split('_')[0]}_ses-day1_task-sleep_sleepStages.csv")
    hypno = np.loadtxt(hypno_path, dtype=str)

    # Create a list to store confusion matrices for each channel
    channel_matrices = []

    # Iterate over EEG channels
    for ch in raw.ch_names:
        # Perform sleep staging for each channel
        sls = yasa.SleepStaging(raw, eeg_name=ch, metadata=dict(age=21, male=True))
        y_predict = sls.predict()

        # Calculate confusion matrix for this channel
        cm = confusion_matrix(hypno, y_predict)

        # Normalize confusion matrix to percentages
        cm_percentage = (cm / cm.sum(axis=1, keepdims=True) * 100.0)

        # Add the normalized confusion matrix to the list
        channel_matrices.append(cm_percentage)

        # Save channel name
        channels.append(ch)

    # Add the confusion matrices for each channel to the cumulative matrices
    if cumulative_matrices:
        for i in range(len(channel_matrices)):
            cumulative_matrices[i] += channel_matrices[i]
    else:
        cumulative_matrices = channel_matrices.copy()

# Normalize the cumulative matrices to get overall percentages
cumulative_matrices = [cm / len(eeg_files) for cm in cumulative_matrices]

# Plot the cumulative confusion matrices for each channel
for i, cumulative_matrix in enumerate(cumulative_matrices):
    plt.figure(figsize=(8, 6))
    sns.heatmap(cumulative_matrix, annot=True, fmt='.2f', cmap='Blues', cbar=False,
                xticklabels=np.unique(y_predict), yticklabels=np.unique(y_predict))

    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title(f'Cumulative Confusion Matrix (Percentages) for {channels[i]}')
    plt.show()
