import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the Excel file
ac = pd.read_excel(r'C:\Users\danie\OneDrive\Desktop\Biomedical_engineering_PHD\Argenina_pasantia\EEG_DATA\accuracy_results.xlsx',
                   sheet_name="accuracy_results")

# Convert 'Accuracy' column to numeric values
ac['Accuracy'] = pd.to_numeric(ac['Accuracy'], errors='coerce')

# Create a figure and axis
fig, ax = plt.subplots(figsize=(12, 8))

# Create a boxplot for each channel with custom styling
boxplot = ax.boxplot(ac.groupby('Channel')['Accuracy'].apply(list).values,
                     vert=True, widths=0.6, patch_artist=True)

# Adding colors to the boxplots
colors = plt.cm.viridis_r(np.linspace(0, 1, len(ac['Channel'].unique())))
for box, color in zip(boxplot['boxes'], colors):
    box.set(facecolor=color, alpha=0.7)

# Set X-axis label
ax.set_xlabel('Channel', fontsize=14)

# Set Y-axis label
ax.set_ylabel('Accuracy', fontsize=14)

# Set title
ax.set_title('Accuracy by Channel', fontsize=16)

# Set X-axis ticks and labels
ax.set_xticks(range(1, len(ac['Channel'].unique()) + 1))
ax.set_xticklabels(ac['Channel'].unique(), fontsize=12, rotation=45, ha='right')

# Add a grid for better readability
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Show the plot
plt.show()
