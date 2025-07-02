# Edge Sensor Telemetry Visualization

This project demonstrates real-time monitoring of environmental conditions using ESP32-based sensors and a time-series dashboard. Designed as a lightweight, scalable telemetry system for edge-to-cloud or local deployments.

## Components

- ESP32: temperature (DHT11), motion (PIR)
- MQTT: publish sensor data
- Python bridge: MQTT → InfluxDB
- Grafana: real-time dashboard visualization

##  Use Case

Condition monitoring, motion detection, basic status tracking for machines, rooms, or assembly areas.

##  Dashboard Preview

![Dashboard](dashboard/grafana_screenshot.png)

##  Architecture

![Architecture](dashboard/architecture.png)

##  Repo Contents

- `/esp32/`: Arduino code for sensor acquisition
- `/python_bridge/`: MQTT subscriber → Influx writer
- `/dashboard/`: Grafana JSON + visualizations
