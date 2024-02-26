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

    # Perform sleep staging
    sls = yasa.SleepStaging(raw, eeg_name='FC2', metadata=dict(age=21, male=True))
    y_predict = sls.predict()

    # Calculate confusion matrix
    cm = confusion_matrix(hypno, y_predict)

    # Plot confusion matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, xticklabels=np.unique(y_predict), 
                yticklabels=np.unique(y_predict))

    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title(f'Confusion matrix for {eeg_file}')
    plt.show()

    # You can add more code here for additional analysis or save the confusion matrix if needed
