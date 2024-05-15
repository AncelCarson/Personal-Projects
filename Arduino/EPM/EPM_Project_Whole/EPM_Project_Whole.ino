#include <Wire.h>
#include <Adafruit_MPL3115A2.h>
#include <DFRobot_sim808.h>

#define PHONE_NUMBER "+19033126656"  
#define MESSAGE "Test Pass"
#define MESSAGE_LENGTH 160
char message[MESSAGE_LENGTH];
int messageIndex = 0, HourP = 0, HourC = 0;

char phone[16];
char datetime[24];

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
  }
  else
  {
    Serial.println("Open the GPS power failure");
  }
  GPSData();
  TempGague();
//  sim808.sendSMS(PHONE_NUMBER,MESSAGE);
}

void loop() 
{
  messageIndex = sim808.isSMSunread();
  Serial.print("messageIndex: ");
  Serial.println(messageIndex);
  if (messageIndex > 0) 
  {
    sim808.readSMS(messageIndex, message, MESSAGE_LENGTH, phone, datetime);

    //***********In order not to full SIM Memory, is better to delete it**********
    if (message == "Report")
    {
//      DataCall();
    }
    sim808.deleteSMS(messageIndex);  
  }
  if (HourP < HourC)
  {
//    DataReport();
    HourP = HourC;
  }
  HourC = sim808.GPSdata.hour;
}

void DataCall()
{
  #define MESSAGE " "
  sim808.sendSMS(phone,MESSAGE);
}

void DataReport()
{
  #define MESSAGE " "
  sim808.sendSMS(PHONE_NUMBER,MESSAGE);
}

void WritenReport()
{
  GPSData();
  TempGague();
}

void GPSData()
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

    //************* Turn off the GPS power ************
    sim808.detachGPS();
  }
  else
  {
    Serial.print("GPS load fail\n");
  }
}

void TempGague()
{
  //***************** Get Temp/Pressure/Alt *****************
  if (! baro.begin()) 
  {
    Serial.println("Couldnt find sensor");
    return;
  }
  
  float pascals = baro.getPressure();
  // Our weather page presents pressure in Inches (Hg)
  // Use http://www.onlineconversion.com/pressure.htm for other units
  Serial.print(pascals/3377); Serial.println(" Inches (Hg)");

  float altm = baro.getAltitude();
  Serial.print(altm); Serial.println(" meters");

  float tempC = baro.getTemperature();
  Serial.print(tempC); Serial.println("*C");

  delay(250);
}
