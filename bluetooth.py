#include <BluetoothSerial.h>

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
  #error Bluetooth is not enabled! Please enable it in the settings
#endif

BluetoothSerial SerialBT;

void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32_BT_Device");   // 블루투스 장치명 설정
  Serial.println("The device started, you can pair it with Bluetooth!");
}

void loop() {
  // PC(시리얼 모니터) → 블루투스
  if (Serial.available()) {
    char c = Serial.read();
    SerialBT.write(c);
  }
  // 블루투스 → PC(시리얼 모니터)
  if (SerialBT.available()) {
    char c = SerialBT.read();
    Serial.print("From BT: ");
    Serial.println(c);
  }

  delay(20);
}
