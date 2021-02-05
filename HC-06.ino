#include <Wire.h> // Library for I2C communication
#include <LiquidCrystal_I2C.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>

#include <SoftwareSerial.h>
Servo myservo;
int pos = 90;
LiquidCrystal_I2C lcd = LiquidCrystal_I2C(0x27, 16, 2);
SoftwareSerial HC06(10, 11); //HC06-TX Pin 10, HC06-RX to Arduino Pin 11
String msg = ""; 

void setup() {
  HC06.begin(9600); //Baudrate 9600  
  Serial.begin(9600);
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  myservo.write(10);
  lcd.init();
  lcd.backlight();
  
  // Escribimos el Mensaje en el LCD.
  lcd.print("Lab Electronica.");
}

void loop() {
  if(HC06.available() > 0) //When HC06 receive something
  {
    String receive = HC06.readString(); //Read from Serial Communication
    Serial.println(receive);
   // delay(50);
    if(receive.length() >=3){
      lcd.clear();
      lcd.setCursor(0, 0);

      lcd.print("Verificacion");
      lcd.setCursor(2, 1);
      lcd.print(" Exitosa!");
      myservo.write(110);
      delay(2000);

      delay(100);
      myservo.write(10);
      delay(1000);
      lcd.clear();
      lcd.print("Lab Electronica.");
      receive = "";
    }
  }
}
