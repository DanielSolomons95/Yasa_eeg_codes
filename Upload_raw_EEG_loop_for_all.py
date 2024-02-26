import mne
import os

source_directory = r'C:\Users\danie\OneDrive\Desktop\Biomedical_engineering_PHD\Argenina_pasantia\EEG_DATA\EDF'

if not os.path.exists(source_directory):
    print(f"Source directory '{source_directory}' does not exist.")
else:
    for file in os.listdir(source_directory):
        file_path = os.path.join(source_directory, file)
        if file.endswith('.edf'):
            raw = mne.io.read_raw_edf(file_path, preload=True)
            print(f"Read '{file}' into MNE-Python.")


