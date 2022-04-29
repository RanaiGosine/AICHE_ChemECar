const int BUTTON = 4; // Naming switch button pin
//const int LED = 3;   // Namin LED pin
int BUTTONstate = 0; // A variable to store Button Status / Input

void setup(){ 
  Serial.begin(115200);
  
  //pinMode(LED, OUTPUT);
  pinMode (BUTTON, INPUT);
 }
 
void loop() {
  BUTTONstate = digitalRead(BUTTON);  // Reading button status / input
  if (BUTTONstate == HIGH)  // Condition to check button input
    {
      //digitalWrite(LED, HIGH);
      Serial.println("On");
    }
    else
    {
      //digitalWrite(LED, LOW);
      Serial.println("Off");
    }
}
