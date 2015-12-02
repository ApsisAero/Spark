#include "HX711.h"
#include <SoftwareSerial.h>

#define CALIB_FACT 432
#define txPin 0

#define IGN 4
#define DAT 2
#define CLK 3

HX711 scale(DAT, CLK);
SoftwareSerial LCD = SoftwareSerial(0, txPin);
const int LCDdelay=10;

void lcdPosition(int row, int col) {
  LCD.write(0xFE);
  LCD.write((col + row*64 + 128));
  delay(LCDdelay);
}
void clearLCD(){
  LCD.write(0xFE);
  LCD.write(0x01);
  delay(LCDdelay);
}
void backlightOn() {
  LCD.write(0x7C);
  LCD.write(157);
  delay(LCDdelay);
}
void backlightOff(){
  LCD.write(0x7C);
  LCD.write(128);
   delay(LCDdelay);
}
void serCommand(){
  LCD.write(0xFE);
}

int getLoad(int iters) {
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
  pinMode(txPin, OUTPUT);
  LCD.begin(9600);
  scale.set_scale(CALIB_FACT);
  
  delay(1500);
  clearLCD();
  lcdPosition(0,0);
  LCD.print("Remove engine and");
  lcdPosition(1,0);
  LCD.print("connect via USB.");
}

void loop() {
  if (Serial.available() > 0) {
    char incomingByte = Serial.read();
    if (incomingByte == 'i') {
      digitalWrite(IGN,HIGH);
      clearLCD();
      lcdPosition(0,0);
      LCD.print("Igniter live.");
      lcdPosition(1,0);
      LCD.print("Recording data.");
    } else if (incomingByte == 'o') {
      digitalWrite(IGN,LOW);
      clearLCD();
      lcdPosition(0,0);
      LCD.print("Igniter cold.");
      lcdPosition(1,0);
      LCD.print("Data saved.");
    } else if (incomingByte == 'c') {
      clearLCD();
      lcdPosition(0,0);
      LCD.print("Connected to");
      lcdPosition(1,0);
      LCD.print("control.");
      scale.tare();
    } else if (incomingByte == 'y') {
      clearLCD();
      lcdPosition(0,0);
      LCD.print("Zeroing the");
      lcdPosition(1,0);
      LCD.print("load cell...");
    } else if (incomingByte == 'z') {
      clearLCD();
      lcdPosition(0,0);
      LCD.print("Zero successful.");
      lcdPosition(1,0);
      LCD.print("Ready to launch.");
    }
  }

  int load = getLoad(1);
  const int n = snprintf(NULL, 0, "%d", load);
  char buf[n+1];
  int c = snprintf(buf, n+1, "%d", load);

  
  Serial.print(millis());
  Serial.print(",");
  Serial.println(load);
  delay(10);
}
