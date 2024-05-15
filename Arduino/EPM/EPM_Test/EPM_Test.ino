#include <Wire.h>
#include <Adafruit_MPL3115A2.h>
#include <DFRobot_sim808.h>

int cat = 3;
String dog = String(cat);
#define PHONE_NUMBER "+19033126656"  
#define MESSAGE dog

void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:
cat = hamster();
dog = String(cat);  
#define MESSAGE dog

}

int hamster()
{
  return 1;
}

