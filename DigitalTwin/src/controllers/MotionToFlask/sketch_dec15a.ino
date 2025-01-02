#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "***********";
const char* password = "***************";
const int motionSensorPin = 4; // Pin where PIR sensor is connected
unsigned long lastMotionTime = 0; // Time of the last motion detection
const unsigned long motionCooldown = 10000; // 5 seconds cooldown period

void setup() {
  Serial.begin(115200);
  pinMode(motionSensorPin, INPUT);
  WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to Wifi...");
  }
  Serial.println("Connected to Wifi network...");
}


void loop() {

int sensorState = digitalRead(motionSensorPin); // Read motion sensor state

  // Check if motion is detected
  if (sensorState == HIGH) {
    if (millis() - lastMotionTime > motionCooldown) {
      Serial.println("Motion detected!");

      // Send motion data to the Flask server
      HTTPClient http;
      http.begin("http://************/motion");
      http.addHeader("Content-Type", "application/json");

      String payload = "{\"motionDetection\": 1}";
      int httpResponseCode = http.POST(payload);

      if (httpResponseCode > 0) {
        Serial.println("Motion data sent successfully");
      } else {
        Serial.println("Error sending motion data");
      }
      http.end();

      lastMotionTime = millis(); // Update the last motion time
    }
  } else {
    Serial.println("No motion.");
  }

  delay(200); // Small delay for stability
}


//   // Check if motion is detected
//   if (sensorState == HIGH) {
//     if (millis() - lastMotionTime > motionCooldown) {
//       // If 5 seconds have passed since the last detection, log motion
//       Serial.println("Motion detected!");
//       lastMotionTime = millis(); // Update the last motion time
//     }
//   } else {
//     // No motion
//     Serial.println("No motion.");
//   }

//   delay(200); // Small delay for stability
// }
