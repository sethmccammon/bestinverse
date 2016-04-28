#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
#include <Servo.h>

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
// Or, create it with a different I2C address (say for stacking)
// Adafruit_MotorShield AFMS = Adafruit_MotorShield(0x61); 

// Connect a stepper motor with 200 steps per revolution (1.8 degree)
// to motor port #2 (M3 and M4)
Adafruit_StepperMotor *myMotor1 = AFMS.getStepper(200, 1);
Adafruit_StepperMotor *myMotor2 = AFMS.getStepper(200, 2);

Servo s1;

char x_dir = 0;
char y_dir = 0;
char fish  = 0;
char inByte = 0;
char prevInByte = '~';


void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps
  Serial.println("Stepper test!");

  AFMS.begin();  // create with the default frequency 1.6KHz
  //AFMS.begin(1000);  // OR with a different frequency, say 1KHz
  
  myMotor1->setSpeed(10);  // 10 rpm   
  myMotor2->setSpeed(10);  // 10 rpm  
  
  // Attach a servo to pin #10
  s1.attach(10);
}

void loop() {
  if(Serial.available()){ // only send data back if data has been sent
    char inByte = Serial.read(); // read the incoming data
    if(prevInByte == '~'){
      x_dir = inByte;
    }
    else if(prevInByte == '$'){
      y_dir = inByte;
    }
    else if(prevInByte == '%'){
      fish = inByte;
    }
    prevInByte = inByte;
    //Serial.println(control[1]);
  }
  else{
    x_dir = 0;
    y_dir = 0;
    fish = 0;
  }
  //x control
  if( x_dir == 1){
    Serial.println("Forward x");
    myMotor1->step(1, FORWARD, SINGLE); 
    x_dir = 0;
  }
  else if(x_dir == -1 ){
    Serial.println("Backward x");
    myMotor1->step(1, BACKWARD, SINGLE);
    x_dir = 0;
  }
  //y contorl
    if( y_dir == 1){
      Serial.println("Forward y");
    myMotor2->step(1, FORWARD, SINGLE); 
    y_dir = 0;
  }
  else if(y_dir == -1 ){
    Serial.println("Backward y");
    myMotor2->step(1, BACKWARD, SINGLE);
    y_dir = 0;
  }
  if (fish == 1) {
    Serial.println("FISH!!!");
    stab();
    fish = 0;
  }
  


   
}

void stab() {
  for(int ii = 20; ii <90; ii++){
    s1.write(ii);
    delay(5);
   }

  delay(1000);
  for(int ii = 90; ii >20; ii--){
    s1.write(ii);
    delay(10);
   }

}
