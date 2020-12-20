int pin = 8;        //내부 미세먼지 센서 GPIO NUMBER 8
int pin2 = 7;       //외부 미세먼지 센서 GPIO NUMBER 7
unsigned long duration, duration2;           //측정한 시간
unsigned long startTime;                     //현재 시간
unsigned long sampletime_ms = 10000;         //샘플링 시간 : 30s
                                             //미세먼지 센서에서 LOW펄스가 지속되는 시간의 총합
unsigned long lowpulseoccupancy = 0, lowpulseoccupancy2 = 0;
float ratio = 0, ratio2 = 0;                 //데이터 저장을 위한 버퍼(1)
float concentration = 0, concentration2 = 0; //데이터 저장을 위한 버퍼(2)
float ugm3 = 0, ugm3_2 = 0;                  //실제 미세먼지 농도저장을 위한 변수

//프로그램 시작 전 각종 설정처리부
void setup() {
  //시리얼통신시작 (통신속도 9600baud)
  Serial.begin(9600);
  //미세먼지 센서를 입력으로 설정
  pinMode(pin,INPUT);
  pinMode(pin2, INPUT);
  startTime = millis();//get the current time;
}

void loop() {
 //미세먼지센서에서 0값이 발생하면 해당 펄스가 발생한 시간을 측정
 duration = pulseIn(pin, LOW);
 duration2 = pulseIn(pin2, LOW);
 lowpulseoccupancy = lowpulseoccupancy+duration;
 lowpulseoccupancy2 = lowpulseoccupancy2+duration2;
 if ((millis()-startTime) > sampletime_ms)//if the sampling time is over...
 {
  ratio = lowpulseoccupancy/(sampletime_ms*10.0); // Integer percentage 0=>100
  ratio2 = lowpulseoccupancy2/(sampletime_ms*10.0);
  concentration = 1.1*pow(ratio,3)-3.8*pow(ratio,2)+520*ratio+0.62; // using spec sheet curve
  //미세먼지 농도 계산
  ugm3 = concentration*100/13000;
  concentration2 = 1.1*pow(ratio2,3)-3.8*pow(ratio2,2)+520*ratio2+0.62;
  ugm3_2 = concentration2*100/13000;
  
  //미세먼지 농도를 시리얼통신으로 전송
  Serial.println(ugm3);

  Serial.println(ugm3_2);
  
  lowpulseoccupancy = 0;
  lowpulseoccupancy2 = 0;
  startTime = millis();
 }
}