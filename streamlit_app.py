import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
import time
from datetime import datetime, timedelta

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
                
                # Convert the timestamp to the 'days' format
                sensor_data["timestamp"] = pd.to_datetime(sensor_data["timestamp"])
                time_range = sensor_data["timestamp"].max() - timedelta(days=1)  # Get data for the last day
                filtered_data = sensor_data[sensor_data["timestamp"] > time_range]
                
                # Create the plots
                fig, axs = plt.subplots(4, 1, figsize=(10, 16), sharex=True)

                # Plot gyroscope X data
                axs[0].plot(filtered_data["timestamp"], filtered_data["gyroscope_x"], color="blue")
                axs[0].set_title("Gyroscope X")
                axs[0].set_ylabel("Degrees")
                axs[0].tick_params(axis='x', rotation=45)

                # Plot gyroscope Y data
                axs[1].plot(filtered_data["timestamp"], filtered_data["gyroscope_y"], color="orange")
                axs[1].set_title("Gyroscope Y")
                axs[1].set_ylabel("Degrees")
                axs[1].tick_params(axis='x', rotation=45)

                # Plot gyroscope Z data
                axs[2].plot(filtered_data["timestamp"], filtered_data["gyroscope_z"], color="green")
                axs[2].set_title("Gyroscope Z")
                axs[2].set_ylabel("Degrees")
                axs[2].tick_params(axis='x', rotation=45)

                # Plot RFID and Camera motion data on the fourth subplot
                axs[3].step(filtered_data["timestamp"], filtered_data["rfid_detected"], label="RFID Detected", color="purple", where="mid")
                axs[3].step(filtered_data["timestamp"], filtered_data["camera_motion"], label="Camera Motion", color="red", where="mid")
                axs[3].set_title("RFID and Camera Motion Detection")
                axs[3].set_ylabel("Binary Detection")
                axs[3].set_xlabel("Timestamp")
                axs[3].legend()
                axs[3].tick_params(axis='x', rotation=45)

                st.pyplot(fig)

            # Wait for the next update
            time.sleep(update_interval)

    except KeyboardInterrupt:
        st.write("Live data updates stopped.")
else:
    st.write("Click 'Start Live Updates' to begin streaming sensor data.")
