#include <Wire.h>
#include <Adafruit_MPL3115A2.h>
#include <DFRobot_sim808.h>

String dog = "test";
#define PHONE_NUMBER "+19033126656"  
#define MESSAGE String(dog)

const int pinSwitch = 12;
int HourP = 0, HourC = 0, StatoSwitch = 0, count = 0, current = 0, past = 0;
float pascals, altm, tempC;
String GPSPart, TempPart, message; 

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
    Serial.println("Open the GPS power success");
    DataReport();
  }
  else
  {
    Serial.println("Open the GPS power failure");
    return;
  }
//  sim808.sendSMS(PHONE_NUMBER,MESSAGE);
}

void loop() 
{
  if (HourP < HourC)
  {
    DataReport();
    HourP = HourC;
//    sim808.sendSMS(PHONE_NUMBER,MESSAGE);
  }
  HourC = sim808.GPSdata.hour;
  Ticker();
  TempGague();
  GPSPart = GPSData();
  Serial.print(GPSPart);
  delay (20000);
}

void DataReport()
{
//  String temp = WritenReport();
//  message = String(temp);
//  #define MESSAGE message
//  sim808.sendSMS(PHONE_NUMBER,MESSAGE);
}

String WritenReport()
{
  String Msg;
  GPSPart = GPSData();
  GPSData();
  TempPart = TempGague();
  TempGague();
  Msg = GPSPart+TempPart;
  return Msg;
}

String GPSData()
{
  //************** Get GPS data *******************
  if (sim808.getGPS()) 
  {
    Serial.print(sim808.GPSdata.year);
    Serial.print("/");
    Serial.print(sim808.GPSdata.month);
    Serial.print("/");
    Serial.print(sim808.GPSdata.day);
    Serial.print(" ");
    Serial.print(sim808.GPSdata.hour);
    Serial.print(":");
    Serial.print(sim808.GPSdata.minute);
    Serial.print(":");
    Serial.print(sim808.GPSdata.second);
    Serial.print(":");
    Serial.println(sim808.GPSdata.centisecond);
    Serial.print("latitude :");
    Serial.println(sim808.GPSdata.lat);
    Serial.print("longitude :");
    Serial.println(sim808.GPSdata.lon);
    Serial.print("speed_kph :");
    Serial.println(sim808.GPSdata.speed_kph);
    Serial.print("heading :");
    Serial.println(sim808.GPSdata.heading);
    Serial.println();
    
    String GPSReport = String(sim808.GPSdata.lat)+"*N "+String(sim808.GPSdata.lon)+"*W\n";
//    #define MESSAGE GPSReport

    return GPSReport;
  }
}

String TempGague()
{
  //***************** Get Temp/Pressure/Alt *****************
  if (! baro.begin()) 
  {
    Serial.println("Couldnt find sensor");
    return;
  }
  
  pascals = baro.getPressure();
  // Our weather page presents pressure in Inches (Hg)
  // Use http://www.onlineconversion.com/pressure.htm for other units
  Serial.print(pascals/3377); Serial.println(" Inches (Hg)");

  altm = baro.getAltitude();
  Serial.print(altm); Serial.println(" meters");

  tempC = baro.getTemperature();
  Serial.print(tempC); Serial.println("*C");

  delay(250);

  String TempReport = String(pascals/3377)+" Inches (Hg)\n"+String(altm)+" meters\n"+String(tempC)+"*C\n";
//  #define MESSAGE TempReport

  return TempReport;
}

void Ticker() 
{ 
  StatoSwitch = digitalRead(pinSwitch); //Leggo il valore del Reed 
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
  Serial.println(count);
}
