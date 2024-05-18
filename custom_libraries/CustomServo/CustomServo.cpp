#include "Arduino.h"
#include "Servo.h"
#include "CustomServo.h"

CustomServo::CustomServo(int pin, int minMicroseconds, int maxMicroseconds, float minPos, float maxPos){
  _pin = pin;
  _minMicroseconds = minMicroseconds;
  _maxMicroseconds = maxMicroseconds;
  _minPos = minPos;
  _maxPos = maxPos;
}

void CustomServo::setPos(float pos){ //Maybe make a relative set pos later on which takes the limits into account when setting position
  pos = min(max(_minPos,pos),_maxPos);
  int val = (_maxMicroseconds-_minMicroseconds)*pos + _minMicroseconds;
  //Serial.print(val);
  _servo.writeMicroseconds(val);
}

void CustomServo::setRelPos(float pos){
  pos = min(max(0,pos),1);
  pos = _minPos + (_maxPos-_minPos)*pos;
  int val = (_maxMicroseconds-_minMicroseconds)*pos + _minMicroseconds;
  _servo.writeMicroseconds(val);
}

void CustomServo::setup(){
  //Set servo default pos here something like (0,0.25,0.5)
  _servo.attach(_pin,_minMicroseconds,_maxMicroseconds);
}

void CustomServo::sweep(){
  for (float i = 0; i <= 1; i+=0.05){
    CustomServo::setPos(i);
    delay(150);
  }

  for (float i = 1; i >= 0; i-=0.05){
    CustomServo::setPos(i);
    delay(150);
  }
}