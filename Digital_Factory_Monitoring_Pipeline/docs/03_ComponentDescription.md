# 03_ComponentDescription.md

## Overview

This document describes the primary components of the telemetry simulation system. Each component is listed with its role, interfaces, and core functions.

---

###  Component: TIA Portal PLC Project (`/tia_project/factory_sim.zip`)

**Role:**  
Simulates an industrial tank system controlled by motion and temperature inputs.

**Functions:**
- If `MotionDetected` is true, pump turns on.
- Tank level increases while pump is on.
- `TempAlarm` triggers alarm logic if temperature exceeds threshold.
- All control logic is executed in `FC_TankControl`, called by `OB1`.

**Inputs:**
- `DB_Tank.MotionDetected` (Bool, from REST/ESP32)
- `DB_Tank.TempAlarm` (Bool, from REST/ESP32)

**Outputs:**
- `DB_Tank.PumpOn` (Bool)
- `DB_Tank.Level` (Real)

**Interfaces:**
- OPC UA (Read/Write, PLCSIM Advanced)

---

###  Component: OPC UA to InfluxDB Bridge (`/opc_bridge/opcua_to_influx.py`)

**Role:**  
Polls selected variables from the PLC via OPC UA and writes to InfluxDB.

**Functions:**
- Connects to `opc.tcp://localhost:4840`
- Reads values from `DB_Tank.Level`, `PumpOn`, etc.
- Converts values to InfluxDB line protocol
- Writes into `factory_telemetry` measurement

**Update Rate:**  
1-second polling

---

###  Component: REST-to-OPC API (`/opc_bridge/opc_rest_api.py`)

**Role:**  
Exposes a REST endpoint to allow toggling of `MotionDetected` via HTTP.

**Functions:**
- HTTP POST `/motion` → connect to OPC UA
- Reads current value of `DB_Tank.MotionDetected`
- Inverts the value and writes it back
- Disconnects cleanly

**Use Case:**  
Allows test tools or external dashboards to simulate sensor input
