#include<Arduino.h>

volatile bool buttonPressed = false;
int InterruptPin = 4;
hw_timer_t *timer = NULL;

void IRAM_ATTR handleInterrupt () {
    buttonPressed = true;
}

void setup (){
  Serial.begin(115200);
  delay(1000);
  Serial.println("Hello, ESP32!");
  pinMode(InterruptPin, INPUT_PULLUP);
  timer = timerBegin(0, 80, true);
  timerAttachInterrupt(timer, &handleInterrupt, true);
  timerAlarmWrite(timer, 1000000, true);
  timerAlarmEnable(timer);
    }

void loop () {
    if (buttonPressed) {
        buttonPressed = false;
        Serial.println("Interrupt occured.");
    }
}