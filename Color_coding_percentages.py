import pandas as pd

# Read the CSV file
ac = pd.read_csv(
    r"C:\Users\danie\OneDrive\Desktop\Biomedical_engineering_PHD\Argenina_pasantia\EEG_DATA\accuracy_results.csv",
    index_col=None,
    na_values=['NA']
)

# Define a function for cell highlighting
def highlight_red_or_green(val):
    color = "red" if val < 70 else "green"
    return f"background-color: {color}"

# Apply the cell highlighting function to the third column (index 2)
styled_ac = ac.style.applymap(highlight_red_or_green, subset=pd.IndexSlice[:, [2]])

# Display the styled DataFrame
styled_ac
