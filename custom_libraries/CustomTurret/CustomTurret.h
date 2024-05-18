#ifndef CustomTurret_h
#define CustomTurret_h

#include "Arduino.h"
#include "CustomServo.h"
#include "Servo.h"

class CustomTurret {
  public:
    CustomTurret(CustomServo &base, CustomServo &armClose, CustomServo &armFar);
    void setPos(float x, float y, float z);
    void setup();
  private:
    CustomServo _base;
    CustomServo _armClose;
    CustomServo _armFar;
};
#endif