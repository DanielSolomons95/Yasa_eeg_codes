import shutil
import os

source_directory = r'G:\.shortcut-targets-by-id\1InqcJ3MoOoUrrF0m_shwa3f2Mvy-oeJq\copia_daniel_CNTR_VMA_NOCHE-BIDS'
destination_directory = r'C:\Users\danie\OneDrive\Desktop\Biomedical_engineering_PHD\Argenina_pasantia\EEG_DATA\EDF'
file_suffix = 'task-sleep_eeg.edf'
# Use os.walk to traverse through the source directory and its subdirectories
for root, dirs, files in os.walk(source_directory):
    for file in files:
        if file.endswith(file_suffix):
            source_path = os.path.join(root, file)
            destination_path = os.path.join(destination_directory, file)
            shutil.move(source_path, destination_path)
            print(f"Moved '{file}' to '{destination_directory}'")














#JUST IN CASE

# import shutil
# import os

# source_directory = r'G:\.shortcut-targets-by-id\1InqcJ3MoOoUrrF0m_shwa3f2Mvy-oeJq\copia_daniel_CNTR_VMA_NOCHE-BIDS'
# destination_directory = r'C:\Users\danie\OneDrive\Desktop\Biomedical_engineering_PHD\Argenina_pasantia\EEG_DATA\EDF'
# file_suffix = 'task-sleep_eeg.edf'

# # Check if source directory exists
# if not os.path.exists(source_directory):
#     print(f"Source directory '{source_directory}' does not exist.")
# else:
#     # Check if destination directory exists, create if not
#     if not os.path.exists(destination_directory):
#         os.makedirs(destination_directory)

#     # Use os.walk to traverse through the source directory and its subdirectories
#     for root, dirs, files in os.walk(source_directory):
#         for file in files:
#             if file.endswith(file_suffix):
#                 source_path = os.path.join(root, file)
#                 destination_path = os.path.join(destination_directory, file)
#                 shutil.move(source_path, destination_path)
#                 print(f"Moved '{file}' to '{destination_directory}'")
