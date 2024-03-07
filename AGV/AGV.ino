const int In1 = 1;
const int In2 = 2;
const int In3 = 3;      
const int In4 = 4;

const int sensor_left= A2;  //左循線感測器宣告
const int sensor_amid= A1;  //中循線感測器宣告
const int sensor_right= A0;  //右循線感測器宣告

const int trig = 9;
const int echo = 8;
const int trigdistance = 12;
long duration, cm, inches;  

int SLL; //左循線感測器狀態宣告
int SAA; //中循線感測器狀態宣告
int SRR; //右循線感測器狀態宣告
int ENA = 6; //左馬達 
int ENB = 5; //右馬達


void setup() {
  Serial.begin(9600);
  pinMode(In1, OUTPUT);
  pinMode(In2, OUTPUT);
  pinMode(In3, OUTPUT);
  pinMode(In4, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(sensor_left, INPUT);
  pinMode(sensor_amid, INPUT);
  pinMode(sensor_right, INPUT);
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT); 
}

void loop() {

  int pot =analogRead(A3);
  int potvalue = map(pot, 0, 1023, 0 , 255);
  Serial.println(potvalue);
    int SLL = 0 ;
    int SAA = 0 ;
    int SRR = 0 ;
    int SensorStatus=0;

    digitalWrite(trig, LOW);
    delayMicroseconds(500);
    digitalWrite(trig, HIGH);
    delayMicroseconds(1000);
    digitalWrite(trig, LOW);

    pinMode(echo, INPUT);
    duration = pulseIn(echo, HIGH);
    
    cm = (duration/2) / 29.1;
    
    SLL=analogRead(A2); //左循線感測器
    Serial.print(SLL); Serial.print(",");Serial.print("Distance : ");Serial.print(cm);Serial.print("cm");Serial.println(); 
    if(SLL>200){
      SensorStatus=(SensorStatus+4);}
         
    SAA=analogRead(A1); //中循線感測器
    Serial.print(SAA); Serial.print(",");Serial.print("Distance : ");Serial.print(cm);Serial.print("cm");Serial.println();  
    if(SAA>200){
      SensorStatus=(SensorStatus+2);}
         
    SRR=analogRead(A0); //右循線感測器
    Serial.println(SRR); Serial.print(",");Serial.print("Distance : ");Serial.print(cm);Serial.print("cm");Serial.println(); 
    if(SRR>200){
      SensorStatus=(SensorStatus+1);}
    Serial.println(SensorStatus);

    if(cm<= trigdistance){
      SensorStatus=(SensorStatus+8);}
      
  switch(SensorStatus){
    case 0: //白白白
      Serial.println("000");
      car_front();
      break;
    case 1: //白白黑
     Serial.println("001");
      car_right();
      break;
    case 2: //白黑白
     Serial.println("010");
      car_front();
      break;
    case 3: //白黑黑
     Serial.println("011");
      car_right();
      break;
    case 4: //黑白白
     Serial.println("100");
      car_left();
      break;
    //case 5:
     //Serial.print("101"); 
      //car_stop();     
      //break;
    case 6: //黑黑白
     Serial.println("110");  
      car_left();
      break;
    case 7: //黑黑黑
     Serial.println("111");
      car_stop();
      break;
    case 8:
      car_stop();
      break;
    case 9:
     car_stop();
     break;
    case 10:
     car_stop();
     break; 
    case 11:
     car_stop();
     break;
    case 12:
     car_stop();
     break;
    //case 13:
     //car_stop();
     //break;
    case 14:
     car_stop();
     break;
    case 15:
     car_stop();
     break;
  }
}

void car_front(){
  int pot =analogRead(A3);
  int potvalue = map(pot, 0, 1023, 0 , 255);
  digitalWrite(In1, LOW);
  digitalWrite(In2, HIGH);
  digitalWrite(In3, HIGH);
  digitalWrite(In4, LOW);
  analogWrite(ENA, 210);//左馬達,最低70  
  analogWrite(ENB, potvalue);
 
}
void car_stop(){
  digitalWrite(In1, LOW);
  digitalWrite(In2, LOW);
  digitalWrite(In3, LOW);
  digitalWrite(In4, LOW);
  analogWrite(ENA, 0);//左馬達 
  analogWrite(ENB, 0); //右馬達,最低130
 
}
void car_right(){
  int pot =analogRead(A3);
  int potvalue = map(pot, 0, 1023, 0 , 255);
  digitalWrite(In1, LOW);
  digitalWrite(In2, HIGH);
  digitalWrite(In3, LOW);
  digitalWrite(In4, HIGH);
  analogWrite(ENA, 255);//左馬達,最低70 
  analogWrite(ENB, potvalue); //右馬達,最低130
 
}
void car_left(){
  int pot =analogRead(A3);
  int potvalue = map(pot, 0, 1023, 0 , 255);
  digitalWrite(In1, HIGH);
  digitalWrite(In2, LOW);
  digitalWrite(In3, HIGH);
  digitalWrite(In4, LOW);
  analogWrite(ENA, 255);//左馬達,最低70
  analogWrite(ENB, potvalue); //右馬達,最低130
 
}
