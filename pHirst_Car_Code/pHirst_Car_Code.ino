#include <Wire.h>
#include "SparkFunBME280.h"

BME280 mySensor;
int potPin = A0;    // select the input pin for the potentiometer
int relayPin = 7;      // select the pin for the relay
int potValue = 0;  // variable to store the value coming from the potentiometer
bool onState = false;      // Car drives or not
int pressureValue = 0;   //the value read from the pressure sensor in Pa
float stoppingPressure = 800;    // assign the pressure that we want to stop the car at here

void setup() 
{
  Serial.begin(115200);

  //Pressure sensor setup--------------------------------------------  
  Wire.begin();
  Wire.setClock(400000); //Increase to fast I2C speed!
  mySensor.beginI2C();
  //  mySensor.setReferencePressure(101200); 
  //Adjust the sea level pressure used for altitude calculations
  //---------------------------------------------------------------

  //Relay setup-----------------------------------------------------
  pinMode(relayPin, OUTPUT);
  //----------------------------------------------------------------
}

void loop() 
{
  //read the value from the potentiometer---------------------------
  potValue = analogRead(potPin);
  //  Serial.print(sensorValue);
  //  Serial.print("\n");
  delay(100);
  //----------------------------------------------------------------
  
  // turn the car state on-----------------------------------------------
  //on when potentiometer >= 620
  if(potValue < 620){
    onState = false;
  }
  else {
    onState = true;
  }
  //-------------------------------------------------------------------

  //Test
  Serial.println("ON");
  delay(5000);
  onState = true;
  
  //Car operation with pressure sensor and motor---------------------
  while(onState) {
    //motor simulation
    Serial.println("vroom");
    pressureValue += 100;
    Serial.print(pressureValue);
    
    //Motor On/Relay On---------------------------------
    digitalWrite(relayPin, HIGH);
    //--------------------------------------------------
    
    //read Pressure Sensor------------------------------
    //pressureValue = mySensor.readFloatPressure();
    delay(100);
    //--------------------------------------------------

    //Stopping Mechanism--------------------------------
    if(pressureValue > stoppingPressure)
    {
      //test
      Serial.println("Car Off");
      
      //Motor Off/Relay Off-----------------------------
      digitalWrite(relayPin, LOW);
      //------------------------------------------------

      //Exit the On while loop
      onState = false;
    }
  }
}
