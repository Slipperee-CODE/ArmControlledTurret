#ifndef CustomServo_h
#define CustomServo_h

#include "Arduino.h"
#include "Servo.h"

class CustomServo {
  public:
    CustomServo(int pin, int minMicroseconds, int maxMicroseconds, float minPos, float maxPos);
    void setPos(float pos);
    void setRelPos(float pos);
    void setup();
    void sweep();
  private:
    Servo _servo;
    int _pin;
    int _minMicroseconds;
    int _maxMicroseconds;
    float _minPos;
    float _maxPos;
};
#endif