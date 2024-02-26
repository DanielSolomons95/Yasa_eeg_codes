import os
import shutil

# Source directory
source_directory = r'C:\Users\danie\OneDrive\Desktop\Biomedical_engineering_PHD\Argenina_pasantia\EEG_DATA'

# Destination directory
destination_directory = os.path.join(source_directory, 'Hypnograms')

# Walk through the source directory
for root, dirs, files in os.walk(source_directory):
    for file in files:
        # Check if the file ends with "sleepStages.csv"
        if file.endswith("sleepStages.csv"):
            # Build the full path of the source file
            source_file_path = os.path.join(root, file)
            
            # Build the full path of the destination file
            destination_file_path = os.path.join(destination_directory, file)
            
            # Move the file to the destination directory
            shutil.move(source_file_path, destination_file_path)
            print(f"Moved {file} to {destination_directory}")

print("Files moved successfully!")
