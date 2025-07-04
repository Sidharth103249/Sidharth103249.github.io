# Deployment and Execution

## Requirements
- Siemens TIA Portal v18
- PLCSIM Advanced
- Python 3.10+
- InfluxDB
- Grafana (local or Docker)

## Steps
1. Launch PLCSIM Advanced and run the TIA project
2. Start the Python bridge: `python opcua_to_influx.py`
3. Start Grafana and import the dashboard JSON
4. (Optional) Connect ESP32 MQTT publisher

## Interfaces
- OPC UA Server: `opc.tcp://localhost:4840`
- InfluxDB: `http://localhost:8086`
