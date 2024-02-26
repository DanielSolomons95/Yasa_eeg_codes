import mne
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

def calculate_cross_correlation(raw1, raw2):
    # Plot PSD for raw1
    raw1.plot_psd(fmax=50, show=False)
    psd1, freqs1 = plt.psd(raw1.get_data()[0], NFFT=raw1.n_times, Fs=raw1.info['sfreq'])
    plt.close()

    # Plot PSD for raw2
    raw2.plot_psd(fmax=50, show=False)
    psd2, freqs2 = plt.psd(raw2.get_data()[0], NFFT=raw2.n_times, Fs=raw2.info['sfreq'])
    plt.close()

    # Extract power values at specific frequencies
    freqs = np.array([1, 5, 10, 15, 20, 25, 30, 35, 40])

    # Find the indices corresponding to the specified frequencies
    indices1 = np.searchsorted(freqs1, freqs)
    indices2 = np.searchsorted(freqs2, freqs)

    # Extract power values at specific frequencies using the found indices
    psd1_values = [psd1[idx] for idx in indices1]
    psd2_values = [psd2[idx] for idx in indices2]

    # Calculate Pearson correlation coefficient
    correlation_coefficient, _ = pearsonr(psd1_values, psd2_values)

    return correlation_coefficient

edf_file_path = r"C:\Users\danie\OneDrive\Desktop\Biomedical_engineering_PHD\Argenina_pasantia\EEG_DATA\Sample_AGUS\sub-200_ses-day1_task-adaptB_eeg.edf"
bdf_file_path = r"C:\Users\danie\OneDrive\Desktop\Biomedical_engineering_PHD\Argenina_pasantia\EEG_DATA\Pruebas_Bruno_Bioamp_281223\OpenBCI-BDF-2023-12-28_14-51-02.bdf"




# Load EEG data from EDF file
raw_edf = mne.io.read_raw(edf_file_path, preload=True)
raw_edf.filter(l_freq=1, h_freq=40)
raw_edf.resample(100)

# Load EEG data from BDF file
raw_bdf = mne.io.read_raw(bdf_file_path, preload=True)
raw_bdf.filter(l_freq=1, h_freq=40)
raw_bdf.resample(100)

# Calculate cross-correlation coefficient
correlation_coefficient = calculate_cross_correlation(raw_edf, raw_bdf)

# Print the correlation coefficient
print(f'Cross-Correlation Coefficient: {correlation_coefficient:.4f}')
