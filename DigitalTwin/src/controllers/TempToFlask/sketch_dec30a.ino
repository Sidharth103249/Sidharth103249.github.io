// Sensor Libraries
#include <OneWire.h>
#include <DallasTemperature.h>
#include <WiFi.h>
#include <HTTPClient.h>
#define ONE_WIRE_BUS 4
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire); 
const char* ssid = "********";
const char* password = "******";

void setup() {

Serial.begin(115200); 
sensors.begin();
WiFi.begin(ssid, password);
while (WiFi.status() != WL_CONNECTED) {
  delay(1000);
  Serial.println(".");
}
Serial.println("Connected to Wifi network...");

}

void loop() {
  if (WiFi.status() == WL_CONNECTED){
    sensors.requestTemperatures();
    int temperature = sensors.getTempCByIndex(0);
    
    //Send data to server
    HTTPClient http;
    http.begin("http://*************/temperature");
    http.addHeader("Content-Type", "application/json");
    String jsonPayload = String("{\"temperature\":") + String(temperature) + "}";
     int httpResponseCode = http.POST(jsonPayload);
    Serial.print("httpResponseCode is : ");  //debug
    Serial.println(httpResponseCode);     //debug
    if (httpResponseCode > 0) {
       Serial.println("1");  //debug
      String response = http.getString();
      Serial.println("Server Response: " + response);
    } else {
      Serial.printf("HTTP POST Failed, error: %s\n", http.errorToString(httpResponseCode).c_str());
    }

    http.end();
  }else {
    Serial.println("WiFi not connected.");
  }
}
