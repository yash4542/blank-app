import random
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from PIL import Image
import streamlit as st

# Constants for simulation
WIDTH = 100  # Width of the grid for heatmap visualization
HEIGHT = 100  # Height of the grid for heatmap visualization
SIMULATION_STEPS = 100  # Number of time steps to simulate data

# Class to represent a coordinate (x, y) in 2D space
class Coordinates:
    def __init__(self, x, y):
        self.x = x  # X-coordinate
        self.y = y  # Y-coordinate

# Class to simulate a gyroscope sensor
class Gyroscope:
    def get_rotation(self):
        return random.uniform(0, 360)  # Random rotation angle

# Class to simulate a camera for counting foot traffic
class Camera:
    def count_foot_traffic(self):
        return random.randint(0, 15)  # Random count of people

# Class to simulate an RFID sensor for detecting item pickup
class RFID:
    def detect_item_pickup(self):
        return random.choice([True, False])  # Random Boolean

# Class to simulate a motion detector
class MotionDetector:
    def detect_movement(self):
        return random.choice([True, False])  # Random Boolean

# Class to create and manage a heatmap for visualizing activity
class HeatMap:
    def __init__(self, width, height):
        self.data = [[0 for _ in range(width)] for _ in range(height)]

    def add_data(self, x, y):
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            self.data[y][x] += 1

    def intensity_to_color(self, intensity):
        scaled = min(255, intensity * 20)
        r = scaled
        g = max(0, 255 - scaled)
        b = 255 - scaled
        return r, g, b

    def save_to_ppm(self, filename):
        img = Image.new('RGB', (WIDTH, HEIGHT))
        for y in range(HEIGHT):
            for x in range(WIDTH):
                r, g, b = self.intensity_to_color(self.data[y][x])
                img.putpixel((x, y), (r, g, b))
        img.save(filename)

# Class to simulate a sensor for indoor positioning
class Sensor:
    def __init__(self, x, y, range_):
        self.position = Coordinates(x, y)
        self.range = range_

    def get_rssi(self, customer_position):
        distance = math.sqrt(
            (customer_position.x - self.position.x) ** 2 +
            (customer_position.y - self.position.y) ** 2
        )
        if distance > self.range:
            return -100  # Signal strength too weak beyond range
        else:
            return -10 * math.log10(distance / self.range)

# Function to simulate data collection over multiple steps
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

    for step in range(steps):
        timestamp = start_time + timedelta(seconds=step)

        rotation = gyroscope.get_rotation()
        foot_traffic = camera.count_foot_traffic()
        item_picked_up = rfid.detect_item_pickup()
        movement_detected = motion_detector.detect_movement()

        data["timestamp"].append(timestamp)
        data["rotation"].append(rotation)
        data["foot_traffic"].append(foot_traffic)
        data["item_picked_up"].append(item_picked_up)
        data["movement_detected"].append(movement_detected)

    return pd.DataFrame(data)

# Function to perform exploratory data analysis on collected data
def perform_eda(df):
    st.subheader("Exploratory Data Analysis")
    st.write("### Data Summary")
    st.write(df.describe())
    
    st.write("### Data Distribution")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    fig, axes = plt.subplots(len(numeric_cols), 1, figsize=(10, 5 * len(numeric_cols)))
    colors = ['skyblue', 'lightcoral', 'lightgreen', 'lightgrey']

    if len(numeric_cols) == 1:
        axes = [axes]  # Convert axes to list if only one numeric column
    
    for i, col in enumerate(numeric_cols):
        axes[i].hist(df[col].dropna(), bins=20, color=colors[i % len(colors)], edgecolor='black')
        axes[i].set_title(f"Histogram of {col}")
        axes[i].set_xlabel(col)
        axes[i].set_ylabel("Frequency")
    
    plt.tight_layout()
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

# Streamlit app configuration
st.set_page_config(page_title="Sensor Simulation", layout="wide")
st.title("Sensor Simulation and Analysis")

# Sidebar for simulation input
st.sidebar.header("Simulation Settings")
steps = st.sidebar.number_input("Number of Simulation Steps:", min_value=1, max_value=1000, value=100, step=10)

# Run simulation when button is clicked
if st.sidebar.button("Run Simulation"):
    st.write(f"Running simulation for {steps} steps...")
    data = simulate_data(steps)
    st.success("Simulation completed!")

    st.subheader("Simulated Data")
    st.dataframe(data)

    perform_eda(data)  # Perform EDA on simulated data
else:
    st.write("Set simulation parameters in the sidebar and click 'Run Simulation' to begin.")
