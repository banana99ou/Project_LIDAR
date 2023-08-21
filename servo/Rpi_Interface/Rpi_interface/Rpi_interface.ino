#include <AccelStepper.h>

const int stepPin = 3;          // Change this to your actual pin
const int dirPin = 4;           // Change this to your actual pin
const int limitSwitchPin1 = 2;  // Change this to your first limit switch pin
const int limitSwitchPin2 = 5;  // Change this to your second limit switch pin

AccelStepper stepper(AccelStepper::DRIVER, stepPin, dirPin);

void setup() {
  pinMode(limitSwitchPin1, INPUT_PULLUP);
  pinMode(limitSwitchPin2, INPUT_PULLUP);
  stepper.setMaxSpeed(2000);  // Adjust this value as needed
  stepper.setAcceleration(1000);  // Adjust this value as needed
  stepper.setSpeed(1000);  // Adjust this value as needed
  
  homing();
}

void loop() {
  if (digitalRead(limitSwitchPin1) == LOW || digitalRead(limitSwitchPin2) == LOW) {
    Serial.println("LimitSwitchPressed");
    delay(100);  // Debounce delay
  }

  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == 'M') {
      char direction = Serial.read();
      int angle = Serial.parseInt();
      moveStepper(direction, angle);
    }
  }
}

void moveStepper(char direction, int angle) {
  int steps = angle * (stepsPerRev / 360.0);
  
  if (direction == 'C') {
    stepper.setDirection(1);  // Clockwise
  } else if (direction == 'A') {
    stepper.setDirection(-1);  // Anticlockwise
  }
  
  stepper.move(steps);
  
  while (stepper.distanceToGo() != 0) {
    stepper.run();
    delay(1);
  }
  
  Serial.print("MoveCompleted:");
  Serial.println(stepper.currentPosition());
}

void homing() {
  // Implement your homing logic here
  // Move the stepper motor to the home position using limit switches
  // Set the stepper's current position to the home position
  
  // Once homing is done, send a completion message to Raspberry Pi
  Serial.println("HomingCompleted");
}
