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
from simulation_code import simulate_data  # Replace with actual filename

# Configure Streamlit page
st.set_page_config(page_title="Sensor Simulation", layout="wide")

# Define main sections
st.title("Sensor Simulation and Analysis")

# Sidebar for simulation input
st.sidebar.header("Simulation Settings")
steps = st.sidebar.number_input("Number of Simulation Steps:", min_value=1, max_value=1000, value=100, step=10)

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
