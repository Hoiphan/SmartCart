#include "HX711.h"

#define LOADCELL_DOUT_PIN A1
#define LOADCELL_SCK_PIN A0

HX711 scale;

// void setup() {
//   Serial.begin(9600);
//   scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
// }

void setup() {
  Serial.begin(9600);
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  
  Serial.println("Tare... Please remove all weight from the scale.");
  delay(3000);
  scale.tare();
  delay(3000);
  scale.tare();

  Serial.println("Tare done.");
}

void loop() {
  if (scale.is_ready()) {
    Serial.print(scale.get_units(5), 1);
    Serial.println(" g");
    delay(100);
  } else {
    Serial.println("HX711 not found.");
  }
  delay(200);
}
