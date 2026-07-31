import pandas as pd
from pathlib import Path

# Get the project directory
BASE_DIR = Path(__file__).resolve().parent

# Path to the dataset
file_path = BASE_DIR / "data" / "agricultural_credit_data.xlsx"

# Read the dataset
df = pd.read_excel(file_path)

# Display first 5 rows
print(df.head())