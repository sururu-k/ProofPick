#include <Arduino.h>

// ピン定義 (UIAPduino Pro Micro)
const int PIN_IR_RECEIVER = 3; // 受光モジュール OUT 端子 (アクティブLOW)
const int PIN_BUZZER      = 5; // アクティブブザー (+) 端子 (アクティブHIGH)

void setup() {
  // 受光モジュールの信号ピンを入力（プルアップ）に設定
  pinMode(PIN_IR_RECEIVER, INPUT_PULLUP);

  // ブザーピンを出力に設定し、初期状態は消音(LOW)
  pinMode(PIN_BUZZER, OUTPUT);
  digitalWrite(PIN_BUZZER, LOW);
}

void loop() {
  // 38kHz赤外線を受光するとOUT端子がLOWになる
  if (digitalRead(PIN_IR_RECEIVER) == LOW) {
    digitalWrite(PIN_BUZZER, HIGH); // ブザー発音
  } else {
    digitalWrite(PIN_BUZZER, LOW);  // ブザー停止
  }
}
