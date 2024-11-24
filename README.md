
# IOT Based Air Quality Monitoring System using Thinkspeak & Streamlit
* Introduction to the Project

The project is an IoT-based air quality monitoring system designed to continuously measure and monitor air quality parameters such as gas concentration, temperature, and humidity.

* Purpose: 
To track air quality and send alerts when certain thresholds are exceeded. This system can help improve environmental monitoring and public health awareness.





## Key Features

1) Monitors gas concentration, temperature, and humidity in real-time.
2) Alerts users when thresholds are exceeded within the dashboard.
3) Visualizes data using Streamlit (line charts, bar charts, and live metrics).
4) Data stored and retrieved from ThingSpeak cloud.
5) User-friendly interface to analyze trends over time.

## Hardware Components
IoT components used and their roles:

ESP8266: Wi-Fi module for sending data to the cloud.

MQ-135: Gas sensor for detecting pollutants.

DHT-11: Sensor for temperature and humidity.

LCD 16X2: Displays real-time data locally.

Breadboard & Jumper Wires: Connects components for the prototype.

## Software Requirements
* Required Software and Libraries:

Arduino IDE: For programming ESP8266.

Python 3.9: For Streamlit app.

Streamlit: Web application framework.

ThingSpeak API: For cloud data storage.

* Python Libraries:
streamlit, requests, pandas, matplotlib & seaborn.

## Installation
Detail steps to set up the project.

* Hardware Setup:
1) Connect MQ-135, DHT-11, and LCD to the ESP8266 using jumper wires on the breadboard.
2) Power the circuit and ensure all sensors are functional.

* Arduino Code:
1) Open the Arduino IDE.
2) Install required libraries for ESP8266, MQ-135, LCD 16x2 and DHT-11.
3) Upload the Arduino code to the ESP8266 module.

*  Streamlit Dashboard:
1) Install Python 3.9 or later.
2) Install required Python libraries.

Commands for Installing libraries:
    
    pip install streamlit requests pandas matplotlib seaborn pytz

3) Save the Streamlit code in a .py file (e.g., app.py).
Run the Streamlit app using the below Command:

    python -m streamlit run "DV WebApp.py"


## How to Use
* how to operate the system.

1) Power up the hardware setup.
2) Ensure the ESP8266 is connected to Wi-Fi.
3) Start the Streamlit app to view real-time data on the dashboard.
4) Monitor metrics and charts for air quality status.
5) Look for alerts if thresholds are crossed in the dashboard.
## Insights and Results
* Obervations from the Project.

1) Data trends reveal patterns in air quality over time.
2) Threshold-based alerts help mitigate health risks in polluted environments.
3) Useful for environmental monitoring and awareness.
## Authors
* Contributors of Our Project:
Developed by My team of 5 Data Science girls.
