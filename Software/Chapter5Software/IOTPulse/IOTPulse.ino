


/*
    SwitchDoc Labs Code for IOT Pulse
    Connects Pulse detector to the IBM Bluemix IoT using a ESP8266 processor
    based on pulsecounting code from www.pulsesensor.com
    November 2015

  ----------------------  Notes ----------------------  ----------------------
  This code:
  1) Blinks an LED to User's Live Heartbeat   PIN 0
  2) Fades an LED to User's Live HeartBeat
  3) Determines BPM
  4) Prints All of the Above to Serial
*/

extern "C" {
  #include "user_interface.h"
}
#include <ESP8266WiFi.h>
#include <PubSubClient.h> // https://github.com/knolleary/pubsubclient/releases/tag/v2.3

//----------------------------------------------------------------------
//Local WiFi Variables

const char* ssid = "gracie";
//const char ssid[] = {"gracie"};
const char* password = "faraday01";

#define IOTPULSEVERSION 004

// IBM BlueMix IOT Foundation Data

#define ORG "4183lj"
#define DEVICE_TYPE "IOTPulse-01"
#define DEVICE_ID "1"
#define TOKEN "ul!fjH!y8y0gDREmsA"


// setup for IOT IBM

char server[] = ORG ".messaging.internetofthings.ibmcloud.com";
char topic[] = "iot-2/evt/status/fmt/json";
char authMethod[] = "use-token-auth";
char token[] = TOKEN;
char clientId[] = "d:" ORG ":" DEVICE_TYPE ":" DEVICE_ID;

//----------------------------------------------------------------------


//  Variables
int pulsePin = A0;                 // Pulse Sensor purple wire connected to analog pin 0
int blinkPin = 0;                // pin to blink led at each beat
int fadePin = 5;                  // pin to do fancy classy fading blink at each beat
int fadeRate = 0;                 // used to fade LED on with PWM on fadePin

// Volatile Variables, used in the interrupt service routine!
volatile int BPM;                   // int that holds raw Analog in 0. updated every 2mS
volatile int Signal;                // holds the incoming raw data
volatile int IBI = 600;             // int that holds the time interval between beats! Must be seeded!
volatile boolean Pulse = false;     // "True" when User's live heartbeat is detected. "False" when not a "live beat".
volatile boolean QS = false;        // becomes true when Arduoino finds a beat.

// Regards Serial OutPut  -- Set This Up to your needs
static boolean serialData = true;   // Set to 'false' by Default.  Re-set to 'true' to see Arduino Serial Monitor data


#include "AllSerialHandling.h"
#include "Interrupt.h"


void callback(char* topic, byte* payload, unsigned int length) {
  Serial.println("callback invoked from IOT BlueMix");
}

WiFiClient wifiClient;
PubSubClient client(server, 1883, callback, wifiClient);

unsigned long oldPulseTime;
unsigned long oldIOTTime;

void setup() {


  pinMode(blinkPin, OUTPUT);        // pin that will blink to your heartbeat!

  Serial.begin(115200);             // we agree to talk fast!


  Serial.println("----------------");
  Serial.println("IOTPulse IBM Bluemix IOT");
  Serial.println("----------------");

  Serial.print("Connecting to ");
  Serial.print(ssid);
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

  // interruptSetup();                 // sets up to read Pulse Sensor signal every 2mS
  // Note:  Interrupts based on os_timer seems to break the ESP8266 WiFi.  Moving to micros() polling methodology
  oldPulseTime = micros();
  oldIOTTime = micros();
}

int sampleCount = 0;
int beatCount = 0;

int beatValue = 0;
unsigned long newPulseDeltaTime;
unsigned long newIOTDeltaTime;

//  Where the Magic Happens
void loop() {

  //serialOutput() ;

  if (QS == true) {    // A Heartbeat Was Found
    // BPM and IBI have been Determined
    // Quantified Self "QS" true when arduino finds a heartbeat
    digitalWrite(blinkPin, LOW);    // Blink LED, we got a beat.
    beatCount++;

    serialOutputWhenBeatHappens();   // A Beat Happened, Output that to serial.
    QS = false;                      // reset the Quantified Self flag for next time
  }

  newPulseDeltaTime = micros() - oldPulseTime; // doing this handles the 71 second rollover because of unsighned arithmetic

  newIOTDeltaTime = micros() - oldIOTTime; // doing this handles the 71 second rollover because of unsighned arithmetic







  // do this every ten seconds
  if (newIOTDeltaTime > 10000000)  // check for 10sec work to be done
  {

    Serial.print("IOT Delta time =");
    Serial.println(newIOTDeltaTime);
    sampleCount++;

    // Sending payload: {"d":{"IOTPulse":"IP1","VER":2"SC":0,"BPM":235,"IBI":252}}

    String payload = "{\"d\":{\"IOTPulse\":\"IP1\",";
    payload += "\"VER\":";
    payload += IOTPULSEVERSION;
    payload += ",\"SC\":";
    payload += sampleCount;
    payload += ",\"BPM\":";
    payload += BPM;
    payload += ",\"IBI\":";
    payload += IBI;
    payload += ",\"BC\":";
    payload += beatCount;
    payload += "}}";

    if (!!!client.connected()) {
      Serial.print("Reconnecting client to ");
      Serial.println(server);
      while (!!!client.connect(clientId, authMethod, token)) {
        Serial.print(".");
        delay(500);
      }
      Serial.println();
    }

    Serial.print("Sending IOTPulse payload: ");
    Serial.println(payload);

    if (client.publish(topic, (char*) payload.c_str())) {
      Serial.println("BlueMix IOT Publish ok");
    } else {
      Serial.println("BlueMix IOT Publish failed");
    }
    oldIOTTime = micros();

    // restart the pulse counter
    restartPulse();
  }


  //Serial.print("micros()=");
  //Serial.println(micros());





  if (newPulseDeltaTime > 2000)  // check for 2ms work to be done
  {


    //Serial.print("Pulse Delta time =");
    //Serial.println(newPulseDeltaTime);
    // do the work for pulse calculation
    timerCallback(NULL);

    oldPulseTime = micros();
  }

  yield(); //  take a break
}







