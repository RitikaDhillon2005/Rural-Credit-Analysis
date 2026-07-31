import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Rural Credit Analysis Dashboard", layout="wide")
st.title("Rural Credit Analysis Dashboard")

DATA_PATH = Path(__file__).resolve().parent / "data" / "agricultural_credit_data.xlsx"

if not DATA_PATH.exists():
    st.error(f"Data file not found at: {DATA_PATH}")
    st.stop()


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path)

    required_columns = {"State", "Limits_Sanctioned", "Drawals"}
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        st.error(f"Missing required columns: {sorted(missing_columns)}")
        st.stop()

    df = df.copy()

    df["Limits_Sanctioned"] = pd.to_numeric(df["Limits_Sanctioned"], errors="coerce")
    df["Drawals"] = pd.to_numeric(df["Drawals"], errors="coerce")
    
    df["Utilisation_Rate"] = (
        df["Drawals"] / df["Limits_Sanctioned"].replace(0, pd.NA)
    ) * 100
    df["Utilisation_Rate"] = df["Utilisation_Rate"].fillna(0)
    return df


df = load_data(DATA_PATH)

st.subheader("Dataset Preview")
st.dataframe(df.head(), use_container_width=True)

col1, col2, col3 = st.columns(3)
col1.metric("Total Limits Sanctioned", f"{df['Limits_Sanctioned'].sum():,.0f}")
col2.metric("Total Drawals", f"{df['Drawals'].sum():,.0f}")
col3.metric("Average Utilisation Rate", f"{df['Utilisation_Rate'].mean():.2f}%")

top_states = (
    df.groupby("State")["Limits_Sanctioned"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.subheader("Top States by Agricultural Credit")
fig, ax = plt.subplots(figsize=(10, 5))
top_states.plot(kind="bar", color="steelblue", ax=ax)
ax.set_title("Top 10 States by Total Limits Sanctioned")
ax.set_ylabel("Total Limits Sanctioned")
ax.tick_params(axis="x", labelrotation=45)
plt.tight_layout()
st.pyplot(fig)

state_utilisation = (
    df.groupby("State")["Utilisation_Rate"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

st.subheader("Average Utilisation Rate by State")
fig2, ax2 = plt.subplots(figsize=(10, 5))
state_utilisation.plot(kind="bar", color="darkorange", ax=ax2)
ax2.set_title("Top 10 States by Average Utilisation Rate")
ax2.set_ylabel("Utilisation Rate (%)")
ax2.tick_params(axis="x", labelrotation=45)
plt.tight_layout()
st.pyplot(fig2)
