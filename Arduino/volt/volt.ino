void setup() {
  Serial.begin(115200);
}

void loop() {
  int analogValue = analogRead(A2);
  float voltage = (analogValue / 1023.0) * 25.0 - 0.5;
  Serial.print(analogValue);
  Serial.print("    ");
  Serial.println(voltage);
  delay(100);
}

