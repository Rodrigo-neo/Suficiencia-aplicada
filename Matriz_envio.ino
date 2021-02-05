#include <Key.h>
#include <Keypad.h>
#include <SoftwareSerial.h>   // Incluimos la librería  SoftwareSerial  
SoftwareSerial BT(10,11);    // Definimos los pines RX y TX del Arduino conectados al Bluetooth
String mensaje = "";
const byte rowsCount = 4;
const byte columsCount = 4;
const char*envio= "";
String dato = "";
int conteo = 0;
String accion;

char keys[rowsCount][columsCount] = {
   { '1','2','3', 'A' },
   { '4','5','6', 'B' },
   { '7','8','9', 'C' },
   { '#','0','*', 'D' }
};
 
const byte rowPins[rowsCount] = { 4, 5, 6, 7 };
const byte columnPins[columsCount] = { 8, 9, 12, 13 };
 
Keypad keypad = Keypad(makeKeymap(keys), rowPins, columnPins, rowsCount, columsCount);
 
void setup() {
   BT.begin(9600);       // Inicializamos el puerto serie BT (Para Modo AT 2)
   Serial.begin(9600);
}
 
void loop() {
  
  if (Serial.available()){
    accion = Serial.readString();  
    //Serial.print(accion.length());

  }
  if (accion.length() == 3 ){
    while (conteo == 0){
      char key = keypad.getKey();
      if (key) {
        //Serial.println(key);
        mensaje.concat(key);
        }
      if (mensaje.length()== 6){
        Serial.println(mensaje);
        conteo = 1;
        }
       }
      if (conteo == 1){
        mensaje = "";
        conteo =0;
        accion = "";
   }
   }
   else if (accion.length() == 2){
      char key = keypad.getKey();
      if (key) {
        Serial.println(key);
        
       }
   }
   else if (accion.length() == 4){
    dato = Serial.readString();
    int len = dato.length() + 1;
    char char_array[len];
    dato.toCharArray(char_array,len);
    envio = char_array;
    BT.print(envio);
    delay(500);
    accion="";
   }
   else{
    accion="";
   }
}
