import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pytz
from datetime import datetime

# ThingSpeak channel details
CHANNEL_ID = "2662816"  # Replace with your ThingSpeak Channel ID
API_KEY = "4QZVN0HJ79A6A3BI"  # Replace with your ThingSpeak API Key

# Thresholds for air quality parameters
THRESHOLDS = {
    "gas": 100,  # ppm
    "temperature": 37,  # °C
    "humidity": 80,  # % 
}

def fetch_thingspeak_data():
    """Fetch data from ThingSpeak."""
    url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json"

    params = {
        "api_key": API_KEY,  # Your ThingSpeak API key
        "results": 1000  # Adjust the number of records to fetch as necessary
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()['feeds']
    else:
        st.error(f"Failed to fetch data: {response.status_code}")
        return None

def process_data(data):
    """Process the raw data into a pandas DataFrame."""
    df = pd.DataFrame(data)
    
    # Convert 'created_at' to datetime format
    df['created_at'] = pd.to_datetime(df['created_at'])
    
    # Extract just the time (without the date) for plotting
    df['time'] = df['created_at'].dt.strftime('%H:%M:%S')  # Extract just time

    # Convert fields to numeric, coercing any errors to NaN (useful if there are invalid entries)
    df['field1'] = pd.to_numeric(df['field1'], errors='coerce')  # Temperature
    df['field2'] = pd.to_numeric(df['field2'], errors='coerce')  # Humidity
    df['field3'] = pd.to_numeric(df['field3'], errors='coerce')  # Gas concentration
    
    # Drop rows with invalid data (NaN values)
    df = df.dropna(subset=['field1', 'field2', 'field3'])
    
    return df

def create_bar_chart(df):
    """Create a bar chart of the average values."""
    avg_values = {
        'Gas Concentration (ppm)': df['field3'].mean(),
        'Temperature (°C)': df['field1'].mean(),
        'Humidity (%)': df['field2'].mean(),
    }

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(avg_values.keys(), avg_values.values(), color=['blue', 'green', 'orange'])
    ax.set_title('Average Air Quality Parameters')
    ax.set_ylabel('Average Value')
    
    return fig

def create_line_chart(df, field, title, ylabel):
    """Create a line chart."""
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df['time'], df[field])
    ax.set_title(title)
    ax.set_xlabel('Time')
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=45)
    
    return fig

def check_thresholds(latest_data):
    """Check if any parameters exceed their thresholds."""
    alerts = []
    if latest_data['field3'] > THRESHOLDS['gas']:
        alerts.append(f"Gas concentration ({latest_data['field3']:.2f} ppm) exceeds threshold!")
    if latest_data['field1'] > THRESHOLDS['temperature']:
        alerts.append(f"Temperature ({latest_data['field1']:.1f} °C) exceeds threshold!")
    if latest_data['field2'] > THRESHOLDS['humidity']:
        alerts.append(f"Humidity ({latest_data['field2']:.1f} %) exceeds threshold!")
    return alerts

def get_pakistani_time():
    """Get the current time in Pakistan Standard Time (PST)."""
    tz = pytz.timezone('Asia/Karachi')
    return datetime.now(tz).strftime('%H:%M:%S')

# Streamlit app
st.title('Air Quality Monitoring Dashboard')

# Fetch and process data
data = fetch_thingspeak_data()
if data:
    df = process_data(data)

    # Display raw data for debugging
    st.write("Processed Data (First 10 Entries):", df.head(10))  # Check the processed data

    # Display latest readings
    st.subheader('Current Air Quality Readings')
    col1, col2, col3 = st.columns(3)

    # Ensure we access the latest data correctly (use iloc[-1] for the latest row)
    latest_data = df.iloc[-1]

    # Display latest readings
    col1.metric("Current Temperature", f"{latest_data['field1']:.1f} °C")  # Temperature (Field 1)
    col2.metric("Current Humidity", f"{latest_data['field2']:.1f} %")  # Humidity (Field 2)
    col3.metric("Current Gas Concentration", f"{latest_data['field3']:.2f} ppm")  # Gas Concentration (Field 3)
    
    # Check thresholds for alerts
    alerts = check_thresholds(df.iloc[-1])
    if alerts:
        st.warning("Alerts:")
        for alert in alerts:
            st.warning(alert)

    # Display current time in Pakistani timezone
    st.write(f"Current Time (Pakistan): {get_pakistani_time()}")

    # Create tabs (using selectbox to switch between sections)
    option = st.selectbox(
        'Select a parameter to view:',
        ['Gas Concentration Over Time', 'Temperature Over Time', 'Humidity Over Time', 'Average Values']
    )
    
    # Display selected tab content
    if option == 'Gas Concentration Over Time':
        st.subheader('Gas Concentration Over Time')
        st.pyplot(create_line_chart(df, 'field3', 'Gas Concentration Over Time', 'Concentration (ppm)'))
    
    elif option == 'Temperature Over Time':
        st.subheader('Temperature Over Time')
        st.pyplot(create_line_chart(df, 'field1', 'Temperature Over Time', 'Temperature (°C)'))
    
    elif option == 'Humidity Over Time':
        st.subheader('Humidity Over Time')
        st.pyplot(create_line_chart(df, 'field2', 'Humidity Over Time', 'Humidity (%)'))
    
    elif option == 'Average Values':
        st.subheader('Average Values of Air Quality Parameters')
        st.pyplot(create_bar_chart(df))

else:
    st.error("Failed to fetch data from ThingSpeak. Please check your connection and try again.")
