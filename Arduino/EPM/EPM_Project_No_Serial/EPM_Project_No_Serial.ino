#include <Wire.h>
#include <Adafruit_MPL3115A2.h>
#include <DFRobot_sim808.h>

#define PHONE_NUMBER "+19033126656"  

const int pinSwitch = 12;
int HourP = 30, HourC = 0, StatoSwitch = 0, count = 0, dayCount = 0, current = 0, past = 0;
float pascals, altm, tempC;
String GPSPart, TempPart, RainPart, message; 

DFRobot_SIM808 sim808(&Serial);

// Power by connecting Vin to 3-5V, GND to GND
// Uses I2C - connect SCL to the SCL pin, SDA to SDA pin
// See the Wire tutorial for pinouts for each Arduino
// http://arduino.cc/en/reference/wire
Adafruit_MPL3115A2 baro = Adafruit_MPL3115A2();

void setup() 
{
  //mySerial.begin(9600);
  Serial.begin(9600);
  Serial.println("Adafruit_MPL3115A2 test!");
  pinMode(pinSwitch, INPUT);

  //******** Initialize sim808 module *************
  while(!sim808.init()) 
  {
    delay(1000);
    Serial.print("Sim808 init error\r\n");
  }
  Serial.println("Sim808 init success");

  //************* Turn on the GPS power************
  if( sim808.attachGPS())
  {
    delay(100);
    while(!sim808.getGPS())
    {
      sim808.getGPS();
    }
  }
  else
  {
    delay(100);
//    #define MESSAGE "Initilization Failed"
//    sim808.sendSMS(PHONE_NUMBER,MESSAGE);
  }
}

void loop() 
{
  HourC = GetTime();
  if (HourP != HourC)
  {
    dayCount = dayCount+count;
    SendMessage();
    delay(1000);
    HourP = HourC;
    count = 0;
    if (HourC == 0)
    {
      dayCount = 0;
    }
  }
  StatoSwitch = digitalRead(pinSwitch);
  if (StatoSwitch == HIGH) 
  { 
    current = 1;
  } 
  if (StatoSwitch == LOW) 
  { 
    current = 0;
  } 
  if (current == 0)
  {
    if (past == 1)
    {
      count++;
      past = 0;
      delay(1000);
    }
  }
  if (current == 1)
  {
    if (past == 0)
    {
      past = 1;
    }
  }
}

void SendMessage()
{
  int hourRain = count*4;
  int dayRain = dayCount*4;
  RainPart = String(hourRain)+"in. last hour "+String(dayRain)+"in. today\n";
  TempPart = TempGague();
  GPSPart = GPSData();
  message = String(RainPart)+String(TempPart)+String(GPSPart);
  int Str_Len = message.length()+1;
  char char_array[Str_Len];
  message.toCharArray(char_array, Str_Len);
  delay(5000);
  
  #define MESSAGE char_array
  delay(100);
  sim808.sendSMS(PHONE_NUMBER,MESSAGE);
  delay(1000);
  return;
}

int GetTime()
{
  while(!sim808.getGPS())
  {
    sim808.getGPS();
  }
  
  int Time = sim808.GPSdata.hour;
  return Time;
}

String TempGague()
{
  //***************** Get Temp/Pressure/Alt *****************
  if (! baro.begin()) 
  {
    return;
  }
  
  pascals = baro.getPressure();
  // Our weather page presents pressure in Inches (Hg)
  // Use http://www.onlineconversion.com/pressure.htm for other units

  altm = baro.getAltitude();

  tempC = baro.getTemperature();

  delay(250);

  String TempReport = String(pascals/3377)+" Inches (Hg)\n"+String(altm)+" meters\n"+String(tempC)+"*C\n";

  return TempReport;
}

String GPSData()
{
  //************** Get GPS data *******************
//  if (sim808.getGPS()) 
//  {
    
    String GPSReport = String(sim808.GPSdata.lat,6)+"*N "+String(sim808.GPSdata.lon,6)+"*W\n";

    return GPSReport;
//  }
}

