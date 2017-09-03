int N_samples = 160;
int VREF = 517;
float dataIn[100];
float currentNorm = 0.00578;
float watts=0;
float totalWatts;


void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:

for(int q = 0;q<20;q++){
  for(int i = 0; i<100;i++){
dataIn[i] = analogRead(0);
dataIn[i] -= VREF;
dataIn[i] = dataIn[i] * currentNorm;
dataIn[i] = dataIn[i] * 120;
  }

for(int n = 0;n<100;n++){
  watts = watts + abs(dataIn[n]);
}

watts = watts / 100;
totalWatts += watts;
}

  totalWatts = totalWatts / 20;
  if(totalWatts > 1){
  Serial.println(totalWatts);
  }else{
    Serial.println("0");
  }
  totalWatts = 0;

delay(100);

}
