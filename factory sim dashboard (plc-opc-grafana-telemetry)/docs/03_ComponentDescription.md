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
