# Component Description

## Component: TankControlLogic
- Language: TIA SCL
- Inputs: MotionDetected (Bool), TempAlarm (Bool)
- Outputs: PumpOn (Bool), Level (Real)

## Component: OPC_UA_Client
- Technology: Python + FreeOpcUa
- Function: Poll selected DB tags at 1s interval

## Component: Grafana_Dashboard
- Panels: Level, Pump Status, Alarms
- Data Source: InfluxDB

## Component: opc_rest_api.py

- Endpoint: `/motion` (HTTP POST)
- Reads tag: `DB_Tank.MotionDetected` via OPC UA
- Inverts Boolean and writes back to PLC
- Use Case: External web system toggles simulated motion sensor

Example:
```bash
curl -X POST http://localhost:5000/motion
