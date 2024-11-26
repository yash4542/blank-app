import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from datetime import datetime, timedelta
import random
import math
import numpy as np

# Import your simulation functions and classes
# Removed the import for simulation_code as it is now embedded in this script

# Configure Streamlit page
st.set_page_config(page_title="CBT", layout="wide")

# Define main sections
st.title("CUSTOMER BEHAVIOUR TRACKING")

# Sidebar for simulation input
st.sidebar.header("Simulation Settings")
steps = st.sidebar.number_input("Number of Simulation Steps:", min_value=1, max_value=1000, value=100, step=10)

# Function to simulate sensor data
def simulate_data(steps):
    # Create a timestamp column that starts from the current time and increments by 1 minute
    start_time = datetime.now()
    timestamps = [start_time + timedelta(minutes=i) for i in range(steps)]
   
    # Simulate sensor data (random data for the example)
    rotation = [random.uniform(0, 360) for _ in range(steps)]  # Rotation in degrees
    foot_traffic = [random.randint(0, 100) for _ in range(steps)]  # Foot traffic count
    movement_detected = [random.choice([0, 1]) for _ in range(steps)]  # 0 = no movement, 1 = movement detected
   
    # Create a DataFrame
    data = pd.DataFrame({
        "timestamp": timestamps,
        "rotation": rotation,
        "foot_traffic": foot_traffic,
        "movement_detected": movement_detected
    })
   
    return data

# Run simulation when button is clicked
if st.sidebar.button("Run Simulation"):
    st.write(f"Running simulation for {steps} steps...")
    data = simulate_data(steps)  # Run the simulation
    st.success("Simulation completed!")

    # Display raw data
    st.subheader("Simulated Data")
    st.dataframe(data)

    # Exploratory Data Analysis (EDA)
    st.subheader("Exploratory Data Analysis")

    # Data summary
    st.markdown("### Data Summary")
    st.write(data.describe())

    # Histograms of numeric columns
    st.markdown("### Data Distribution")
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    fig, ax = plt.subplots(figsize=(12, 6))
    data[numeric_cols].hist(ax=ax, bins=20, grid=False)
    st.pyplot(fig)

    # Correlation heatmap
    st.markdown("### Correlation Heatmap")
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(data.corr(), annot=True, cmap="coolwarm", vmin=-1, vmax=1, ax=ax)
    st.pyplot(fig)

    # Time series plots
    st.markdown("### Time Series Analysis")
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(data["timestamp"], data["rotation"], label="Rotation (degrees)", color='blue')
    ax.plot(data["timestamp"], data["foot_traffic"], label="Foot Traffic (count)", color='orange')
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Sensor Data")
    ax.legend()
    st.pyplot(fig)

    # Movement detected foot traffic
    st.markdown("### Foot Traffic During Movement")
    movement_data = data[data["movement_detected"] == 1]
    if not movement_data.empty:
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.plot(movement_data["timestamp"], movement_data["foot_traffic"], label="Foot Traffic (movement detected)", color='red')
        ax.set_xlabel("Timestamp")
        ax.set_ylabel("Foot Traffic Count")
        ax.legend()
        st.pyplot(fig)
    else:
        st.write("No movement detected during the simulation.")
else:
    st.write("Set simulation parameters in the sidebar and click 'Run Simulation' to begin.")
