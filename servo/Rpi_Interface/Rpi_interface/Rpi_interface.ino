const int stepPin = 3;          // Change this to your actual pin
const int dirPin = 6;           // Change this to your actual pin
const int limitSwitchPin1 = 2;  // Change this to your first limit switch pin
const int limitSwitchPin2 = 5;  // Change this to your second limit switch pin
int finePin = 10;
int coarsePin = 11;
const int enPin = 8;
const float StepsPerDegree = 0.5555555556;
const int stepsPerRev = 200;
int pulseWidthMicros = 100;   // microseconds
int millisBtwnSteps = 1000;
int angleNow = 0;
String stepdir = "cw";
float StepToAngle = 360/200;
bool stringComplete;
String inputString;

void setup() {
  pinMode(limitSwitchPin1);
  pinMode(limitSwitchPin2);
  homing();
}

void loop() {
  if (digitalRead(limitSwitchPin1) == HIGH || digitalRead(limitSwitchPin2) == HIGH) {
    Serial.println("LimitSwitchPressed");
    delay(100);  // Debounce delay
  }

  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == 'M') {
      char direction = Serial.read();
      int angle = Serial.parseInt();
      StepmotorStep(angle)
    }
  }
}


void step(String dir, int angle){
  // handle stepper motor
  // takes in dirrection and angle in degrees and keep record of current angle
  if(dir == "cw"){
    digitalWrite(dirPin, HIGH);
    anglestep = 1;
  }
  if(dir == "ccw"){
    digitalWrite(dirPin, LOW);
    anglestep = -1;
  }
  for(i=0; i<angle; i++){
    digitalWrite(stepPin, HIGH);
    delayMicros(pulseWidthMicros);
    digitalWrite(stepPin, LOW);
    delayMillis(millisBtwnSteps);
    angleNow += anglestep
    // print(angleNow * StepToAngle)
    // time.sleep(0.1)
  }
}
    
int StepmotorStep(int resolution){ // , ifinit):
  // emergencystop
  // stop and go back few step
  String IsScanEdge = "Nan" 
  if(digitalRead(HomingPin)){
   raise StepperError('Angle Error')
  }
  // set resolution
  // if(resolution == "fine"){
  //   resolution = 1  // == 1,8 degree
  // }
  // if(resolution == "coarse"){
  //   resolution = 5  // == 9 degree
  // }
  if(stepdir == "cw" and angleNow >= -25){ // 225 d
    // if lidar scan range right edge (from lidar's perspective)
    print("CW bound")
    stepdir = "ccw"
    IsScanEdge = 1 // "Right"
  }
  elif(stepdir == "ccw" and angleNow <= 25){ // 135 d
    // if lidar scan range l{eft edge
    print("CCW bound")
    stepdir = "cw"
    IsScanEdge = -1 // "left"
  }
  else(){
    IsScanEdge = 0 // "Nan"
  // need to add a feature that ties scanning range to certain range
  // print("stepdir: ", stepdir)
  step(stepdir, resolution)
  return IsScanEdge
  }
}

void homing() {
  while True:
    // if homing switch pressed
    if(digitalRead(HomingPin) == true){ 
      angleNow = 75; // 45 degree
      //print(angleNow * StepToAngle)
      delay(0.5);
      // turn 180 clockwise to initialize lidar pos
      // then break
      // find way to use arduino as driver instead
      step("cw", 50);
      dealy(1);
      break;
    }    
    // if homing switch not pressed
    else(){
      // keep turning ccw until switch pressed
      step("ccw", 1)
    }
  Serial.println("HomgComp");
}
