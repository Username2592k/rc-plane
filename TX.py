#include <SPI.h>
#include "RF24.h"
#include <BluetoothSerial.h>

#define CE_PIN 5
#define CSN_PIN 17
RF24 radio(CE_PIN, CSN_PIN);
BluetoothSerial SerialBT;

const byte address[][6] = {"1Node", "2Node"};
char message[32] = ""; // 31개의 문자 사용 가능

void setup() {
  Serial.begin(115200);
  radio.begin();
  radio.setPALevel(RF24_PA_MAX);
  radio.setAutoAck(true);
  radio.enableDynamicPayloads();
  radio.enableAckPayload();

  SerialBT.begin("ESP32_BT_Device");
  Serial.println(F("Bluetooth ready. Waiting..."));

  // 송신 노드 설정
  radio.openWritingPipe(address[0]);
  radio.openReadingPipe(1, address[1]);
  radio.startListening();
}

void loop() {
  // 블루투스 입력 처리
  if (SerialBT.available()) {
    int len = SerialBT.readBytes(message, sizeof(message) - 1);
    message[len] = '\0';

    radio.stopListening();
    bool success = radio.write(message, strlen(message) + 1);
    Serial.println(success ? F("Sent OK (BT)") : F("Send failed (BT)"));
    radio.startListening();
  }

  // PC 시리얼 입력 처리
  if (Serial.available()) {
    int len = Serial.readBytes(message, sizeof(message) - 1);
    message[len] = '\0';

    radio.stopListening();
    bool success = radio.write(message, strlen(message) + 1);
    Serial.println(success ? F("Sent OK (Serial)") : F("Send failed (Serial)"));
    radio.startListening();
  }

  // RF24 수신 → PC 시리얼로 출력
  if (radio.available()) {
    char message[32] = "";
    radio.read(&message, sizeof(message));
    Serial.print(F("Received: "));
    Serial.println(message);
  }
}