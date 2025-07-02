#include <WiFi.h>
#include <HTTPClient.h>

// Wi-Fi credentials
const char* ssid = "";
const char* password = "";

// Motion sensor pin and state tracking
const int motionSensorPin = 4;
unsigned long lastMotionTime = 0;
const unsigned long motionCooldown = 5000; // 5-second cooldown
bool lastMotionState = false;

void setup() {
  Serial.begin(115200);
  Serial.print("boot-ok");

  pinMode(motionSensorPin, INPUT); // Configure motion sensor pin

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConnected to Wi-Fi.");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    bool motionDetected = digitalRead(motionSensorPin) == HIGH;

    // Send HTTP POST only on motion rising edge + cooldown
    if (motionDetected && !lastMotionState && (millis() - lastMotionTime > motionCooldown)) {
      Serial.println("Motion detected!");

      HTTPClient http;
      http.begin("http://192.168.0.108:5000/motion");
      http.addHeader("Content-Type", "application/json");

      String payload = String("{\"motion\": true}");
      int httpResponseCode = http.POST(payload);

      Serial.print("HTTP Response: ");
      Serial.println(httpResponseCode);

      if (httpResponseCode > 0) {
        String response = http.getString();
        Serial.println("Server response: " + response);
      } else {
        Serial.printf("HTTP POST failed: %s\n", http.errorToString(httpResponseCode).c_str());
      }

      http.end();
      lastMotionTime = millis(); // Reset cooldown timer
    }

    lastMotionState = motionDetected; // Update state tracker
  } else {
    Serial.println("WiFi not connected.");
  }

  delay(200); // Polling delay
}
