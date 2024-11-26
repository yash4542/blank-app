import random
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from PIL import Image
import streamlit as st

# Set Streamlit page configuration
st.set_page_config(page_title="Sensor Simulation and Analysis", layout="wide")

# Constants for simulation
WIDTH = 100  # Width of the grid for heatmap visualization
HEIGHT = 100  # Height of the grid for heatmap visualization

# Sidebar for user input
st.sidebar.header("Simulation Settings")
steps = st.sidebar.number_input("Number of Simulation Steps:", min_value=1, max_value=1000, value=100, step=10)

# Define main classes and functions for simulation

class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Gyroscope:
    def get_rotation(self):
        return random.uniform(0, 360)

class Camera:
    def count_foot_traffic(self):
        return random.randint(0, 15)

class RFID:
    def detect_item_pickup(self):
        return random.choice([True, False])

class MotionDetector:
    def detect_movement(self):
        return random.choice([True, False])

class HeatMap:
    def __init__(self, width, height):
        self.data = [[0 for _ in range(width)] for _ in range(height)]

    def add_data(self, x, y):
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            self.data[y][x] += 1

    def intensity_to_color(self, intensity):
        scaled = min(255, intensity * 20)
        return scaled, max(0, 255 - scaled), 255 - scaled

    def save_to_image(self):
        img = Image.new('RGB', (WIDTH, HEIGHT))
        for y in range(HEIGHT):
            for x in range(WIDTH):
                r, g, b = self.intensity_to_color(self.data[y][x])
                img.putpixel((x, y), (r, g, b))
        return img

# Simulate data collection over multiple steps
def simulate_data(steps):
    gyroscope = Gyroscope()
    camera = Camera()
    rfid = RFID()
    motion_detector = MotionDetector()

    data = {
        "timestamp": [],
        "rotation": [],
        "foot_traffic": [],
        "item_picked_up": [],
        "movement_detected": []
    }

    start_time = datetime.now()
    heatmap = HeatMap(WIDTH, HEIGHT)

    for step in range(steps):
        timestamp = start_time + timedelta(seconds=step)
        rotation = gyroscope.get_rotation()
        foot_traffic = camera.count_foot_traffic()
        item_picked_up = rfid.detect_item_pickup()
        movement_detected = motion_detector.detect_movement()

        # Add random coordinates to heatmap to simulate foot traffic
        x, y = random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)
        heatmap.add_data(x, y)

        data["timestamp"].append(timestamp)
        data["rotation"].append(rotation)
        data["foot_traffic"].append(foot_traffic)
        data["item_picked_up"].append(item_picked_up)
        data["movement_detected"].append(movement_detected)

    df = pd.DataFrame(data)
    return df, heatmap.save_to_image()

# Perform exploratory data analysis on collected data
def perform_eda(df):
    st.subheader("Exploratory Data Analysis")
    st.write("### Data Summary")
    st.write(df.describe())
    
    st.write("### Data Distribution")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    fig, ax = plt.subplots(figsize=(12, 8))
    df[numeric_cols].hist(ax=ax, bins=20, grid=False, color=['skyblue', 'lightcoral'])
    plt.suptitle("Histograms of Numeric Columns")
    st.pyplot(fig)

    df["item_picked_up"] = df["item_picked_up"].astype(int)
    df["movement_detected"] = df["movement_detected"].astype(int)

    st.write("### Correlation Heatmap")
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(df.corr(), annot=True, cmap="coolwarm", vmin=-1, vmax=1)
    st.pyplot(fig)

    st.write("### Time Series of Rotation and Foot Traffic")
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(df["timestamp"], df["rotation"], label="Rotation (degrees)", color='blue')
    ax.plot(df["timestamp"], df["foot_traffic"], label="Foot Traffic (count)", color='orange')
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Sensor Data")
    ax.legend()
    st.pyplot(fig)

    st.write("### Foot Traffic When Movement is Detected")
    movement_data = df[df["movement_detected"] == 1]
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(movement_data["timestamp"], movement_data["foot_traffic"], label="Foot Traffic (movement detected)", color='red')
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Foot Traffic Count")
    ax.legend()
    st.pyplot(fig)

# Execute simulation and analysis
if st.sidebar.button("Run Simulation"):
    st.write(f"Running simulation for {steps} steps...")
    df, heatmap_image = simulate_data(steps)
    st.success("Simulation completed!")

    st.subheader("Simulated Data")
    st.dataframe(df)

    st.subheader("Heatmap of Foot Traffic")
    st.image(heatmap_image, caption="Foot Traffic Heatmap")

    perform_eda(df)
else:
    st.write("Set simulation parameters in the sidebar and click 'Run Simulation' to begin.")
