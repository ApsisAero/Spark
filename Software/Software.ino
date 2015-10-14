#include "HX711.h"

#define CALIB_FACT -7050.0
#define LCDSERIAL Serial2

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

void setIgnite(bool on) {

}

void setup() {
  Serial.begin(9600);
  LCDSERIAL.begin(9600);
  scale.set_scale(CALIB_FACT);
  
  writeFirstLCD("Place engine and");
  writeSecondLCD("connect + zero.");
  
  Serial.flush();
  
  scale.tare();
}

void loop() {
  if (Serial.available() > 0) {
    char incomingByte = Serial.read();
    if (incomingByte == 'i') setIgnite(true);
    else if (incomingByte == 'o') setIgnite(false);
  }
  
  Serial.print(millis());
  Serial.print(",");
  Serial.print(scale.get_units());
  Serial.print("\n");
}

