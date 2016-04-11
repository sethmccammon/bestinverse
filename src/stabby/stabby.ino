#include <Servo.h>

#define PIN_SERVO_1 3 //fishing servo
#define PIN_SERVO_2 11 //rotation servo
#define PIN_BUTTON 4

Servo s1;
Servo s2;

char locs[2] = {-1, -1};
void stab();

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); // set the baud rate
  pinMode(PIN_BUTTON, INPUT);
  s1.attach(PIN_SERVO_1);
  s2.attach(PIN_SERVO_2);
  s1.write(20);
  s2.write(10);
  Serial.println("Ready"); // print "Ready" once
  
  delay(1000);
}

void loop() {
  stab();
//  int button_val = digitalRead(PIN_BUTTON);
//  Serial.println(button_val);
//  if(button_val){
//    stab();
//  }
  // put your main code here, to run repeatedly:
  delay(100);
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

