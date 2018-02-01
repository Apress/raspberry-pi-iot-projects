//
//
// AES Library Test
// SwitchDoc Labs
// February 2016
//



#include <AESLib.h>

// 256 bit key for AES
uint8_t key[] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31};




void setup() {

  Serial.begin(115200);






}

void loop() {
  // put your main code here, to run repeatedly:

  char data[] = "01234567890Hello";


  int sizeOfArray;
  int i;

  sizeOfArray = sizeof(data) / sizeof(char);

  Serial.println();

  Serial.print("data to be encrypted (ASCII format):\t ");
  Serial.println(data);

  Serial.print("data to be encrypted (Hex format):\t ");

  for (i = 0; i < sizeOfArray - 1; i++)
  {
    if (uint8_t(data[i]) < 0x10)
      Serial.print("0");
    Serial.print(uint8_t(data[i]), HEX);

  }
  Serial.println();


  // Now we encrypt the data using a 256 byte AES key

  aes256_enc_single(key, data);

  // print the encrypted data out in Hex

  Serial.print("encrypted (in Hex):\t\t\t ");


  for (i = 0; i < sizeOfArray - 1; i++)
  {
    if (uint8_t(data[i]) < 0x10)
      Serial.print("0");
    Serial.print(uint8_t(data[i]), HEX);

  }
  Serial.println();

  // Now decrypt the data and print it out

  aes256_dec_single(key, data);
  Serial.print("decrypted:\t\t\t\t ");
  Serial.println(data);
}
