int led13 = 13;

void setup() {
  Serial.begin(9600);
  pinMode(led13, OUTPUT);
  delay(2000);
}

void loop() {
  while(Serial.available()>0){
    int val = Serial.read() - 48;
    //String num;
    if(val == 1){
      digitalWrite(led13, HIGH);
      for(int i=0; i<21; i++){
        Serial.println(i);
        //delay(500);
      }
    }
    else if(val == 0){
      digitalWrite(led13, LOW);
    }
  }
}
