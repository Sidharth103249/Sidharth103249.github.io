import azure.functions as func
import logging
import asyncio
import os

from tapo import ApiClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="LytBulb_Trigger")
async def LytBulb_Trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    tapo_username = os.getenv("krishsid1997@gmail.com")
    tapo_password = os.getenv("AdaPoda@123")
    ip_address = os.getenv("192.168.0.62")

    client = ApiClient(tapo_username, tapo_password)
    device = await client.l350(ip_address)
    
    try:
        # Parse the JSON body
        req_body = req.get_json()

        # Extract the motionDetection value
        motion_status = req_body.get("_unmodeleddata", {}).get("motionDetection")

         # Check if motion is detected
        if motion_status == 1:
            # Query the current state of the bulb
            device_info = await device.get_device_info()

            if device_info.device_on == True:
                await device.off()
            else:
                await device.off()
                # print("Device is on. Turning it off...")

        else:
            return func.HttpResponse("No motion detected. Bulb state unchanged.",
            status_code=200         )
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)