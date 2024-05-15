const int pinSwitch = 12; //Pin Reed 
const int pinLed = 9; //Pin LED 
int StatoSwitch = 0, count = 0, current = 0, past = 0; 

void setup() 
{ 
  pinMode(pinSwitch, INPUT);
  Serial.begin(9600);
} 

void loop() 
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
