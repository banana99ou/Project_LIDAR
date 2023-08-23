#include <AccelStepper.h>

const int stepPin = 3;
const int dirPin = 6;
const int enPin = 8;

AccelStepper stepper(AccelStepper::DRIVER, stepPin, dirPin);
setEnablePin(enPin);
disableOutputs();

void setup() {
    Stepper.setMaxSpeed(70);
    stepper.setAcceleration(100);
}

void loop() {
    stepper.moveTo()
}