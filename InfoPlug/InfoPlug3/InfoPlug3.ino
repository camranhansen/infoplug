int N_samples = 160;
int AREF = 512;
int VREF = 0;
float totalVolt;
float dataIn[149];
float voltIn[149];
float currentNorm = 0.00578;
float voltNorm = 0.479;
float watts = 0;
float totalWatts;
float maxA = 0;
float minA = 1024;
float arAref = 0;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:

  for (int q = 0; q < 20; q++) {
    for (int i = 0; i < 149; i++) {
      dataIn[i] = analogRead(0);
      voltIn[i] = analogRead(1);
      //volt
      totalVolt += voltIn[i];
      VREF = totalVolt / 149;
      totalVolt = 0;
      voltIn[i] -= VREF;
      voltIn[i] = voltIn[i] * voltNorm;
      //amp
      if (dataIn[i] > maxA) {
        maxA = dataIn[i];
      } else if (dataIn[i] < minA) {
        minA = dataIn[i];
      }
      dataIn[i] -= AREF;
      dataIn[i] = dataIn[i] * currentNorm;

    }

    for (int n = 0; n < 149; n++) {
      watts = watts + (dataIn[n] * voltIn[n]);
    }

    arAref = arAref + (maxA + minA) / 2;

    maxA = 0;
    minA = 1024;
    // resets variables
    watts = watts / 149;
    totalWatts += watts;
  }
  AREF = arAref / 20;
  arAref = 0;
  maxA = 0;
  minA = 1024;
  totalWatts = totalWatts / 20;
  if (totalWatts > 1) {
    Serial.println(totalWatts);
  } else {
    Serial.println("0");
  }
  totalWatts = 0;


}
