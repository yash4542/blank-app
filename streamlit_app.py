import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
import time
from datetime import datetime

# Configure Streamlit page
st.set_page_config(page_title="Customer Behavior Tracking", layout="wide")

# Define main sections
st.title("Customer Behavior Tracking")

# Sidebar control for live updates
st.sidebar.header("Live Update Settings")
update_interval = st.sidebar.slider("Update Interval (seconds):", min_value=1, max_value=10, value=2)

# Placeholder function to simulate real-time sensor data
def get_sensor_data():
    """Simulate or fetch live IoT sensor data for customer behavior tracking."""
    current_time = datetime.now()
    data = {
        "timestamp": current_time,
        "gyroscope_x": random.uniform(-180, 180),  # Simulated gyroscope X-axis rotation
        "gyroscope_y": random.uniform(-180, 180),  # Simulated gyroscope Y-axis rotation
        "gyroscope_z": random.uniform(-180, 180),  # Simulated gyroscope Z-axis rotation
        "rfid_detected": random.choice([0, 1]),    # 0 = no RFID tag, 1 = RFID tag detected
        "camera_motion": random.choice([0, 1]),   # 0 = no motion, 1 = motion detected by camera
        "position_x": random.uniform(0, 100),     # Simulated indoor position X
        "position_y": random.uniform(0, 100),     # Simulated indoor position Y
    }
    return data

# Initialize an empty DataFrame for live data
sensor_data = pd.DataFrame(columns=[
    "timestamp", "gyroscope_x", "gyroscope_y", "gyroscope_z",
    "rfid_detected", "camera_motion", "position_x", "position_y"
])

# Start live data updates
if st.sidebar.button("Start Live Updates"):
    st.write("Live data updates started...")
    placeholder = st.empty()  # Placeholder for live data display
    live_chart_placeholder = st.empty()  # Placeholder for live charts
    
    # Loop to simulate live updates
    try:
        while True:
            # Fetch new sensor data
            new_data = get_sensor_data()
            # Append to the DataFrame (in place)
            sensor_data.loc[len(sensor_data)] = new_data
            # Limit DataFrame to the last 100 rows for performance
            sensor_data = sensor_data.tail(10)
            
            # Display live data in the placeholder
            placeholder.dataframe(sensor_data)

            # Update live charts in a container
            with live_chart_placeholder.container():
                st.markdown("### Sensor Readings Over Time")
                fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
                
                # Plot gyroscope data
                axs[0].plot(sensor_data["timestamp"], sensor_data["gyroscope_x"], label="Gyroscope X", color="blue")
                axs[0].plot(sensor_data["timestamp"], sensor_data["gyroscope_y"], label="Gyroscope Y", color="orange")
                axs[0].plot(sensor_data["timestamp"], sensor_data["gyroscope_z"], label="Gyroscope Z", color="green")
                axs[0].set_ylabel("Gyroscope (degrees)")
                axs[0].legend()

                # Plot RFID and Camera motion data
                axs[1].step(sensor_data["timestamp"], sensor_data["rfid_detected"], label="RFID Detected", color="purple", where="mid")
                axs[1].step(sensor_data["timestamp"], sensor_data["camera_motion"], label="Camera Motion", color="red", where="mid")
                axs[1].set_ylabel("Binary Detection")
                axs[1].legend()

                # Plot indoor positioning data
                axs[2].scatter(sensor_data["position_x"], sensor_data["position_y"], c="cyan", label="Position (X,Y)", alpha=0.6)
                axs[2].set_xlabel("Timestamp")
                axs[2].set_ylabel("Position (X, Y)")
                axs[2].legend()

                st.pyplot(fig)

            # Wait for the next update
            time.sleep(update_interval)

    except KeyboardInterrupt:
        st.write("Live data updates stopped.")
else:
    st.write("Click 'Start Live Updates' to begin streaming sensor data.")
