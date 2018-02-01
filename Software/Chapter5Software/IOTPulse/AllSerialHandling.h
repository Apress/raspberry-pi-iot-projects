
//////////
/////////  All Serial Handling Code,
/////////  It's Changeable with the 'serialVisual' variable
/////////  Set it to 'true' or 'false' when it's declared at start of code.
/////////

void sendDataToSerial(char symbol, int data );

void serialOutput() {  // Decide How To Output Serial.

    sendDataToSerial('S', Signal);     // goes to sendDataToSerial function
}


//  Decides How To OutPut BPM and IBI Data
void serialOutputWhenBeatHappens() {
  if (serialData == true) {           //  Code to Make the Serial Monitor Visualizer Work
    Serial.print("*** Heart-Beat Happened *** ");  //ASCII Art Madness
    Serial.print("BPM: ");
    Serial.print(BPM);
    Serial.print(" IBI: ");
    Serial.print(IBI);
    Serial.println("  ");
  } 
}



//  Sends Data to Pulse Sensor Processing App, Native Mac App, or Third-party Serial Readers.
void sendDataToSerial(char symbol, int data ) {
  Serial.print(symbol);

  Serial.println(data);
}



