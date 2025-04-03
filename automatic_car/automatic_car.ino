int stop_distance = 12;

const int trigPin = A1; 
const int echoPin = A2; 

//L298 kết nối arduino
const int motorA1      = 3;  
const int motorA2      = 4;  
const int motorAspeed  = 5; 
const int motorB1      = 7; 
const int motorB2      = 8; 
const int motorBspeed  = 6;  

//kết nối của 5 cảm biến hồng ngoại
const int L2_S = 9; 
const int L1_S = 10; 
const int S_S = 2; 
const int R1_S = 13;
const int R2_S = 12; 


int left2_sensor_state;
int left1_sensor_state;
int s_sensor_state;  
int right1_sensor_state;
int right2_sensor_state;



long duration; 
int distance; 


void setup() {
  pinMode(L2_S, INPUT); 
  pinMode(L1_S, INPUT);
  pinMode(S_S, INPUT);
  pinMode(R1_S, INPUT);
  pinMode(R2_S, INPUT);
  pinMode(motorA1, OUTPUT);
  pinMode(motorA2, OUTPUT);
  pinMode(motorB1, OUTPUT);
  pinMode(motorB2, OUTPUT);
  pinMode(motorAspeed, OUTPUT);
  pinMode(motorBspeed, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  Serial.begin(9600);
  analogWrite(motorAspeed, 120); 
  analogWrite(motorBspeed, 120);
  delay(2000);

}

void loop() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;
  Serial.print("Distance: ");
  Serial.println(distance);

  left2_sensor_state = digitalRead(L2_S);
  left1_sensor_state = digitalRead(L1_S);
  s_sensor_state = digitalRead(S_S);
  right1_sensor_state = digitalRead(R1_S);
  right2_sensor_state = digitalRead(R2_S);

if ((digitalRead(L2_S) == 1)&&(digitalRead(L1_S) ==1) && (digitalRead(S_S) == 1) && (digitalRead(R1_S) == 1)&&(digitalRead(R2_S)) == 1)  {
    forword(); 
  }

  if ((digitalRead(L2_S) == 0)&&(digitalRead(L1_S) ==0) && (digitalRead(S_S) == 1) && (digitalRead(R1_S) == 0)&&(digitalRead(R2_S)) == 0)  {
    forword(); 
  }

  if ((digitalRead(L2_S) == 1)&&(digitalRead(L1_S) == 1) && (digitalRead(S_S) == 1) && (digitalRead(R1_S) == 0)&& (digitalRead(R2_S) == 0)) {
    turnLeft(); 
  }
   if ((digitalRead(L2_S) == 1)&&(digitalRead(L1_S) == 1) && (digitalRead(S_S) == 0) && (digitalRead(R1_S) == 0)&& (digitalRead(R2_S) == 0)) {
    turnLeft(); 
  }

  if ((digitalRead(L2_S) == 0)&&(digitalRead(L1_S) == 0)&& (digitalRead(S_S) == 1) && (digitalRead(R1_S) == 1) && (digitalRead(R2_S) == 1)) {
    turnRight(); 
  }
  if ((digitalRead(L2_S) == 0)&&(digitalRead(L1_S) == 0) && (digitalRead(S_S) == 0) && (digitalRead(R1_S) == 1)&& (digitalRead(R2_S) == 1)) {
    turnRight(); 
  }

  if ((digitalRead(L2_S) == 0)&&(digitalRead(L1_S) == 0) && (digitalRead(S_S) == 0) && (digitalRead(R1_S) == 0)&& (digitalRead(R2_S) == 0)) {
    Stop();
  }



 if (distance < stop_distance) 
  {

    digitalWrite (motorA1, HIGH);
    digitalWrite(motorA2, LOW);
    digitalWrite (motorB1, LOW);
    digitalWrite(motorB2, HIGH);
   
    analogWrite(motorAspeed, 0);
    analogWrite(motorBspeed, 0);
  


    digitalWrite (motorA1, LOW);
    digitalWrite(motorA2, LOW);
    digitalWrite (motorB1, LOW);
    digitalWrite(motorB2, LOW);
    
  


    digitalWrite (motorA1, HIGH); 
    digitalWrite(motorA2, LOW);
    digitalWrite (motorB1, HIGH);
    digitalWrite(motorB2, LOW);
    analogWrite(motorAspeed, 95);
    analogWrite(motorBspeed, 95);
   
  
    

    digitalWrite (motorA1, LOW); 
    digitalWrite(motorA2, HIGH);
    digitalWrite (motorB1, HIGH);
    digitalWrite(motorB2, LOW);
    analogWrite(motorAspeed, 110);
    analogWrite(motorBspeed, 110);
   


    digitalWrite (motorA1, LOW); 
    digitalWrite(motorA2, HIGH);
    digitalWrite (motorB1, LOW);
    digitalWrite(motorB2, LOW);
    analogWrite(motorAspeed, 110);
    analogWrite(motorBspeed, 110);




   
    digitalWrite (motorA1, LOW);
    digitalWrite(motorA2, HIGH);
    digitalWrite (motorB1, HIGH);
    digitalWrite(motorB2, LOW);
    analogWrite(motorAspeed, 110);
    analogWrite(motorBspeed, 110);
   

    
    digitalWrite (motorA1, LOW);
    digitalWrite(motorA2, HIGH);
    digitalWrite (motorB1, LOW);
    digitalWrite(motorB2, LOW);
    analogWrite(motorAspeed, 100);
    analogWrite(motorBspeed, 100);
    

    digitalWrite (motorA1, LOW); 
    digitalWrite(motorA2, HIGH);
    digitalWrite (motorB1, HIGH);
    digitalWrite(motorB2, LOW);
    analogWrite(motorAspeed, 100);
    analogWrite(motorBspeed, 100);

    while ((left1_sensor_state == LOW)&&(left2_sensor_state == LOW)) {
      left2_sensor_state = digitalRead(L2_S);
      left1_sensor_state = digitalRead(L1_S);
      s_sensor_state = digitalRead(S_S);
      right1_sensor_state = digitalRead(R1_S);
      right2_sensor_state = digitalRead(R2_S);
      Serial.println("in the first while");

    }

  }
}

void forword() { 

  digitalWrite (motorA1, LOW);
  digitalWrite(motorA2, HIGH);
  digitalWrite (motorB1, HIGH);
  digitalWrite(motorB2, LOW);
}


void turnRight() {

  digitalWrite (motorA1, LOW);
  digitalWrite(motorA2, LOW);
  digitalWrite (motorB1, HIGH);
  digitalWrite(motorB2, LOW);
}

void turnLeft() {

  digitalWrite (motorA1, LOW);
  digitalWrite(motorA2, HIGH);
  digitalWrite (motorB1, LOW);
  digitalWrite(motorB2, LOW);
}

void Stop() {

  digitalWrite (motorA1, LOW);
  digitalWrite(motorA2, LOW);
  digitalWrite (motorB1, LOW);
  digitalWrite(motorB2, LOW);
}
