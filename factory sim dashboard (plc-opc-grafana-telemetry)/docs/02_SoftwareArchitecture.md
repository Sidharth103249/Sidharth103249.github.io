# Software Architecture

## System Components
- **Control Layer:** Siemens S7-1500 PLC logic (TIA Portal)
- **Communication Layer:** PLCSIM Advanced OPC UA server
- **Data Bridge:** Python script (opcua client → InfluxDB writer)
- **Visualization Layer:** Grafana dashboard

## Data Flow
- PLC (TIA) → OPC UA → Python Bridge → InfluxDB → Grafana
## Modularity
- `opcua_to_influx.py` is isolated; can be swapped for MQTT or Azure SDK
- TIA DB variables designed for external interface access
- 
### Component: REST-OPC Bridge (opc_rest_api.py)
- Technology: Python (Flask + FreeOpcUa)
- Role: Accepts HTTP POSTs to flip `MotionDetected` tag
- Interface: `/motion` endpoint
- Purpose: Web trigger for PLC simulation events
