#include "Arduino.h"
#include "CustomServo.h"
#include "CustomTurret.h"

CustomTurret::CustomTurret(CustomServo &base, CustomServo &armClose, CustomServo &armFar)
  : _base(base), _armClose(armClose), _armFar(armFar)
{
}

void CustomTurret::setPos(float basePos, float armClosePos, float armFarPos){
  _armFar.setRelPos(armFarPos);
  _base.setRelPos(basePos);
  _armClose.setRelPos(armClosePos);
}

void CustomTurret::setup(){
  _base.setup();
  _armClose.setup();
  _armFar.setup();
}