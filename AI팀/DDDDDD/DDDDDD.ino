
int data;

void setup() {
  Serial.begin(9600);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(7, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    data = Serial.read();
  }

  if (data == '1') {
    digitalWrite(2, HIGH);
    digitalWrite(3, LOW);
    
  } else if (data == '2') {
    digitalWrite(2, LOW);
    digitalWrite(3, HIGH);
    
  } else if (data == '0') {
    digitalWrite(2, HIGH);
    digitalWrite(3, HIGH);
    digitalWrite(4, LOW);
    digitalWrite(7, HIGH);
    
  }
  else if (data == '3') {
    digitalWrite(2, HIGH);
    digitalWrite(3, HIGH);
    digitalWrite(4, HIGH);
    digitalWrite(7, LOW);
  } 
}
