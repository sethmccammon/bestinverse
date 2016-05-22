// Run a A4998 Stepstick from an Arduino UNO.
// Paul Hurley Aug 2015
#include <stdlib.h>
#include <Servo.h>

int x; 
#define BAUD (9600)

Servo s1;
Servo s2;

void setup() 
{
  Serial.begin(BAUD);
  pinMode(6,OUTPUT); // Enable
  pinMode(5,OUTPUT); // Step
  pinMode(4,OUTPUT); // Dir
  digitalWrite(6,LOW); // Set Enable low
  
  pinMode(10,OUTPUT); // Enable
  pinMode(9,OUTPUT); // Step
  pinMode(8,OUTPUT); // Dir
  digitalWrite(10,LOW); // Set Enable low
  
  pinMode(2,INPUT); //Limit switch1
  pinMode(12,INPUT);
  pinMode(13,INPUT); 
  
  attachInterrupt(2,stopMotors,HIGH);
  s1.attach(12);
  s2.attach(13);
  
  
  
}

void stopMotors(){
  Serial.println("STOP");
}

void posX(int steps){
  digitalWrite(4,LOW); 
  digitalWrite(8,LOW);// Set Dir high
  for(x = 0; x < steps; x++) // Loop step times
  {
    digitalWrite(5,HIGH); 
    digitalWrite(9,HIGH);// Output high
    delay(1); // Wait
    digitalWrite(5,LOW); 
    digitalWrite(9,LOW);// Output low
    delay(1); // Wait
  } 
}

void negX(int steps){
  digitalWrite(4,HIGH); 
  digitalWrite(8,HIGH);// Set Dir high
  for(x = 0; x < steps; x++) // Loop step times
  {
    digitalWrite(5,HIGH); 
    digitalWrite(9,HIGH);// Output high
    delay(1); // Wait
    digitalWrite(5,LOW); 
    digitalWrite(9,LOW);// Output low
    delay(1); // Wait
  } 
}

void posY(int steps){
  digitalWrite(4,HIGH); 
  digitalWrite(8,LOW);// Set Dir high
  for(x = 0; x < steps; x++) // Loop step times
  {
    digitalWrite(5,HIGH); 
    digitalWrite(9,HIGH);// Output high
    delay(1); // Wait
    digitalWrite(5,LOW); 
    digitalWrite(9,LOW);// Output low
    delay(1); // Wait
  } 
}

void negY(int steps){
  digitalWrite(4,LOW); 
  digitalWrite(8,HIGH);// Set Dir high
  for(x = 0; x < steps; x++) // Loop step times
  {
    digitalWrite(5,HIGH); 
    digitalWrite(9,HIGH);// Output high
    delay(1); // Wait
    digitalWrite(5,LOW); 
    digitalWrite(9,LOW);// Output low
    delay(1); // Wait
  } 
}

void initialize(){
  digitalWrite(4,HIGH); 
  digitalWrite(8,HIGH);// Set Dir high
  int i = 0;
  while(i==0){
    
    if(digitalRead(2)){
     
      digitalWrite(5,HIGH); 
      digitalWrite(9,HIGH);// Output high
      delay(1); // Wait
      digitalWrite(5,LOW); 
      digitalWrite(9,LOW);// Output low
      delay(1); // Wait
    }
    else{
     i=1;
   }
  
  }
  Serial.println("StOP");
  
  digitalWrite(4,LOW); 
  digitalWrite(8,LOW);// Set Dir high
  for(x = 0; x < 100; x++) // Loop step times
  {
    digitalWrite(5,HIGH); 
    digitalWrite(9,HIGH);// Output high
    delay(1); // Wait
    digitalWrite(5,LOW); 
    digitalWrite(9,LOW);// Output low
    delay(1); // Wait
    
  } 
  
  delay(1000);
  digitalWrite(4,LOW);
  digitalWrite(8,HIGH);
  i = 0;
  
  while(i == 0){
    
    if(digitalRead(11)){
      digitalWrite(5,HIGH); 
      digitalWrite(9,HIGH);// Output high
      delay(1); // Wait
      digitalWrite(5,LOW); 
      digitalWrite(9,LOW);// Output low
      delay(1); // Wait
    }
    else{
     i = 1;
   }
  
  }
  Serial.println("StOP");
  
  digitalWrite(4,HIGH); 
  digitalWrite(8,LOW);// Set Dir high
  for(x = 0; x < 100; x++) // Loop step times
  {
    digitalWrite(5,HIGH); 
    digitalWrite(9,HIGH);// Output high
    delay(1); // Wait
    digitalWrite(5,LOW); 
    digitalWrite(9,LOW);// Output low
    delay(1); // Wait
    
  } 
  delay(1000);
  
}


boolean I = true;
float Xposition = 0.000;
float Yposition = 0.000;

String inputString = "";
boolean stringComplete = false;



// 300 steps = 2 in
// 150 steps = 1 in

void loop() {
  digitalWrite(6,LOW); 
  digitalWrite(10,LOW);// Set Enable low

    if (I){
      Serial.println("INTIALIZING");
   initialize();
   I = false;
   posY(200);
 delay(1000);
 posX(200);
 
 Xposition = 2.000;
 Yposition = 2.000;
 
 
 
 
   
 }
 while(!stringComplete){
 if(Serial.available()){ // only send data back if data has been sent
    char inByte = Serial.read(); // read the incoming data
    
    
    if (inByte == '~') {
      inByte = ' ';
      inputString += inByte;
      stringComplete = true; 
    }
    
    inputString += inByte;
    }

  }
  if(inputString != ""){
    Serial.println(inputString);
    char command = inputString[0];
    if (command == '0'){
     String X = inputString.substring(2,7);
     String Y = inputString.substring(8,13);
     char floatbuf[32]; // make this at least big enough for the whole string
     X.toCharArray(floatbuf, 32);
      float x = atof(floatbuf);
     Y.toCharArray(floatbuf, 32);
      float y = atof(floatbuf);
      Serial.write("OK");
      
      goTo(x,y,Xposition,Yposition);
      Xposition = x;
      Yposition = y;

    }
  }
  inputString = "";
  stringComplete = false;
  Serial.flush();

  
}

void goTo(float moveX,float moveY,float currX, float currY){
  int stepsX = (moveX - currX)*150;
 int stepsY = (moveY - currY)*150;
 
 
 if (stepsX < 0){
   Serial.print("MOVE negative X: ");
   Serial.println(stepsX);
  negX(stepsX);   
 }
 else if (stepsX > 0) {
    Serial.print("MOVE positive X: ");
   Serial.println(stepsX);
  posX(stepsX); 
 }
 
  if (stepsY < 0){
     Serial.print("MOVE negative Y: ");
   Serial.println(stepsY);
  negY(stepsY);   
 }
 else if (stepsY > 0) {
   Serial.print("MOVE positive Y: ");
   Serial.println(stepsY);
  posY(stepsY); 
 }
};
