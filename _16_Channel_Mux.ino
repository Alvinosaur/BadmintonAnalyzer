int pin_Out_S0 = 3;
int pin_Out_S1 = 4;
int pin_Out_S2 = 5;
int pin_Out_S3 = 6;
int pin_In_Mux1 = 2;
int Mux1_State[16] = {0};

void setup() {
  pinMode(pin_Out_S0, OUTPUT);
  pinMode(pin_Out_S1, OUTPUT);
  pinMode(pin_Out_S2, OUTPUT);
  pinMode(pin_Out_S3, OUTPUT);
  //pinMode(pin_In_Mux1, INPUT);
  Serial.begin(9600);
}

void loop() {
  updateMux1();
  for(int i = 0; i < 16; i ++) {
    if(i == 15) {
      Serial.println(Mux1_State[i]);
    } else {
      Serial.print(Mux1_State[i]);
      Serial.print(",");
    }
  }
  delay(500);
}

void updateMux1 () {
  for (int i = 0; i < 16; i++){
    digitalWrite(pin_Out_S0, HIGH && (i & B00000001));
    digitalWrite(pin_Out_S1, HIGH && (i & B00000010));
    digitalWrite(pin_Out_S2, HIGH && (i & B00000100));
    digitalWrite(pin_Out_S3, HIGH && (i & B00001000));
    Mux1_State[i] = !digitalRead(pin_In_Mux1);
  }
}
