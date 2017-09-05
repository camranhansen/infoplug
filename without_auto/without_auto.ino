int N_samples = 160;
int AREF = 475;
int VREF = 0;
float totalVolt;
float dataIn[149];
float voltIn[149];
float currentNorm = 0.00578;
float voltNorm = 0.479;
float watts = 0;
float totalWatts;


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

      dataIn[i] -= AREF;
      dataIn[i] = dataIn[i] * currentNorm;

    }

    for (int n = 0; n < 149; n++) {
      watts = watts + (dataIn[n] * voltIn[n]);
    }

    watts = watts / 149;
    totalWatts += watts;
  }

  totalWatts = totalWatts / 20;
  if (totalWatts > 7) {
    Serial.println(totalWatts);
  } else {
    Serial.println("0");
  }
  totalWatts = 0;



}
