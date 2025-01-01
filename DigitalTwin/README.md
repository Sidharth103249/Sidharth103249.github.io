# Prototype Digital Twin of Home Environment

## 🌟 Overview
This project demonstrates a **prototype digital twin** of a home environment. The goal is to create a virtual representation of a physical object (a room in this case) with **real-time two-way communication** between the physical and virtual worlds.

This prototype focuses on:
1. **Real-time monitoring** of environmental data (e.g., temperature, motion, light status).
2. **Interactive control** of room elements through a **3D virtual model**.

---

## 🤔 What Are Digital Twins?
Digital twins are virtual representations of physical objects that simulate the real-world state in real time. While definitions vary, a common understanding is that a digital twin:
- **Replicates real-world objects**, processes, or systems in a virtual environment.
- **Allows two-way communication**, enabling monitoring and control of the physical object.

### Key Benefits of Digital Twins:
- Reduce costs during design, testing, and operational phases.
- Improve understanding of behavior under different conditions.
- Enable better decision-making through simulations and real-time data.

This project explores these benefits in a home environment, using a single room as a testbed for digital twin functionality.

---

## 🚀 Features
### Current Capabilities:
1. **Real-Time Monitoring**:
   - Light status.
   - Motion detection.
   - Temperature (indoor and outdoor).
2. **Interactive Controls**:
   - Turn lights on/off via a 3D model.
   - Automate light brightness based on sundown time.
   - Activate night lamps during predefined times.
   - Dynamically manage lights using motion detection.

### Future Expansion Ideas:
- Extend the 3D model to represent an entire house.
- Monitor soil moisture levels for houseplants with reminders to water.
- Optimize temperature and heater settings for comfort and energy efficiency.
- Improve lighting controls for multi-occupancy scenarios.

---

## 🛠️ Setup Instructions
### Prerequisites
1. **Hardware**:
   - ESP32 microcontroller.
2. **Software**:
   - [Visual Studio Code (VSCode)](https://code.visualstudio.com/) for general programming.
   - [Arduino IDE](https://www.arduino.cc/en/software) for ESP32 programming.
3. **Azure Account**:
   - Ensure the following services are set up in your Azure account:
     - **IoT Hub**
     - **IoT Central**
     - **Azure Digital Twins**
     - **Azure Blob Storage**
   - Generate **Shared Access Signatures (SAS)** and note the primary and secondary keys for these services.

---

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/digital-twin-project.git
   cd digital-twin-project
