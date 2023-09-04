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


void Step(int dir, int angle){
  // handle stepper motor
  // takes in dirrection and angle in degrees and keep record of current angle
  // Serial.print(dir);
  // Serial.print(' ');
  // Serial.println(angle);
  int anglestep = 0;
  if(dir == 1){
    digitalWrite(dirPin, HIGH);
    anglestep = 1;
  }
  if(dir == 0){
    digitalWrite(dirPin, LOW);
    anglestep = -1;
  }
  for(i=0; i<angle; i++){
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(pulseWidthMicros);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(millisBtwnSteps);
    delayMicroseconds(100000);
    angleNow += anglestep;

    if(angleNow>199){
      angleNow = 0;
    }
    if(angleNow<0){
      angleNow = 199;
    }
    // Serial.println("AngleNow: " + String(angleNow));
    // time.sleep(0.1)
  }
}
    
int StepLoop(int resolution=3){ // , ifinit):
  // emergencystop
  // stop and go back few step
  int IsScanEdge = 0 ;
  if(digitalRead(limitSwitchPin1) == true){
//   /raise StepperError('Angle Error');
  }
  // set resolution
  // if(resolution == "fine"){
  //   resolution = 1  // == 1,8 degree
  // }
  // if(resolution == "coarse"){
  //   resolution = 5  // == 9 degree
  // }
  if(stepdir == 1 and angleNow >= -25){ // 225 d
    // if lidar scan range right edge (from lidar's perspective)
    Serial.println("CW bound");
    stepdir = 0; //ccw
    IsScanEdge = 1; // "Right"
  }
  else if(stepdir == 0 and angleNow <= 25){ // 135 d
    // if lidar scan range l{eft edge
    Serial.println("CCW bound");
    stepdir = 1; // "cw"
    IsScanEdge = -1; // "left"
  }
  else {
    IsScanEdge = 0; // "Nan"
    // need to add a feature that ties scanning range to certain range
    // print("stepdir: ", stepdir)
    Step(stepdir, resolution);
    return IsScanEdge;
  }
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
      Step(1, 100); // cw 180d
      // delay(1);
      break;
    }    
    // if homing switch not pressed
    else {
      // keep turning ccw until switch pressed
      // Serial.println("not there yet");
      Step(0, 1); //ccw 1.8d
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
    if(inputString.startsWith("Step")) {
      Serial.println("Ack: Step");
      delay(100);
      int spaceIndex = inputString.indexOf(' ');
      if(spaceIndex != -1){
        String value = inputString.substring(spaceIndex + 1);
        int direction = value.charAt(0) - '0';
        int amount = value.substring(1).toInt();
        Step(direction, amount);
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
