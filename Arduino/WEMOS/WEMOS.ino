#include <Servo.h>

#define pinServo1 D5 //pin servo tunjuk, tengah
#define pinServo2 D6 //pin servo ibu, manis, kici

#define tarik1 180 //servo1 ditarik
#define tarik2 180 //servo2 ditarik

#define lepas1 0 //servo1 dilepas
#define lepas2 0 //servo2 dilepas

Servo servo1; //tunjuk, tengah
Servo servo2; //ibu, manis, kici

#define LED LED_BUILTIN

#define ledOff digitalWrite(LED, 1)
#define ledOn digitalWrite(LED, 0)
 
void setup() { 
  Serial.begin(9600);
  pinMode(LED, OUTPUT);
  pinMode(pinServo1, OUTPUT);
  pinMode(pinServo2, OUTPUT); 

  servo1.attach(pinServo1, 500, 2400);
  servo2.attach(pinServo2, 500, 2400);

  servo1.write(lepas1);
  servo2.write(lepas2);
  
  delay(1000);
}

void loop() { 
  if(Serial.available()>0){
    char dataS = Serial.read(); 
     
    if(dataS == '1'){ //deteksi gunting
      //bikin batu
      servo1.write(tarik1);
      servo2.write(tarik2);
      ledOn;
    } else if(dataS == '2'){ //deteksi batu
      //bikin kertas
      servo1.write(lepas1);
      servo2.write(lepas2);
      ledOff;
    } else if(dataS == '3'){ //deteksi kertas 
      //bikin guntin
      servo1.write(lepas1);
      servo2.write(tarik2); 
      ledOn;
    }  
    
  }
}
