#include <Servo.h>

#define PIN_SERVO_1 3
#define PIN_SERVO_2 11


Servo s1;
Servo s2;
char control[2] = {0, 0};
char inByte = 0;
char offset1 = 50;
char offset2 = 50;

  
char prevInByte = '~';
void setup() {
  s1.attach(PIN_SERVO_1);
  s2.attach(PIN_SERVO_2);
  s1.write(0);
  s2.write(0);
  Serial.begin(9600); // set the baud rate
  Serial.println("Ready"); // print "Ready" once
  delay(1000);
}

void loop() {
  if(Serial.available()){ // only send data back if data has been sent
    char inByte = Serial.read(); // read the incoming data
    //Serial.println(inByte);
    if(prevInByte == '~'){
      control[0] = inByte;
    }
    else if(prevInByte == '$'){
      control[1] = inByte;
    }
    prevInByte = inByte;
    //Serial.println(control[1]);
    s1.write(control[0]+offset1);
    s2.write(control[1]+offset2);
  }
  //s2.write(100);
  //s1.write(control[0]+offset1);
  
  
  //delay(100); // delay for 1/10 of a second
}
