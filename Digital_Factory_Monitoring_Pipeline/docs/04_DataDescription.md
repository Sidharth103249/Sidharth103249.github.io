# Data Description

| Tag                     | Type   | Description                     |
|-------------------------|--------|---------------------------------|
| DB_Tank.Level           | Real   | Current tank level              |
| DB_Tank.PumpOn          | Bool   | Pump actuation status           |
| DB_Tank.MotionDetected  | Bool   | External sensor (ESP32) input   |
| DB_Tank.TempAlarm       | Bool   | Temperature alarm input         |

All tags are OPC UA accessible with Read/Write enabled.
