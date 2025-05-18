#include<Arduino.h>

volatile bool buttonPressed = false;
volatile unsigned long lastInterruptTime = 0;
int InterruptPin = 4;
const int debounceDelay = 50;

void IRAM_ATTR handleInterrupt () {
  unsigned int long currentTime = millis();
  if (currentTime - lastInterruptTime > debounceDelay){
    buttonPressed = true;
  lastInterruptTime = currentTime;
  }
  
}

void setup (){
  Serial.begin(115200);
  delay(1000);
  Serial.println("Hello, ESP32!");
  pinMode(InterruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(InterruptPin), handleInterrupt, CHANGE);
    }

void loop () {
    if (buttonPressed) {
        buttonPressed = false;
        Serial.println("Interrupt occured.");
    }
    // thread t(setup, 0);
    // t.detach();
}