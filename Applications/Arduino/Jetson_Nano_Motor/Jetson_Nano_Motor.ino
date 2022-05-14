
#include <Wire.h>
#include <Adafruit_MotorShield.h>

Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

Adafruit_DCMotor *Motor1 = AFMS.getMotor(1);
Adafruit_DCMotor *Motor2 = AFMS.getMotor(2);
Adafruit_DCMotor *Motor3 = AFMS.getMotor(3);
Adafruit_DCMotor *Motor4 = AFMS.getMotor(4);

#define speedLimit 130
#define rightSpeeds 100
#define leftSpeeds 100

int defaultSpeed = 60;
int sidespeed = 60;
int speeds;
int rightSpeedPwm = 0;
int leftSpeedPwm = 0;

void setup() {

  AFMS.begin();
 // Motor1 -> setSpeed(defaultSpeed);
 // Motor2 -> setSpeed(defaultSpeed);
 // Motor3 -> setSpeed(defaultSpeed);
 // Motor4 -> setSpeed(defaultSpeed);

  Serial.begin(115200);
  while (!Serial) {
  }
}

void loop() {
   if (Serial.available() > 0)
    {
     speeds=Serial.parseInt();
   
     rightSpeedPwm = rightSpeeds + speeds;
     leftSpeedPwm = leftSpeeds - speeds;
     
     rightSpeedPwm = constrain(rightSpeedPwm, -speedLimit, speedLimit);
     leftSpeedPwm = constrain(leftSpeedPwm, -speedLimit, speedLimit);

     moveRobot(rightSpeedPwm, leftSpeedPwm);
     Serial.println(rightSpeedPwm);
     Serial.println(leftSpeedPwm); 
    }

  //SideLeft();
 // delay(1000);
  //SideRight();
 // delay(1000);
 // Release();
 // delay(2000);
  
  /*Forward();
  delay(1000);
  Backward();
  delay(1000);
  Release();
  delay(2000);

  RotateRight();
  delay(1000);
  RotateLeft();
  delay(1000);
  Release();
  delay(2000);*/
}

void moveRobot(int leftSpeed, int rightSpeed)
{
       if (leftSpeed > 0){
        Motor1 -> setSpeed(leftSpeed);
        Motor4 -> setSpeed(leftSpeed);
        Motor1 -> run(BACKWARD);
        Motor4 -> run(BACKWARD);
   
     }

     else {
        Motor1 -> setSpeed(leftSpeed);
        Motor4 -> setSpeed(leftSpeed);
        Motor1 -> run(FORWARD);
        Motor4 -> run(FORWARD);
     }

     if (rightSpeed > 0){
        Motor2 -> setSpeed(rightSpeed);
        Motor3 -> setSpeed(rightSpeed);
        Motor2 -> run(FORWARD);
        Motor3 -> run(FORWARD);  
        
     }

     else {
        Motor2 -> setSpeed(rightSpeed);
        Motor3 -> setSpeed(rightSpeed);
        Motor2 -> run(BACKWARD);
        Motor3 -> run(BACKWARD);
     }
     
}
void Backward(){
  Motor1 -> run(FORWARD);
  Motor2 -> run(BACKWARD);
  Motor3 -> run(BACKWARD);
  Motor4 -> run(FORWARD); 
}

void Forward(){
  Motor1 -> run(BACKWARD);
  Motor2 -> run(FORWARD);
  Motor3 -> run(FORWARD);
  Motor4 -> run(BACKWARD); 
}

void Release(){
  Motor1 -> run(RELEASE);
  Motor2 -> run(RELEASE);
  Motor3 -> run(RELEASE);
  Motor4 -> run(RELEASE); 
}

void RotateLeft() {
  Motor1 -> run(FORWARD);
  Motor2 -> run(FORWARD);
  Motor3 -> run(FORWARD);
  Motor4 -> run(FORWARD); 
}

void RotateRight() {
  Motor1 -> run(BACKWARD);
  Motor2 -> run(BACKWARD);
  Motor3 -> run(BACKWARD);
  Motor4 -> run(BACKWARD); 
}

void SideLeft() {
  Motor1 -> setSpeed(sidespeed);
  Motor2 -> setSpeed(sidespeed);
  Motor3 -> setSpeed(sidespeed);
  Motor4 -> setSpeed(sidespeed);
  
  Motor1 -> run(FORWARD);
  Motor2 -> run(FORWARD);
  Motor3 -> run(BACKWARD);
  Motor4 -> run(BACKWARD); 
  
}

void SideRight() {
  Motor1 -> setSpeed(sidespeed);
  Motor2 -> setSpeed(sidespeed);
  Motor3 -> setSpeed(sidespeed);
  Motor4 -> setSpeed(sidespeed);
  
  Motor1 -> run(BACKWARD);
  Motor2 -> run(BACKWARD);
  Motor3 -> run(FORWARD);
  Motor4 -> run(FORWARD); 
  
}
