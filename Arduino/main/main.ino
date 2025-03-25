#include "HX711.h"

#define LOADCELL_DOUT_PIN  A1
#define LOADCELL_SCK_PIN   A0

HX711 scale;
float calibration_factor = 167000;

void setup() {
  Serial.begin(115200);
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.set_scale(calibration_factor);
  scale.tare();
}

void loop() {
  float weight = scale.get_units() * 453.592;
  int analogValue = analogRead(A2);
  float voltage = (analogValue / 1023.0) * 25.0 - 0.5;
  Serial.print(weight, 1);
  Serial.print(",");
  Serial.println(voltage, 2);

  delay(500);
}
