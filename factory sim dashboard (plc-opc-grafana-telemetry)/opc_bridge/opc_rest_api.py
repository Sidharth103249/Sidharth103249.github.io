from flask import Flask, request, jsonify
from opcua import Client, ua

app = Flask(__name__)

# OPC-UA server connection details
opcua_url = "opc.tcp://192.168.1.100:4840"
node_id = 'ns=3;s="DB_Tank"."MotionDetected"'

@app.route("/motion", methods=["POST"])
def motion_handler():
    try:
        # Connect to OPC-UA server and get target node
        opcua_client = Client(opcua_url)
        opcua_client.connect()
        node = opcua_client.get_node(node_id)

        # Read current value and invert it
        current_value = node.get_value()
        new_value = not bool(current_value)

        # Write the inverted value back to the node
        dv = ua.DataValue()
        dv.Value = ua.Variant(new_value, ua.VariantType.Boolean)
        node.set_data_value(dv)

        opcua_client.disconnect()
        return jsonify({"status": "OK", "flipped_to": new_value}), 200

    except Exception as e:
        # Handle errors during OPC-UA operations
        return jsonify({"error": str(e)}), 500

# Start Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
