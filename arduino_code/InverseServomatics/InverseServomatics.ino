#include <CustomTurret.h>
#include <CustomServo.h>
//Lucky comment

CustomServo baseServo(9,500,2500,0.3,0.95);
CustomServo armCloseServo(10,500,2500,0.27,0.55);
CustomServo armFarServo(11,500,2500,0.05,0.62);
CustomTurret customTurret(baseServo, armCloseServo, armFarServo);


void setup() {
  Serial.begin(115200);
  customTurret.setPos(0.5,0,1);
  customTurret.setup();
} 

void loop() {
  while (Serial.available() == 0) {}
  float baseServoPos = Serial.parseFloat();
  float armCloseServoPos = Serial.parseFloat();
  float armFarServoPos = Serial.parseFloat();

  customTurret.setPos(baseServoPos, armCloseServoPos, 1-armFarServoPos);
}
