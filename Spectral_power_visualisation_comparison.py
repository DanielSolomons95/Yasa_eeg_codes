
import mne
import numpy as np
import matplotlib.pyplot as plt

def calculate_snr(raw):
    # Calculate SNR as the ratio of signal power to noise power
    data, _ = raw[:, :]
    signal_power = np.mean(np.var(data, axis=1))
    noise_power = np.mean(raw.info['chs'][0]['loc'][3] ** 2)  # Assuming noise level from electrode info
    snr = 10 * np.log10(signal_power / noise_power)
    return snr

def plot_psd(raw, title):
    raw.plot_psd(fmax=100, show=False)
    plt.title(title)
    plt.ylim(-50,50) #more detailed look
    plt.show()

# Replace 'your_edf_file.edf' and 'your_bdf_file.bdf' with the actual filenames
edf_file_path = r"C:\Users\danie\OneDrive\Desktop\Biomedical_engineering_PHD\Argenina_pasantia\EEG_DATA\Pruebas_Agus_12_01\pruebasControladas_BioAmp_Agus_120124\OpenBCI-BDF-2024-01-12_16-38-45.bdf"
#bdf_file_path = r"C:\Users\danie\OneDrive\Desktop\Biomedical_engineering_PHD\Argenina_pasantia\EEG_DATA\Pruebas_Bruno_Bioamp_281223\OpenBCI-BDF-2023-12-28_14-51-02.bdf"


# Load EEG data from EDF file
raw_edf = mne.io.read_raw(edf_file_path, preload=True)
raw_edf.filter(l_freq=1, h_freq=40)
#raw_edf.resample(100)

# Load EEG data from BDF file
#raw_bdf = mne.io.read_raw(bdf_file_path, preload=True)
# raw_bdf.filter(l_freq=1, h_freq=40)
# raw_bdf.resample(100)

# Calculate and compare SNR
snr_edf = calculate_snr(raw_edf)
# snr_bdf = calculate_snr(raw_bdf)
print(f'SNR for EDF: {snr_edf:.2f}')
# print(f'SNR for BDF: {snr_bdf:.2f}')

# Plot and compare PSD
plot_psd(raw_edf, 'Prueba equipo 1 Agus enero')
# plot_psd(raw_bdf, 'Bruno December 2023')

# Perform additional analyses as needed

# Show the plots
plt.show()
