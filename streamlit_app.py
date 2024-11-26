

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from datetime import datetime, timedelta
import random
import math
import numpy as np

# Configure Streamlit page
st.set_page_config(page_title="Customer Behavior Tracking", layout="wide")

# Define main sections
st.title("Customer Behavior Tracking")

# Sidebar for simulation input
st.sidebar.header("Simulation Settings")
steps = st.sidebar.number_input("Number of Simulation Steps:", min_value=1, max_value=1000, value=100, step=10)

# Function to simulate customer behavior data
def simulate_data(steps):
    # Create a timestamp column that starts from the current time and increments by 1 minute
    start_time = datetime.now()
    timestamps = [start_time + timedelta(minutes=i) for i in range(steps)]
   
    # Simulate customer behavior data
    browsing_time = [random.uniform(0, 15) for _ in range(steps)]  # Browsing time in minutes
    purchases = [random.randint(0, 5) for _ in range(steps)]  # Number of purchases
    returning_customers = [random.choice([0, 1]) for _ in range(steps)]  # 0 = new customer, 1 = returning customer
   
    # Create a DataFrame
    data = pd.DataFrame({
        "timestamp": timestamps,
        "browsing_time": browsing_time,
        "purchases": purchases,
        "returning_customers": returning_customers
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
    ax.plot(data["timestamp"], data["browsing_time"], label="Browsing Time (minutes)", color='blue')
    ax.plot(data["timestamp"], data["purchases"], label="Purchases (count)", color='orange')
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Customer Behavior Data")
    ax.legend()
    st.pyplot(fig)

    # Returning customers purchases
    st.markdown("### Purchases by Returning Customers")
    returning_data = data[data["returning_customers"] == 1]
    if not returning_data.empty:
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.plot(returning_data["timestamp"], returning_data["purchases"], label="Purchases (returning customers)", color='red')
        ax.set_xlabel("Timestamp")
        ax.set_ylabel("Number of Purchases")
        ax.legend()
        st.pyplot(fig)
    else:
        st.write("No returning customers during the simulation.")
else:
    st.write("Set simulation parameters in the sidebar and click 'Run Simulation' to begin.")
