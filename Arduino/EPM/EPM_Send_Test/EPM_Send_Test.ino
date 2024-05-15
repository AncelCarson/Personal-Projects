#include <DFRobot_sim808.h>

int cat = 10;
String dog = String(cat);
#define PHONE_NUMBER "+19033126656"  
//#define MESSAGE "Dog"
//#define MESSAGE dog
//#define MESSAGE String(30)

DFRobot_SIM808 sim808(&Serial);

void setup() {
  // put your setup code here, to run once:
//sim808.sendSMS(PHONE_NUMBER,MESSAGE);
sim808.sendSMS(PHONE_NUMBER,"30");
}

void loop() {
  // put your main code here, to run repeatedly:

}
