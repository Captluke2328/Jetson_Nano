void setup() {
  Serial.begin(9600);
  while (!Serial) {
}
}

void loop() {
 if (Serial.available() > 0)
    {
     int temp=Serial.parseInt();
     //if (temp>=0){
       Serial.println(temp);
     //}

    }
}
