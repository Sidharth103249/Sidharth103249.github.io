import threading
import time
import asyncio
from flask_cors import CORS
from flask import Flask, request, jsonify
from tapo import ApiClient
from requests_html import HTMLSession

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Environment Variables (For Security, you should store these safely)
TAPO_USERNAME = "************"
TAPO_PASSWORD = "*********"
TAPO_IP = "*************"

# Global variable to store the latest temperature
latest_weather = {"temperature": None, "unit": None, "description": None}

# Webscrape google weather data
def webscrape():
    global latest_weather
    try:
        print("inside webscrape")        
        s = HTMLSession()
        url = f'https://www.google.com/search?q=weather+aachen'
        r = s.get(url, headers={'User-Agent': '**'})
        temp = r.html.find('span#wob_tm', first=True).text
        unit = r.html.find('div.vk_bk.wob-unit span.wob_t', first=True).text
        desc = r.html.find('div.VQF4g', first=True).find('span#wob_dc', first=True).text

        # Update the latest weather data
        latest_weather.update({"temperature": temp, "unit": unit, "description": desc})
        print(f"Updated weather: {latest_weather}")
    except Exception as e:
        print(f"Error during web scraping: {e}")

def scraper_task():
    """Background task that runs the scraper every 5 seconds."""
    while True:
        webscrape()
        time.sleep(5)  # Wait for 5 seconds before scraping again

# Start the scraper in a separate thread
thread = threading.Thread(target=scraper_task, daemon=True)
thread.start()

async def toggle_bulb():
    # Create an ApiClient instance for controlling the Tapo bulb
    client = ApiClient("********", "**************")
    device = await client.l530("192.168.0.62")

    # Retrieve current device information
    device_info = await device.get_device_info()

    # Toggle the device on or off based on its current state
    if device_info.device_on:
        await device.off()  # Turn the bulb off
        action = "off"
    else:
        await device.on()   # Turn the bulb o
        action = "on"
    
    return action

@app.route('/motion', methods=['POST'])
def motion():
    data = request.get_json()  # Parse JSON from the request body
    print("Received data:", data)  # Log the received data in the console

    if data:
        action = asyncio.run(toggle_bulb())
        return jsonify({"message": "Data received successfully!", "data": data}), 200
    else:
        return jsonify({"message": "No data received!"}), 400


@app.route('/light_status', methods=['GET'])
def get_light_status():
    # Fetch current light status
    async def fetch_status():
        client = ApiClient(TAPO_USERNAME, TAPO_PASSWORD)
        device = await client.l530(TAPO_IP)
        device_info = await device.get_device_info()
        return "on" if device_info.device_on else "off"
    
    action = asyncio.run(fetch_status())
    return jsonify({"light_status": action})

@app.route('/lightControl', methods=['POST'])
def controlLight():
    try:
        # Parse the incoming JSON
        data = request.get_json()
        print("Data received lightControl python:", data)  # Debug log
        # Check if 'click_data' exists in the incoming data
        if not data or 'click_data' not in data:
            return jsonify({"error": "'click_data' is required"}), 400

        # Now proceed with controlling the light based on the 'click_data'
        async def toggle_light():
            client = ApiClient(TAPO_USERNAME, TAPO_PASSWORD)
            device = await client.l530(TAPO_IP)
            if data['click_data'] == "on":
                await device.on()
                return "on"
            else:
                await device.off()
                return "off"
        
        # Run the async function and return the response
        action = asyncio.run(toggle_light())
        return jsonify({"message": f"Light turned {action}"}), 200
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/temperature', methods=['POST'])
def receive_temperature():
    print("Received POST request for /temperature")
    global latest_temperature
    data = request.get_json()
    if 'temperature' in data:
        latest_temperature = data['temperature']
        print(f"Received Temperature: {latest_temperature} °C")
        return jsonify({"message": "Temperature received"}), 200
    else:
        return jsonify({"error": "Temperature not found in request"}), 400

@app.route('/temperature', methods=['GET'])
def send_temperature():
    global latest_temperature
    if latest_temperature is not None:
        print("Received GET request for /temperature")
        return jsonify({"temperature": latest_temperature}), 200
    else:
        return jsonify({"error": "No temperature data available"}), 404

@app.route('/weather', methods=['GET'])
def get_weather():
    """API endpoint to get the latest weather data."""
    return jsonify(latest_weather), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


