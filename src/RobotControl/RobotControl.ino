// Run a A4998 Stepstick from an Arduino UNO.
// Paul Hurley Aug 2015
#include <stdlib.h>
#include <Servo.h>

int x; 
#define BAUD (9600)

Servo s1;
Servo s2;

int limit1 = 13;
int limit2 = 4;
int limit3 = 3;
int limit4 = 5;

int step1Dir = 7;
int step1Step = 6;
int step2Dir = 10;
int step2Step = 9;

int enablePin = 8;

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
 
  
  pinMode(enablePin,OUTPUT); // Enable
  pinMode(step2Step,OUTPUT); // Step
  pinMode(step2Dir,OUTPUT); // Dir

  digitalWrite(enablePin,LOW); // Set Enable low
  pinMode(limit1,INPUT); //Limit switch1
  pinMode(limit2,INPUT);
  pinMode(limit3,INPUT); 
  pinMode(limit4,INPUT); 
  
  s1.attach(servo1);
  s2.attach(servo2);
  
  pinMode(startButton,INPUT_PULLUP); //Start Button
  attachInterrupt(0,stopMotors,LOW);
  
   s1.write(30);
  s2.write(70);
digitalWrite(enablePin,LOW);// Set Enable low


  
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

float dropOff[] = {4.500,4.000};
int fishHeight = 70;

void loop() {

//  if(I && digitalRead(startButton)){
//    initialize();
//      Xposition = 100.0/stepsPerX;
//      Yposition = 100.0/stepsPerY;
//     I = false; 
//   
//     goTo(4.500,4.500,Xposition,Yposition);
//      Xposition = x;
//      Yposition = y;
//  }
 



 while(!stringComplete && digitalRead(startButton)){
 if(Serial.available()){ // only send data back if data has been sent
    char inByte = Serial.read(); // read the incoming data
   
    
    if (inByte == '\n') {

      stringComplete = true;
       Serial.println(inputString); 
      Serial.flush();

    }
    if (inByte != '~')
    {
      inputString += inByte;
    }
    }

  }
  
  if(inputString != "" && digitalRead(startButton)){
    //Serial.println(inputString);
    char command = inputString[0];
    if (command == '0'){ //GOTO
      Serial.write("message_recieved");
      Serial.flush();
      //delay(10);
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
      delay(500);
      Serial.write("action_complete");
      Serial.flush();

    }
     if (command == '1') { //Calibration
     Serial.write("message_recieved");
     Serial.flush();
      //delay(10);
      initialize();
      Xposition = 100.0/stepsPerX;
      Yposition = 100.0/stepsPerY;
      Serial.write("action_complete");
      Serial.flush();
    }
    
     if (command == '2') { //Pick up a Fish
    //Serial.println("FISH");
    Serial.write("message_recieved");
    Serial.flush();
      goFishing();
     
      goTo(dropOff[0],dropOff[1],Xposition,Yposition);
      Xposition = dropOff[0];
      Yposition = dropOff[1];
      Serial.write("message_recieved");
      Serial.flush();
     // delay(10);
      //Serial.println("DROP OFF");
      
       for(int ii = 30; ii <100; ii++){
        s1.write(ii);
        delay(10);
       }
       
       for(int ii = 50; ii <100; ii++){
    s2.write(ii);
    delay(5);
   }
      s2.write(50);
        delay(1000);
      for(int ii = 100; ii >30; ii--){
        s1.write(ii);
        delay(30);
       }
       for(int ii = 50; ii <fishHeight; ii++){
    s2.write(ii);
    delay(5);
   }
      Serial.write("action_complete");
      Serial.flush();
 
    }
    
    if (command == '3') { // Deposit Fish
      goTo(dropOff[0],dropOff[1],Xposition,Yposition);
      Xposition = dropOff[0];
      Yposition = dropOff[1];
      Serial.write("message_recieved");
      Serial.flush();
     // delay(10);
      //Serial.println("DROP OFF");
      
       for(int ii = 30; ii <100; ii++){
        s1.write(ii);
        delay(10);
       }
       
       for(int ii = 50; ii <100; ii++){
    s2.write(ii);
    delay(5);
   }
      s2.write(50);
        delay(1000);
      for(int ii = 100; ii >30; ii--){
        s1.write(ii);
        delay(30);
       }
       for(int ii = 50; ii <fishHeight; ii++){
    s2.write(ii);
    delay(5);
   }
      Serial.write("action_complete");
      Serial.flush();
    }
//    else{
//     Serial.println("INVALID COMMAND");
//     inputString = "";
//    stringComplete = false;
//    Serial.flush();
//
//    }
    inputString = "";
  stringComplete = false;
  Serial.flush();
 // delay(100);
    
  }
//  inputString = "";
//  stringComplete = false;
//  Serial.flush();
//  delay(1000);

  
}



// GOTO command
void goTo(float moveX,float moveY,float currX, float currY){
  int stepsX = (moveX - currX)*stepsPerX;
 int stepsY = (moveY - currY)*stepsPerY;
 
 
 if (stepsX < 0){
  // Serial.print("MOVE negative X: ");
  // Serial.println(stepsX);
  negX(abs(stepsX));   
 }
 else if (stepsX > 0) {
  //  Serial.print("MOVE positive X: ");
  // Serial.println(stepsX);
  posX(stepsX); 
 }
 
  if (stepsY < 0){
   //  Serial.print("MOVE negative Y: ");
  // Serial.println(stepsY);
  negY(abs(stepsY));   
 }
 else if (stepsY > 0) {
 //  Serial.print("MOVE positive Y: ");
  // Serial.println(stepsY);
  posY(stepsY); 
 }
};

//Pick up a fish
void goFishing(){

  
   for(int ii = 60; ii <90; ii++){
    s2.write(ii);
    delay(50);
   }

  delay(1000);
  for(int ii = 90; ii >50; ii--){
    s2.write(ii);
    delay(10);
   }
  
  
};

void stopMotors(){
 // digitalWrite(enablePin,HIGH);


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
  s2.write(30);
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
  //Serial.println("StOP");
  
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
 // Serial.println("StOP");
  
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
