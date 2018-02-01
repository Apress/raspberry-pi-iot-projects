
void blinkLED(int timesToBlink, int delayBetweenBlinks)
{

  int i;
  for (i = 0; i < timesToBlink; i++)
  {
    digitalWrite(blinkPin, 0);
    delay(delayBetweenBlinks / 2);
    digitalWrite(blinkPin, 1);
    delay(delayBetweenBlinks / 2);

  }

}



