#include <Servo.h>

#define PIN_SERVO 3

Servo s;

void setup() {
  s.attach(PIN_SERVO);
  s.write(0);
  Serial.begin(9600); // set the baud rate
  Serial.println("Ready"); // print "Ready" once
}

void loop() {
  char inByte = 0;
  char offset = 50;
  if(Serial.available()){ // only send data back if data has been sent
    char inByte = Serial.read(); // read the incoming data
    s.write(inByte+offset);
    Serial.println(inByte); // send the data back in a new line so that it is not all one long line
  }
  //delay(100); // delay for 1/10 of a second
}
