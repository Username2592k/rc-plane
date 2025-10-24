#include <SPI.h>
#include "RF24.h"

#define CE_PIN 7
#define CSN_PIN 8
RF24 radio(CE_PIN, CSN_PIN);

const byte address[][6] = {"2Node", "1Node"};

void setup() {
  Serial.begin(115200);
  radio.begin();
  radio.setPALevel(RF24_PA_MAX);
  radio.setAutoAck(true);

  radio.openWritingPipe(address[0]);
  radio.openReadingPipe(1, address[1]);

  radio.startListening();
}

void loop() {
  if (radio.available()) {
    char message[32] = "";
    radio.read(message, sizeof(message));
    Serial.print("Received: ");
    Serial.println(message);
  }
}
