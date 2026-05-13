import pandas as pd

df = pd.read_excel(
    r"C://Users//DELL//Desktop//rits//Rural-Credit-Analysis//data//credit.xlsx"
)

print(df.head())
# Show column names
print(df.columns)

# Dataset information
print(df.info())

# Check missing values
print(df.isnull().sum())
df["Utilisation_Rate"] = (
    df["Drawals"] / df["Limits_Sanctioned"]
) * 100

print(df.head())
import matplotlib.pyplot as plt

# Top states by sanctioned credit
top_states = (
    df.groupby("State")["Limits_Sanctioned"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)




top_states.plot(kind="bar")

plt.title("Top States by Agricultural Credit")

plt.savefig("image/top_states_credit.png")

plt.show()