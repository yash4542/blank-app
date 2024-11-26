import random
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from PIL import Image

# Constants for simulation
WIDTH = 100  # Width of the grid for heatmap visualization
HEIGHT = 100  # Height of the grid for heatmap visualization
SIMULATION_STEPS = 100  # Number of time steps to simulate data

# Class to represent a coordinate (x, y) in 2D space
class Coordinates:
    def __init__(self, x, y):
        self.x = x  # X-coordinate
        self.y = y  # Y-coordinate

    def __repr__(self):
        # Provide a clear string representation for debugging
        return f"Coordinates(x={self.x}, y={self.y})"

# Class to simulate a gyroscope sensor
class Gyroscope:
    def get_rotation(self):
        """
        Simulate the detection of rotation by generating a random value
        between 0 and 360 degrees.
        """
        rotation = random.uniform(0, 360)  # Random rotation angle
        print(f"[Gyroscope] Rotation detected: {rotation:.2f} degrees")
        return rotation

    def __repr__(self):
        return "Gyroscope()"

# Class to simulate a camera for counting foot traffic
class Camera:
    def count_foot_traffic(self):
        """
        Simulate the detection of foot traffic by generating a random
        number of people (between 0 and 15).
        """
        people_count = random.randint(0, 15)  # Random count of people
        print(f"[Camera] Detected {people_count} people.")
        return people_count

    def __repr__(self):
        return "Camera()"

# Class to simulate an RFID sensor for detecting item pickup
class RFID:
    def detect_item_pickup(self):
        """
        Simulate item pickup detection. Randomly decide if an item was
        picked up (True) or not (False).
        """
        item_picked = random.choice([True, False])  # Random Boolean
        if item_picked:
            print("[RFID] Item pickup detected!")
        else:
            print("[RFID] No item pickup detected.")
        return item_picked

    def __repr__(self):
        return "RFID()"

# Class to simulate a motion detector
class MotionDetector:
    def detect_movement(self):
        """
        Simulate motion detection. Randomly decide if movement was
        detected (True) or not (False).
        """
        movement = random.choice([True, False])  # Random Boolean
        if movement:
            print("[Motion Detector] Movement detected!")
        else:
            print("[Motion Detector] No movement detected.")
        return movement

    def __repr__(self):
        return "MotionDetector()"

# Class to create and manage a heatmap for visualizing activity
class HeatMap:
    def __init__(self, width, height):
        """
        Initialize the heatmap with a grid of specified dimensions,
        all set to zero.
        """
        self.data = [[0 for _ in range(width)] for _ in range(height)]

    def add_data(self, x, y):
        """
        Increment the intensity at a specific grid location (x, y).
        """
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            self.data[y][x] += 1

    def intensity_to_color(self, intensity):
        """
        Map an intensity value to an RGB color for visualization.
        The scaling ensures the color intensity corresponds to the
        activity level.
        """
        scaled = min(255, intensity * 20)  # Scale the intensity
        r = scaled  # Red component increases with intensity
        g = max(0, 255 - scaled)  # Green decreases as intensity increases
        b = 255 - scaled  # Blue decreases as intensity increases
        return r, g, b

    def save_to_ppm(self, filename):
        """
        Save the heatmap data as a .ppm image file for visualization.
        """
        img = Image.new('RGB', (WIDTH, HEIGHT))  # Create a blank image
        for y in range(HEIGHT):
            for x in range(WIDTH):
                r, g, b = self.intensity_to_color(self.data[y][x])
                img.putpixel((x, y), (r, g, b))  # Assign color to pixel
        img.save(filename)
        print(f"[HeatMap] Heat map saved as {filename}")

    def __repr__(self):
        return f"HeatMap(width={WIDTH}, height={HEIGHT})"

# Class to simulate a sensor for indoor positioning
class Sensor:
    def __init__(self, x, y, range_):
        self.position = Coordinates(x, y)  # Position of the sensor
        self.range = range_  # Detection range of the sensor

    def get_rssi(self, customer_position):
        """
        Calculate the Received Signal Strength Indicator (RSSI) based
        on the distance between the sensor and the customer's position.
        """
        distance = math.sqrt(
            (customer_position.x - self.position.x) ** 2 +
            (customer_position.y - self.position.y) ** 2
        )
        if distance > self.range:
            return -100  # Signal strength too weak beyond range
        else:
            return -10 * math.log10(distance / self.range)  # RSSI calculation

    def __repr__(self):
        return f"Sensor(x={self.position.x}, y={self.position.y}, range={self.range})"

# Function to simulate data collection over multiple steps
def simulate_data(steps):
    """
    Simulate data collection by combining readings from various sensors
    over a specified number of steps.
    """
    # Instantiate sensor objects
    gyroscope = Gyroscope()
    camera = Camera()
    rfid = RFID()
    motion_detector = MotionDetector()

    # Dictionary to store the data collected at each step
    data = {
        "timestamp": [],
        "rotation": [],
        "foot_traffic": [],
        "item_picked_up": [],
        "movement_detected": []
    }

    start_time = datetime.now()  # Starting timestamp

    for step in range(steps):
        timestamp = start_time + timedelta(seconds=step)  # Calculate timestamp

        # Collect sensor readings
        rotation = gyroscope.get_rotation()
        foot_traffic = camera.count_foot_traffic()
        item_picked_up = rfid.detect_item_pickup()
        movement_detected = motion_detector.detect_movement()

        # Append readings to the dictionary
        data["timestamp"].append(timestamp)
        data["rotation"].append(rotation)
        data["foot_traffic"].append(foot_traffic)
        data["item_picked_up"].append(item_picked_up)
        data["movement_detected"].append(movement_detected)

    # Convert the data dictionary into a DataFrame
    return pd.DataFrame(data)

# Function to perform exploratory data analysis on collected data
def perform_eda(df):
    """
    Analyze the data through summary statistics, visualizations,
    and detecting trends.
    """
    print("[EDA] Data Summary:")
    print(df.head())  # Display the first few rows
    print("\n[EDA] DataFrame Info:")
    print(df.info())  # Display structure and memory usage
    print("\n[EDA] Descriptive Statistics:")
    print(df.describe())  # Display summary statistics
    print("\n[EDA] Missing values per column:")
    print(df.isnull().sum())  # Check for missing values

    # Visualize data distribution with histograms
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols].hist(figsize=(12, 8), bins=20)
    plt.suptitle("Histograms of Numeric Columns")
    plt.show()

    # Encode True/False columns as integers for correlation analysis
    df["item_picked_up"] = df["item_picked_up"].astype(int)
    df["movement_detected"] = df["movement_detected"].astype(int)

    # Correlation heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.corr(), annot=True, cmap="coolwarm", vmin=-1, vmax=1)
    plt.title("Correlation Heatmap")
    plt.show()

    # Plot time series of rotation and foot traffic
    plt.figure(figsize=(14, 6))
    plt.plot(df["timestamp"], df["rotation"], label="Rotation (degrees)", color='blue')
    plt.plot(df["timestamp"], df["foot_traffic"], label="Foot Traffic (count)", color='orange')
    plt.xlabel("Timestamp")
    plt.ylabel("Sensor Data")
    plt.legend()
    plt.title("Time Series of Rotation and Foot Traffic")
    plt.show()

    # Visualize foot traffic during movement
    movement_data = df[df["movement_detected"] == 1]
    plt.figure(figsize=(14, 6))
    plt.plot(movement_data["timestamp"], movement_data["foot_traffic"], label="Foot Traffic (movement detected)", color='red')
    plt.xlabel("Timestamp")
    plt.ylabel("Foot Traffic Count")
    plt.legend()
    plt.title("Foot Traffic When Movement is Detected")
    plt.show()

# Main simulation execution
df = simulate_data(SIMULATION_STEPS)  # Generate simulated data
perform_eda(df)  # Perform EDA
