import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use("dark_background")

st.set_page_config(
    page_title="Solar Radiation Analysis",
    page_icon=":bar_chart:",
    layout="wide"
)

st.title(" Solar Radiation Single File Analysis")

# File uploader
uploaded_file = st.file_uploader("Upload solar data CSV", type=["csv"])

@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    return df

if uploaded_file is not None:
    df = load_data(uploaded_file)

    # Select metric
    metric = st.sidebar.radio("Select Metric", ["GHI", "DHI", "DNI"])

    # Summary stats
    st.subheader(f" Summary Statistics for {metric}")
    st.write(df[metric].describe())

    # Boxplot
    st.subheader(f"📊 {metric} Distribution")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.boxplot(x=df[metric], ax=ax, color='skyblue')
    ax.set_title(f"{metric} Boxplot")
    st.pyplot(fig)

    # Time series
    df = df[df["Timestamp"] != "yyyy-mm-dd hh:mm"]
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors='coerce')
    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        st.subheader(f" {metric} Over Time")
        st.line_chart(df.set_index("Timestamp")[metric])

else:
    st.info("Please upload a CSV file to begin.")
