#include "HX711.h"

#define CALIB_FACT -7050.0
#define LCDSERIAL Serial2

#define IGN 4
#define DAT 2
#define CLK 3

HX711 scale(DAT, CLK);

void clearLCD() {
  LCDSERIAL.write(254);  
  LCDSERIAL.write(128);
  
  LCDSERIAL.write("                ");
  LCDSERIAL.write("                ");
}

void writeFirstLCD(const char* input) {
  clearLCD();
  LCDSERIAL.write(input);
}

void writeSecondLCD(const char* input) {
  clearLCD();
  LCDSERIAL.write(254);  
  LCDSERIAL.write(192);
  LCDSERIAL.write(input);
}

float getLoad(int iters) {
  if (iters == 0) {
    return random(0,100);
  } else {
    int num = 0;
    for (int i=0; i<iters; i++)
      num += scale.get_units();
    return num /= iters;
  }
}

void setup() {
  pinMode(IGN,OUTPUT);
  digitalWrite(IGN,LOW);
  Serial.begin(9600);
  LCDSERIAL.begin(9600);
  scale.set_scale(CALIB_FACT);
  
  writeFirstLCD("Place engine and");
  writeSecondLCD("connect + zero.");
  
  Serial.flush();
  if (!Serial.available());
  scale.tare();
}

void loop() {
  if (Serial.available() > 0) {
    char incomingByte = Serial.read();
    if (incomingByte == 'i') digitalWrite(IGN,HIGH);
    else if (incomingByte == 'o') digitalWrite(IGN,LOW);
  }
  
  Serial.print(millis());
  Serial.print(",");
  Serial.print(getLoad(0));
  Serial.print("\n");
  
  writeFirstLCD("Running");
}

