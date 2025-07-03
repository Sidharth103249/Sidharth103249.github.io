# Industrial Telemetry Visualization: Siemens PLC TIA + OPC UA + Grafana

This project demonstrates a full-stack simulation of a factory telemetry system — from PLC logic to real-time dashboards — using OPC UA as the data backbone.
[Watch my visual walkthrough of the pipeline on YouTube](https://youtu.be/iq41lGUyn7w)

![Dashboard](https://Sidharth103249.github.io/factory-sim-dashboard/assets/image/dashboard.png)

##  Stack
- Siemens S7-1500 logic (TIA Portal, simulated)
- PLCSIM Advanced (OPC UA server)
- Python (opcua → InfluxDB)
- Grafana (real-time visualization)
- ESP32 edge sensor stream

##  Goals
- Simulate a realistic tank/pump process
- Collect real-time telemetry from DB variables
- Visualize key industrial metrics (level, flow, motion, alarms)
