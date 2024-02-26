import numpy as np
import mne
import yasa
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score 
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 
import yasa 

# Load data
#file_path = 'C:/Users/danie/anaconda3/envs/EEG_UBA'
raw = mne.io.read_raw_edf("C:/Users/danie/OneDrive/Desktop/Biomedical_engineering_PHD/Argenina_pasantia/EEG_DATA/EDF/sub-217_ses-day1_task-sleep_eeg.edf", preload=True)

raw.resample(100)
raw.filter(0.3, 45)
sf = raw.info['sfreq']
chan = raw.ch_names


data = raw.get_data(units="uV")

hypno = pd.read_csv(r"C:\Users\danie\OneDrive\Desktop\Biomedical_engineering_PHD\Argenina_pasantia\EEG_DATA\Hypnograms\sub-217_ses-day1_task-sleep_sleepStages.csv")
hypno = np.array(hypno)
hypno = np.array(hypno).flatten()
hypno = yasa.hypno_str_to_int(hypno)






sls = yasa.SleepStaging(raw, eeg_name='Fz')
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




