#include "esp32-hal-gpio.h"
#include <Arduino.h>

const int btn = 2
int lastbtn = HIGH;

void setup() {
    Serial.begin(115200)
    pinMode(btn, INPUT_PULLUP);
}

void loop() {
    int b =digitalRead(btn);
    if (b != lastbtn) {
        if (b == LOW) {
            Serial.println("\"{btn\}":1}");
        } else {
         Serial.println("{\"btn\":0}");
         }
         lastbtn = b;
    }
    delay(20);
}