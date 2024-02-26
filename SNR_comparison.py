import mne
import numpy as np
import matplotlib.pyplot as plt

# Replace 'raw_edf' and 'raw_bdf' with your loaded EEG data
raw_edf = mne.io.read_raw_edf(r"C:\Users\danie\OneDrive\Desktop\Biomedical_engineering_PHD\Argenina_pasantia\EEG_DATA\Sample_AGUS\sub-200_ses-day1_task-adaptB_eeg.edf", preload=True)
raw_bdf = mne.io.read_raw_bdf(r"C:\Users\danie\OneDrive\Desktop\Biomedical_engineering_PHD\Argenina_pasantia\EEG_DATA\Pruebas_Bruno_Bioamp_281223\OpenBCI-BDF-2023-12-28_14-51-02.bdf", preload=True)

# Define frequency range for SNR calculation
freq_range = (1, 40)  # Adjust based on your data characteristics

# Function to calculate SNR from raw data
def calculate_snr(raw):
    freqs, psd = plt.psd(raw.get_data()[0], NFFT=raw.n_times, Fs=raw.info['sfreq'])
    freq_idx = np.where((freqs >= freq_range[0]) & (freqs <= freq_range[1]))[0]
    signal_power = np.mean(psd[freq_idx])
    noise_power = np.mean(psd[len(freqs)//2:])  # Assuming noise is present in higher frequencies
    snr = 10 * np.log10(signal_power / noise_power)
    return snr

# Calculate SNR for EDF and BDF
snr_edf = calculate_snr(raw_edf)
snr_bdf = calculate_snr(raw_bdf)

print(f"SNR (EDF): {snr_edf:.2f} dB")
print(f"SNR (BDF): {snr_bdf:.2f} dB")
