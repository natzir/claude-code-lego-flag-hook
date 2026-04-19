#include <Servo.h>

Servo flag;

const int SERVO_PIN = 3;
const int SERVO_MIN_US = 400;
const int SERVO_MAX_US = 2500;

// Tune DOWN_POS and UP_POS to match how your servo horn is clipped
// onto the flag — the exact angles depend on your mount.
const int DOWN_POS = 94;
const int UP_POS = 41;

const int WAVE_HOLD_MS = 1500;

void setup() {
  Serial.begin(9600);
  flag.attach(SERVO_PIN, SERVO_MIN_US, SERVO_MAX_US);
  flag.write(DOWN_POS);
  Serial.println("READY");
}

void loop() {
  if (!Serial.available()) return;
  char c = Serial.read();
  switch (c) {
    case 'U':
      flag.write(UP_POS);
      Serial.println("UP");
      break;
    case 'D':
      flag.write(DOWN_POS);
      Serial.println("DOWN");
      break;
    case 'W':
      flag.write(UP_POS);
      delay(WAVE_HOLD_MS);
      flag.write(DOWN_POS);
      Serial.println("WAVE");
      break;
  }
}
