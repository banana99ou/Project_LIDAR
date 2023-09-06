const int stepPin = 3;          // Change this to your actual pin
const int dirPin = 6;           // Change this to your actual pin
const int limitSwitchPin1 = 10;  // Change this to your first limit switch pin
const int limitSwitchPin2 = 11;  // Change this to your second limit switch pin
int finePin = 10;
int coarsePin = 11;
const int enPin = 8;
const float StepsPerDegree = 0.5555555556;
const int stepsPerRev = 200;
int pulseWidthMicros = 100;   // microseconds
int millisBtwnSteps = 1000;
void setup() {
 	Serial.begin(9600);
 	pinMode(enPin, OUTPUT);
 	digitalWrite(enPin, LOW);
 	pinMode(stepPin, OUTPUT);
 	pinMode(dirPin, OUTPUT);
 	Serial.println(F("CNC Shield Initialized"));
}
void loop() {
 	Serial.println(F("Running clockwise"));
 	digitalWrite(dirPin, HIGH); // Enables the motor to move in a particular direction
 	// Makes 200 pulses for making one full cycle rotation
 	for (int i = 0; i < stepsPerRev/4; i++) {
 			digitalWrite(stepPin, HIGH);
 			delayMicroseconds(pulseWidthMicros);
 			digitalWrite(stepPin, LOW);
 			delayMicroseconds(millisBtwnSteps);
      delayMicroseconds(10000000000);
 	}
 	delay(1000); // One second delay
 	Serial.println(F("Running counter-clockwise"));
 	digitalWrite(dirPin, LOW); //Changes the rotations direction
 	// Makes 400 pulses for making two full cycle rotation
 	for (int i = 0; i < stepsPerRev/4; i++) {
 			digitalWrite(stepPin, HIGH);
 			delayMicroseconds(pulseWidthMicros);
 			digitalWrite(stepPin, LOW);
 			delayMicroseconds(millisBtwnSteps);
      delayMicroseconds(10000000000);
 	}
 	delay(1000);
}
