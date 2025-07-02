# Software Architecture

## System Components
- **Control Layer:** Siemens S7-1500 PLC logic (TIA Portal)
- **Communication Layer:** PLCSIM Advanced OPC UA server
- **Data Bridge:** Python script (opcua client → InfluxDB writer)
- **Visualization Layer:** Grafana dashboard

## Data Flow
