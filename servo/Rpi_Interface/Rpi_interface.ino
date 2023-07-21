int finePin = 10;
int coarsePin = 11;
const int stepPin = 3; //Y.STEP
const int dirPin = 6; // Y.DIR
const int enPin = 8;
const float steps/degree = 0.5555555556
const int stepsPerRev=200;
int pulseWidthMicros = 100; 	// microseconds
int millisBtwnSteps = 1000;

void setup() {
    Serial.begin(9600);
 	pinMode(enPin, OUTPUT);
 	digitalWrite(enPin, LOW);
 	pinMode(stepPin, OUTPUT);
 	pinMode(dirPin, OUTPUT);
    pinMode(finePin, INPUT);
    pinMode(coarsePin, INPUT);

    // homing routine
}

void loop() {
    // read inputPin and step the motor
    // restrain scan range
    if(digitalRead(finePin) == HIGH){
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(pulseWidthMicros);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(millisBtwnSteps);
    }
}