/*
    SwitchDoc Labs Code for IOT RFID
    IOT RFID uses publish subscribe to communicate to Raspberry Pi
    January 2016
*/

// BOF preprocessor bug prevent - insert on top of your arduino-code
#if 1
__asm volatile ("nop");
#endif

// Board options

#pragma GCC diagnostic ignored "-Wwrite-strings"

extern "C" {
#include "user_interface.h"
}
#include <ESP8266WiFi.h>
#include "PubSubClient.h" 



#include "seeedRFID.h"

#define RFID_RX_PIN 4
#define RFID_TX_PIN 5

#undef TEST

SeeedRFID RFID(RFID_RX_PIN, RFID_TX_PIN);
RFIDdata tag;


int count = 0;   // counter for buffer array

//  Variables

int blinkPin = 0;                // pin to blink led at each reception of RFID code

#include "Utils.h"


//----------------------------------------------------------------------
//Local WiFi Variables

const char* ssid = "gracie";
const char* password = "faraday01";

#define IOTRFIDVERSION 005


// Raspberry Pi Information

#define ORG "switchdoc"
#define DEVICE_TYPE "IOTRFID-01"
#define DEVICE_ID "1"
#define TOKEN "ul!fjH!y8y0gDREmsA"


// setup for IOT Raspberry Pi

char server[] = "192.168.1.40";  // Replace with YOUR RASPBERRY IP Number
char topic[] = "IOTRFID";
char authMethod[] = "use-token-auth";
char token[] = TOKEN;
char clientId[] = "IOTRFID";




void callback(char* topic, byte* payload, unsigned int length) {
  Serial.println("callback invoked from IOT RFID");
}

WiFiClient wifiClient;
PubSubClient client(server, 1883, callback, wifiClient);


void setup() {
  // put your setup code here, to run once:

  pinMode(0, OUTPUT);

  Serial.begin(9600);             // we agree to talk fast!


  Serial.println("----------------");
  Serial.println("IOTRFID publish/subscribe Inventory");
  Serial.println("----------------");

  // signal start of code - three quick blinks
  blinkLED(3, 250);





  Serial.print("Connecting to WiFi ");

  if (strcmp (WiFi.SSID().c_str(), ssid) != 0) {
    WiFi.begin(ssid, password);
  }
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");

  Serial.print("Local WiFi connected, IP address: ");
  Serial.println(WiFi.localIP());

  blinkLED(5, 500);
}

void loop() {
  // put your main code here, to run repeatedly:



  count = 0;


  if (!!!client.connected()) {
    Serial.print("Reconnecting client to ");
    Serial.println(server);
    //while (!!!client.connect(clientId, authMethod, token)) {
    while (!!!client.connect(clientId)) {
      Serial.print(".");
      delay(500);
    }
    Serial.println();
  }

  // Check for RFID available

  String payload;


  if (RFID.isAvailable())
  {
    tag = RFID.data();
    Serial.print("RFID card number read: ");
    Serial.println(RFID.cardNumber());
#ifdef TEST
    Serial.print("RFID raw data: ");
    for (int i = 0; i < tag.dataLen; i++) {
      Serial.print(tag.raw[i], HEX);
      Serial.print('\t');
    }
#endif


    // Sending payload

    payload = "{\"d\":{\"IOTRFID\":\"IR1\",";
    payload += "\"VER\":\"";
    payload += IOTRFIDVERSION;
    payload += "\",\"RFID_ID\":\"";
    payload += String(RFID.cardNumber());
    payload += "\"";
    payload += "}}";


    // check for message

    Serial.println(payload.length());

    count = 0;

    if (payload.length() >= 53) // good message
    {
      Serial.print("Sending IOTRFID payload: ");
      Serial.println(payload);

      if (client.publish(topic, (char*) payload.c_str())) {
        Serial.println("IOTRFID Publish ok");
        blinkLED(1, 500);
      } else {
        Serial.println("IOTRFID Publish failed");
        blinkLED(2, 500);
      }

    }
    else
    {
      delay(500);
    }
  }


  yield();   // This is necessary for the ESP8266 to do the background tasks
}
