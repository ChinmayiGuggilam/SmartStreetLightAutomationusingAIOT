# SmartStreetLight
# 🌃 Smart Street Light Automation using AIoT

This project automates street lights using AIoT (Artificial Intelligence of Things) to conserve energy, enhance safety, and detect faults like LED damage.
It integrates sensors, microcontrollers, and cloud-based dashboards for real-time monitoring and control.

## 🚀 Features

- 💡 **Automatic Light Control**: Lights turn ON/OFF based on ambient light and motion detection.
- 🔄 **AI-Based Optimization**: Decision-making based on environmental conditions (e.g., light intensity, motion, time).
- 🔧 **LED Damage Detection**: Detects and notifies when an LED fails or malfunctions.
- 📲 **Cloud Connectivity**: Sensor data is logged into Google Sheets using MIT App Inventor.
- 📊 **Remote Monitoring**: Real-time status display and history through a connected dashboard.
- 🧠 **AIoT Integration**: Combines sensor inputs with cloud intelligence for smarter automation.

## 🛠️ Tech Stack


- **Sensors**: LDR sensor
- **Communication**: Wi-Fi (ESP32) 
- **Cloud Platform**: Google Sheets API via MIT App Inventor
- **Mobile App**: MIT App Inventor for monitoring and control
- **Languages**: C(Arduino), Blockly (MIT App)



## 📝 How It Works

1. **LDR Sensor** measures ambient light. If light level is below threshold and motion is detected, streetlight turns ON.
2. **MIT App Inventor** sends data (timestamp, light status, motion, faults) to Google Sheets.
3. App can also retrieve data for history/analytics or status monitoring.

## 📱 Screenshots

<img width="400" height="400" alt="1" src="https://github.com/user-attachments/assets/5269fe51-bd12-411e-96c6-d6dbb37552c9" />
<img width="400" height="400" alt="2" src="https://github.com/user-attachments/assets/4d34f2c3-6691-45dc-a063-ab992879a9cd" />
<img width="400" height="400" alt="3" src="https://github.com/user-attachments/assets/32134989-0b63-4541-8c94-d69e80ca96cc" />
<img width="400" height="400" alt="4" src="https://github.com/user-attachments/assets/91847505-3332-4204-b7a7-e27106153cb1" />
<img width="400" height="400" alt="5" src="https://github.com/user-attachments/assets/761858a4-ca95-4227-908c-2609aafdee14" />


## 🔌 Hardware Required

- Raspberry pi pico
- LDR (Light Dependent Resistor)
- LEDs 
- Resistors, Breadboard, Wires, Power Supply


