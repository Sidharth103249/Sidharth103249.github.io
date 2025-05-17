#include<iostream.h>
#include<thread>
using namespace std;
volatile bool buttonPressed = false;
int InterruptPin = 2;

void IRAM_ATTR handleInterrupt () {
buttonPressed = true;
}

void setup (){
    cout << "Printing number: " << x << endl;
    attachInterrupt(digitalPinToInterrupt(InterruptPin), handleInterrupt, FALLING);
    }

void loop () {
    if (buttonPressed) {
        buttonPressed = false;
        cout << "Interrupt occured.";
    }
    // thread t(setup, 0);
    // t.detach();
}