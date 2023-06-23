int data;
int Relay1 = 2;
int Relay2 = 3;
int Relay3 = 4;

void setup() {
  Serial.begin(9600);
  pinMode(6, OUTPUT);
  pinMode(Relay1, OUTPUT);
  pinMode(Relay2, OUTPUT);
  pinMode(Relay3, OUTPUT);
  digitalWrite(Relay1, HIGH);
  digitalWrite(Relay2, HIGH);
  digitalWrite(Relay3, HIGH);
}

void loop() {
  if (Serial.available()) {
    data = Serial.read();
  }
  

    if (data == '2') {
      digitalWrite(Relay1, LOW);
      digitalWrite(Relay2, HIGH);
      digitalWrite(Relay3, HIGH);
      delay(200);
      digitalWrite(Relay1, HIGH);
      digitalWrite(Relay2, HIGH);
      digitalWrite(Relay3, HIGH);
    } 
    else if (data == '3') {
      digitalWrite(Relay1, HIGH);
      digitalWrite(Relay2, LOW);
      digitalWrite(Relay3, HIGH);
      delay(200);
      digitalWrite(Relay1, HIGH);
      digitalWrite(Relay2, HIGH);
      digitalWrite(Relay3, HIGH);
    }
    else if (data == '1') {
      digitalWrite(Relay1, HIGH);
      digitalWrite(Relay2, HIGH);
      digitalWrite(Relay3, LOW);
      delay(200);
      digitalWrite(Relay1, HIGH);
      digitalWrite(Relay2, HIGH);
      digitalWrite(Relay3, HIGH);
    }

    if (digitalRead(6) == HIGH) {
      digitalWrite(Relay1, HIGH);
      digitalWrite(Relay2, HIGH);
      digitalWrite(Relay3, HIGH);
    }
  
}




