// Run a A4998 Stepstick from an Arduino UNO.
// Paul Hurley Aug 2015
#include <stdlib.h>
#include <Servo.h>

int x; 
#define BAUD (9600)

Servo s1;
Servo s2;

int limit1 = 13;
int limit2 = 3;
int limit3 = 4;
int limit4 = 5;

int step1Dir = 6;
int step1Step = 7;
int step2Dir = 8;
int step2Step = 9;

int enablePin = 10;

int servo1 = 11;
int servo2 = 12;

int startButton = 2;

boolean motorsOff = HIGH;


void setup() 
{
  Serial.begin(BAUD);
  pinMode(enablePin,OUTPUT); // Enable
  pinMode(step1Step,OUTPUT); // Step
  pinMode(step1Dir,OUTPUT); // Dir
  digitalWrite(enablePin,LOW); // Set Enable low
  
  pinMode(enablePin,OUTPUT); // Enable
  pinMode(step2Step,OUTPUT); // Step
  pinMode(step2Dir,OUTPUT); // Dir
  digitalWrite(10,LOW); // Set Enable low
  
  pinMode(limit1,INPUT); //Limit switch1
  pinMode(limit2,INPUT);
  pinMode(limit3,INPUT); 
  pinMode(limit4,INPUT); 
  
  s1.attach(servo1);
  s2.attach(servo2);
  
  pinMode(startButton,INPUT); //Start Button
  attachInterrupt(0,stopMotors, CHANGE);
  
  
  
}




boolean I = true;
float Xposition = 0.000;
float Yposition = 0.000;

String inputString = "";
boolean stringComplete = false;



// 300 steps = 2 in
// 150 steps = 1 in
int stepsPerX = 150;
int stepsPerY = 150;

float dropOff[] = {3.000,5.000};

void loop() {
  digitalWrite(enablePin,LOW);// Set Enable low

    if (I){
      Serial.println("INTIALIZING");
   initialize();
   I = false;
   posY(200);
 delay(1000);
 posX(200);
 
 Xposition = 300.000/stepsPerX;
 Yposition = 300.000/stepsPerY;
   
 }

 while(!stringComplete and !motorsOff ){
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
    if (command == '0'){ //GOTO
     String X = inputString.substring(2,7);
     String Y = inputString.substring(8,13);
     char floatbuf[32]; // make this at least big enough for the whole string
     X.toCharArray(floatbuf, 32);
      float x = atof(floatbuf);
     Y.toCharArray(floatbuf, 32);
      float y = atof(floatbuf);
   
      goTo(x,y,Xposition,Yposition);
      Xposition = x;
      Yposition = y;
      Serial.write("OK");

    }
    if (command == '1') { //Calibration
      initialize();
      Xposition = 100.0/stepsPerX;
      Yposition = 100.0/stepsPerY;
      Serial.write("OK");
    }
    
    if (command == '2') { //Pick up a Fish
      goFishing();
      Serial.write("OK");
    }
    
    if (command == '3') { // Deposit Fish
      goTo(dropOff[0],dropOff[1],Xposition,Yposition);
      Xposition = dropOff[0];
      Yposition = dropOff[1];
      goFishing();
      Serial.write("OK");
    }
    
    
  }
  inputString = "";
  stringComplete = false;
  Serial.flush();

  
}
//Serial.println("FINISHED THE GAME");
//}


// GOTO command
void goTo(float moveX,float moveY,float currX, float currY){
  int stepsX = (moveX - currX)*stepsPerX;
 int stepsY = (moveY - currY)*stepsPerY;
 
 
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

//Pick up a fish
void goFishing(){
   for(int ii = 20; ii <90; ii++){
    s1.write(ii);
    delay(5);
   }

  delay(1000);
  for(int ii = 90; ii >20; ii--){
    s1.write(ii);
    delay(10);
   }
  
};

void stopMotors(){
  motorsOff = !motorsOff;
  digitalWrite(enablePin,motorsOff);

}

void posX(int steps){
  digitalWrite(step1Dir,LOW); 
  digitalWrite(step2Dir,LOW);// Set Dir 
  for(x = 0; x < steps; x++) // Loop step times
  {
    digitalWrite(step1Step,HIGH); 
    digitalWrite(step2Step,HIGH);// Output high
    delay(1); // Wait
    digitalWrite(step1Step,LOW); 
    digitalWrite(step2Step,LOW);// Output low
    delay(1); // Wait
  } 
}

void negX(int steps){
  digitalWrite(step1Dir,HIGH); 
  digitalWrite(step2Dir,HIGH);// Set Dir high
  for(x = 0; x < steps; x++) // Loop step times
  {
    digitalWrite(step1Step,HIGH); 
    digitalWrite(step2Step,HIGH);// Output high
    delay(1); // Wait
    digitalWrite(step1Step,LOW); 
    digitalWrite(step2Step,LOW);// Output low
    delay(1); // Wait
  } 
}

void posY(int steps){
  digitalWrite(step1Dir,HIGH); 
  digitalWrite(step2Dir,LOW);// Set Dir high
  for(x = 0; x < steps; x++) // Loop step times
  {
    digitalWrite(step1Step,HIGH); 
    digitalWrite(step2Step,HIGH);// Output high
    delay(1); // Wait
    digitalWrite(step1Step,LOW); 
    digitalWrite(step2Step,LOW);// Output low
    delay(1); // Wait
  } 
}

void negY(int steps){
  digitalWrite(step1Dir,LOW); 
  digitalWrite(step2Dir,HIGH);// Set Dir high
  for(x = 0; x < steps; x++) // Loop step times
  {
    digitalWrite(step1Step,HIGH); 
    digitalWrite(step2Step,HIGH);// Output high
    delay(1); // Wait
    digitalWrite(step1Step,LOW); 
    digitalWrite(step2Step,LOW);// Output low
    delay(1); // Wait
  } 
}


//Initialization 
void initialize(){
  digitalWrite(step1Dir,HIGH); 
  digitalWrite(step2Dir,HIGH);// Set Dir high
  int i = 0;
  while(i==0){
    
    if(digitalRead(limit1)){
     
      digitalWrite(step1Step,HIGH); 
      digitalWrite(step2Step,HIGH);// Output high
      delay(1); // Wait
      digitalWrite(step1Step,LOW); 
      digitalWrite(step2Step,LOW);// Output low
      delay(1); // Wait
    }
    else{
     i=1;
   }
  
  }
  Serial.println("StOP");
  
  digitalWrite(step1Dir,LOW); 
  digitalWrite(step2Dir,LOW);// Set Dir high
  for(x = 0; x < 100; x++) // Loop step times
  {
    digitalWrite(step1Step,HIGH); 
    digitalWrite(step2Step,HIGH);// Output high
    delay(1); // Wait
    digitalWrite(step1Step,LOW); 
    digitalWrite(step2Step,LOW);// Output low
    delay(1); // Wait
    
  } 
  
  delay(1000);
  digitalWrite(step1Dir,LOW);
  digitalWrite(step2Dir,HIGH);
  i = 0;
  
  while(i == 0){
    
    if(digitalRead(limit2)){
      digitalWrite(step1Step,HIGH); 
      digitalWrite(step2Step,HIGH);// Output high
      delay(1); // Wait
      digitalWrite(step1Step,LOW); 
      digitalWrite(step2Step,LOW);// Output low
    }
    else{
     i = 1;
   }
  
  }
  Serial.println("StOP");
  
  digitalWrite(step1Dir,HIGH); 
  digitalWrite(step2Dir,LOW);// Set Dir high
  for(x = 0; x < 100; x++) // Loop step times
  {
    digitalWrite(step1Step,HIGH); 
    digitalWrite(step2Step,HIGH);// Output high
    delay(1); // Wait
    digitalWrite(step1Step,LOW); 
    digitalWrite(step2Step,LOW);// Output low
    delay(1); // Wait
    
  } 
  delay(1000);
  
};
