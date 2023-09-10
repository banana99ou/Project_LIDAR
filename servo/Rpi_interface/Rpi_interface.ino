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
int angleNow = 0;
int stepdir = 0;
float StepToAngle = 360/200;
bool stringComplete;
String inputString;
int i = 0;


void Step(int angle, int dir=1){
  // handle stepper motor
  // takes in angle in steps and go to that absolute position

  int e = angleNow - angle;
  if(e >= 0){
    dir = 0;
  }
  else if(e < 0){
    dir = 1;
  }
  Serial.println(angle);
  Serial.println(e);
  e = abs(e);

  int anglestep = 0;
  if(dir == 1){
    digitalWrite(dirPin, HIGH);
    anglestep = 1;
  }
  if(dir == 0){
    digitalWrite(dirPin, LOW);
    anglestep = -1;
  }

  if(e != 0){
    for(i=0; i<e; i++){
      digitalWrite(stepPin, HIGH);
      delayMicroseconds(pulseWidthMicros);
      digitalWrite(stepPin, LOW);
      delayMicroseconds(millisBtwnSteps);
      delay(100);
      angleNow += anglestep;
  
      if(angleNow>199){
        angleNow = 0;
      }
      if(angleNow<0){
        angleNow = 199;
      }
      Serial.println("AngleNow: " + String(angleNow));
      // time.sleep(0.1)
    }
  }

  Serial.println("Job Step finished");
  Serial.println("AngleNow: " + String(angleNow));
}

void Homing() {
  while(true){
    // if homing switch pressed
    if(digitalRead(limitSwitchPin1) == LOW){ 
      angleNow = 25; // 45 degree
      Serial.println(angleNow * StepToAngle);
      delay(0.5);
      // turn 180 clockwise to initialize lidar pos
      // then break
      // find way to use arduino as driver instead
      Step(125); // cw 180d
      // delay(1);
      break;
    }    
    // if homing switch not pressed
    else {
      // keep turning ccw until switch pressed
      // Serial.println("not there yet");
      Step(angleNow-1); //ccw 1.8d
    }
  }
  Serial.println("HomgComp");
}

void setup() {
  Serial.begin(9600);
  pinMode(limitSwitchPin1, INPUT_PULLUP);
  pinMode(limitSwitchPin2, INPUT_PULLUP);
  //Homing();
}

void loop() {
  if(digitalRead(limitSwitchPin1) == LOW || digitalRead(limitSwitchPin2) == LOW) {
    Serial.println("RaiseError");
    delay(100);  // Debounce delay
  }
  serialEvent();
  if(stringComplete) {
    Serial.println(inputString);
    if (spaceIndex1 != -1) {
      String directionValue = inputString.substring(spaceIndex1 + 1);
      int spaceIndex2 = directionValue.indexOf(' ');

      // Check if there's a second space (for the second parameter)
      if (spaceIndex2 != -1) {
        String directionStr = directionValue.substring(0, spaceIndex2);
        String amountStr = directionValue.substring(spaceIndex2 + 1);

        int direction = directionStr.toInt();
        int amount = amountStr.toInt();
        Step(direction, amount);
      } else {
        // If there's no second space, assume only one parameter
        int direction = directionValue.toInt();
        Step(direction);
      }
    }
    if(inputString.startsWith("Homing")) {
      Serial.println("Ack: Homing");
      delay(100);
      Homing();
    }
    if(inputString.startsWith("StepLoop")) {
      Serial.println("Ack: StepLoop");
      delay(100);
      //StepLoop();
    }
    
    inputString = "";
    stringComplete = false;
  }
  
}

void serialEvent() {
  while(Serial.available()){
    char inChar = (char)Serial.read();
    inputString += inChar;
    if(inChar == '\n') {
      stringComplete = true;
    }
  }
}
