import scipy.io
import csv
import os

# Directory containing MATLAB files
matlab_files_directory = 'C:/Users/danie/OneDrive/Desktop/Biomedical_engineering_PHD/Argenina_pasantia/EEG_DATA/'

# Define a mapping dictionary
stage_mapping = {0: 'W', 1: 'N1', 2: 'N2', 3: 'N3', 4: 'N3', 5: 'R', 6: 'W', 7: 'W'}

# Iterate through directories and subdirectories using os.walk
for root, dirs, files in os.walk(matlab_files_directory):
    for filename in files:
        if filename.endswith('.mat'):
            # Load MATLAB file
            mat_data = scipy.io.loadmat(os.path.join(root, filename))
            
            # Extract the raw sleep stages data
            raw_sleep_stages = mat_data['stageData']['stages'][0, 0]
            
            # Specify the CSV file name based on the MATLAB file name
            csv_file_name = os.path.splitext(filename)[0] + '.csv'

            # Write data to CSV file with stage mapping
            with open(os.path.join(root, csv_file_name), 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)

                # Write header if applicable
                # csvwriter.writerow(['ColumnName'])

                # Write data rows with mapping
                for row in raw_sleep_stages:
                    mapped_row = [stage_mapping[value] for value in row]
                    csvwriter.writerow(mapped_row)
