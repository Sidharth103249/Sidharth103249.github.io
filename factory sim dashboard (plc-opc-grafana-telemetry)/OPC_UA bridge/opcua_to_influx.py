# necessary modules
from influxdb_client import InfluxDBClient, Point, WritePrecision
from datetime import datetime, UTC
from opcua import Client
import time

# Configuration for OPC-UA and InfluxDB
opcua_url = "opc.tcp://192.168.1.100:4840"  # OPC-UA server URL
bucket = "plc_data"                         # InfluxDB bucket name (similar to database)
org = "-"                                   # InfluxDB organization (grouping of users and resources)
token = ""  # InfluxDB access token
url = "http://localhost:8086"               # InfluxDB URL

# Initialize InfluxDB client
client = InfluxDBClient(url=url, token=token, org=org)
from influxdb_client.client.write_api import SYNCHRONOUS
write_api = client.write_api(write_options=SYNCHRONOUS)

# Connect to OPC-UA server
opcua_client = Client(opcua_url)
opcua_client.connect()
print("Connected to OPC-UA")

# Define OPC-UA nodes to read
nodes = {
    "motion": opcua_client.get_node("ns=3;s=\"DB_Tank\".\"MotionDetected\""),
    "level": opcua_client.get_node("ns=3;s=\"DB_Tank\".\"Level\""),
    "flowRate": opcua_client.get_node("ns=3;s=\"DB_Tank\".\"FlowRate\""),
    "alarm": opcua_client.get_node("ns=3;s=\"DB_Tank\".\"Alarm\""),
    "pumpOn": opcua_client.get_node("ns=3;s=\"DB_Tank\".\"PumpOn\"")
}

try:
    while True:
        try:
            # Read current values from all OPC-UA nodes
            tag_data = {
                k: node.get_value() for k, node in nodes.items()
            }

            # Create an InfluxDB Point with the tag and field data
            point = (
                Point("plc_telemetry")
                .tag("device", "PLC1")
                .field("tank_level", float(tag_data["level"]))
                .field("flowRate", float(tag_data["flowRate"]))
                .field("alarm", float(tag_data["alarm"]))
                .field("pump_status", int(tag_data["pumpOn"]))
                .field("Trigger_Sensor", int(tag_data["motion"]))
                .time(datetime.now(UTC), WritePrecision.NS)
            )

            # Write the data point to InfluxDB
            write_api.write(bucket=bucket, org=org, record=point)

        except Exception as e:
            # Catch errors in either reading from OPC-UA or writing to InfluxDB
            print("Error reading or writing:", e)

        time.sleep(1)  # Wait

finally:
    # OPC-UA client disconnects cleanly on exit
    opcua_client.disconnect()
