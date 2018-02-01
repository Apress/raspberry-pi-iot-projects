//
// SHA256 Hash Test
//
// For both the Arduino and ESP8266
// SwitchDoc Labs
//
// February 2016

#include "sha256.h"



void printHash(uint8_t* hash) {
  int i;
  for (i = 0; i < 32; i++) {
    Serial.print("0123456789abcdef"[hash[i] >> 4]);
    Serial.print("0123456789abcdef"[hash[i] & 0xf]);
  }
  Serial.println();
}



void setup() {


  Serial.begin(115200);
  Serial.println("SHA256 Hash Test");
    Serial.println();

}

void loop() {

  uint8_t *hash;
  Sha256.init();
  String hashMessage;
  int i;

  i = 0;

  while (1)
  {

    hashMessage = "This is a message to hash-";
    hashMessage = hashMessage + String(i % 10);
    Serial.print("Hashing Message: ");
    Serial.println(hashMessage);
    Sha256.print(hashMessage);

    hash = Sha256.result();

    printHash(hash);
    Serial.println();
    delay(5000);
    
    i++;

  }

}
