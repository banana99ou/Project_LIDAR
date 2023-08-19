int finePin = 10;
int coarsePin = 11;
const int stepPin = 3; //Y.STEP
const int dirPin = 6; // Y.DIR
const int enPin = 8;
const int HomingPin = 20;
const int HomingCommon = 21;
const float StepsPerDegree = 0.5555555556;
const int stepsPerRev = 200;
int pulseWidthMicros = 100; 	// microseconds
int millisBtwnSteps = 1000;
int angleNow = 0;
String stepdir = "cw";
float StepToAngle = 360/200;
bool stringComplete;
String inputString;

void step(String dir, int angle) {
  // handle stepper motor
  // takes in direction and angle in degrees and keep record of current angle
  int anglestep;
  if (dir == "cw") {
    digitalWrite(dirPin, HIGH);
    anglestep = 1;
    angleNow += anglestep;
  }
  if (dir == "ccw") {
    digitalWrite(dirPin, LOW);
    anglestep = -1;
    angleNow += anglestep;
  }
  for (int i = 0; i < angle; i++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(pulseWidthMicros);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(millisBtwnSteps);
  }
}

int StepmotorStep(int resolution=5) {
  // emergencystop
  // stop and go back few step
  int IsScanEdge;
//  if(digitalRead(HomingPin) == HIGH) {
//    raise StepperError('Angle Error');
//  }
  // set resolution
//  if (resolution == "fine") {
//    resolution = 1;  // == 1,8 degree
//  if (resolution == "coarse") {
//    resolution = 5;  // == 9 degree
//  }
  if (stepdir == "cw" && angleNow >= 125) {  // 225 d
    // if lidar scan range right edge (from lidar's perspective)
    Serial.println("CW bound");
    stepdir = "ccw";
    IsScanEdge = 1;  // "Right"
  } else if (stepdir == "ccw" && angleNow <= 75) {  // 135 d
    // if lidar scan range left edge
    Serial.println("CCW bound");
    stepdir = "cw";
    IsScanEdge = -1;  // "left"
  } else {
    IsScanEdge = 0;  // "Nan"
  }
  step(stepdir, resolution);
  return IsScanEdge;
}

void homing() {
  while (true) {
    // if homing switch pressed
    if(digitalRead(HomingPin) == HIGH) {
        angleNow = -25;  // 45 degree
        Serial.println("reset");
        delay(500);
        step("cw", 150);
        delay(1000);
        break;
    } else {
        step("ccw", 1);
    }
  }
}

void serialRead() {
  while(Serial.available()){
    char inChar = (char)Serial.read();
    inputString += inChar;
    if(inChar =='\n'){
      stringComplete = true;
    }
    else{
      stringComplete = false;
    }
  }
}

void setup() {
  Serial.begin(9600);
  pinMode(enPin, OUTPUT);
  digitalWrite(enPin, LOW);
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(finePin, INPUT);
  pinMode(coarsePin, INPUT);
}

void loop() {
  serialRead();
  if(stringComplete){
    if (stringComplete) {
      // Echo the received command back to the Raspberry Pi as an acknowledgment
      Serial.println("ACK: " + inputString);
      stringComplete = false; // Clear the input buffer
    }
  }
}
