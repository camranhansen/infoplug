float analogMax;
float analog[300];
float analogMin = 1024;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  byte serin = 0;
  // put your main code here, to run repeatedly:

  for (int i = 0; i < 300; i++) {
    analog[i] = analogRead(0);
  }

  for (int q = 0; q < 300; q++) {
    if (analog[q] > analogMax) {
      analogMax = analog[q];
    }
  }

  for (int w = 0; w < 300; w++) {
    if (analog[w] < analogMin) {
      analogMin = analog[w];
    }
  }
  analogMax = 0;
  analogMin = 1024;

  AREF = (analogMax + analogMin) / 2

}
