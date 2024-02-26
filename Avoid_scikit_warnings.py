import warnings
from sklearn.exceptions import UndefinedMetricWarning

# Filter out UndefinedMetricWarning
warnings.filterwarnings("ignore", category=UndefinedMetricWarning)

# Your code goes here

# Reset warnings to default behavior
warnings.filterwarnings("default", category=UndefinedMetricWarning)


import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

# Your code goes here

# Reset warnings to default behavior
warnings.filterwarnings("default")
