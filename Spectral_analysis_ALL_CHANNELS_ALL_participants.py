
import numpy as np
import mne
import yasa
import mne
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score 
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 
import yasa 
import os
# Load data
#file_path = 'C:/Users/danie/anaconda3/envs/EEG_UBA'
# raw = mne.io.read_raw_edf("C:/Users/danie/OneDrive/Desktop/Biomedical_engineering_PHD/Argenina_pasantia/EEG_DATA/EDF/sub-291_ses-day1_task-sleep_eeg.edf", preload=True)

# raw.resample(100)
# raw.filter(0.3, 45)
# sf = raw.info['sfreq']
# raw.drop_channels(['Marca', 'A1-A2', 'EMG', 'EOG1','EOG2'])

# Directory containing the EDF files
data_folder = "C:/Users/danie/OneDrive/Desktop/Biomedical_engineering_PHD/Argenina_pasantia/EEG_DATA/EDF/"

# Get a list of all files in the directory
all_files = os.listdir(data_folder)

# Filter files to keep only those with the ".edf" extension - just in case 
edf_files = [file for file in all_files if file.endswith(".edf")]

# Loop over each EDF file
for file_name in edf_files:
    file_path = os.path.join(data_folder, file_name)

    # Read raw EEG data
    raw = mne.io.read_raw_edf(file_path, preload=True)

    # Preprocessing steps
    raw.resample(100)
    raw.filter(0.3, 45)
    sf = raw.info['sfreq']
    raw.drop_channels(['A1-A2', 'EMG', 'EOG1', 'EOG2'])
hypno_files = [file for file in all_files if file.endswith("_sleepStages.csv")]
    # Additional processing or saving can be done here

    # Example: Save preprocessed data
    # raw.save('path_to_save_preprocessed_data.fif', overwrite=True)





chan = raw.ch_names

#sacar: marca / A1-A2 / EMG / both EOG 

data = raw.get_data(units="uV")

# hypno = pd.read_csv(r"C:\Users\danie\OneDrive\Desktop\Biomedical_engineering_PHD\Argenina_pasantia\EEG_DATA\Hypnograms\sub-291_ses-day1_task-sleep_sleepStages.csv")
# hypno = np.array(hypno)
# hypno = np.array(hypno).flatten()
# hypno = yasa.hypno_str_to_int(hypno)


# Directory containing the hypnogram CSV files
hypno_folder = "C:/Users/danie/OneDrive/Desktop/Biomedical_engineering_PHD/Argenina_pasantia/EEG_DATA/Hypnograms/"

# Get a list of all files in the directory
all_files = os.listdir(hypno_folder)

# Filter files to keep only those with the "_sleepStages.csv" extension
hypno_files = [file for file in all_files if file.endswith("_sleepStages.csv")]

# Loop over each hypnogram file
for hypno_file in hypno_files:
    hypno_path = os.path.join(hypno_folder, hypno_file)

    # Read hypnogram data using Pandas
    hypno = pd.read_csv(hypno_path)
    
    print(f"\nFirst few rows of hypnogram from {hypno_file}:\n")
    print(hypno.head())
    
    # Assuming 'sleep_stage' is the column containing sleep stage information
    #hypno = np.array(hypno['sleep_stage'])
    
    # Flatten the array if needed
    hypno =np.array(hypno).flatten()
    
    # Convert sleep stage labels from string to integer using yasa.hypno_str_to_int
    hypno = yasa.hypno_str_to_int(hypno)

    # Additional processing or saving can be done here
    # For example, save the processed hypnogram data if needed
    #np.save('path_to_save_processed_hypno.npy', hypno)
    print(f"Hypnogram from {hypno_file} has been successfully read and processed.")






sls = yasa.SleepStaging(raw, eeg_name='FC2')
hypno_pred = sls.predict()
hypno_pred = yasa.hypno_str_to_int(hypno_pred)


# plt.figure(figsize=(14, 5))
# yasa.plot_hypnogram(hypno_pred);  

# plt.figure(figsize=(14, 5))  
# yasa.plot_hypnogram(hypno)

# Create a single figure with two subplots
fig, axes = plt.subplots(nrows=2, figsize=(12, 8))

# Plot the first hypnogram
axes[0].set_title('Hypnogram - Prediction')
yasa.plot_hypnogram(hypno_pred, ax=axes[0])

# Plot the second hypnogram
axes[1].set_title('Hypnogram - Actual')
yasa.plot_hypnogram(hypno, ax=axes[1])

# Adjust layout to prevent overlapping
plt.tight_layout()

# Show the combined plot
plt.show()

hypno_up = yasa.hypno_upsample_to_data(hypno, sf_hypno=1/30, data=raw)

yasa.plot_spectrogram(data[chan.index("FC2")], sf, hypno_up);


print(f"The accuracy is {100 * accuracy_score(hypno, hypno_pred):.2f}%")

accuracy_scores = []

# Iterate through each channel
for channel in chan:
    # Plot spectrogram for each channel
    yasa.plot_spectrogram(data[chan.index(channel)], sf, hypno_up)
    plt.title(f"Spectrogram - {channel}")
    plt.show()
    
    #accuracy score for each channel
    # Calculate accuracy score for each channel
    hypno_pred_channel = yasa.SleepStaging(raw, eeg_name=channel).predict()
    accuracy = accuracy_score(hypno, yasa.hypno_str_to_int(hypno_pred_channel))
    accuracy_scores.append(accuracy)

    print(f"The accuracy for channel {channel} is {100 * accuracy:.2f}%")
    
#make a table with suject and channel 

#make a loop that shows the names of each one and check it is looking in the right place
#add predicted spectrogram
print(f"\nThe average accuracy across all channels is {100 * np.mean(accuracy_scores):.2f}%")



