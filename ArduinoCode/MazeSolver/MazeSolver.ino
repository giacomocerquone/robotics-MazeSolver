//www.elegoo.com

#define SINISTRO digitalRead(11) // sinistro
#define CENTRALE digitalRead(4) // centrale
#define DESTRO digitalRead(2) // destro

#define ENA 10
#define ENB 5
#define in1 9
#define in2 8
#define in3 7
#define in4 6

#define ABS 80

void _mForward()
{ 
  analogWrite(ENA,ABS);
  analogWrite(ENB,ABS);
  digitalWrite(in1,LOW);//digital output
  digitalWrite(in2,HIGH);
  digitalWrite(in3,LOW);
  digitalWrite(in4,HIGH);
  Serial.println("Forward");
}
/*define back function*/
void _mBack()
{
  analogWrite(ENA,ABS);
  analogWrite(ENB,ABS);
  digitalWrite(in1,HIGH);
  digitalWrite(in2,LOW);
  digitalWrite(in3,HIGH);
  digitalWrite(in4,LOW);
  Serial.println("Back");
}
/*define left function*/
void _mLeft()
{
  analogWrite(ENA,120);
  analogWrite(ENB,120);
  digitalWrite(in1,LOW);
  digitalWrite(in2,HIGH);
  digitalWrite(in3,HIGH);
  digitalWrite(in4,LOW);
  Serial.println("Left");
}
/*define right function*/
void _mRight()
{
  analogWrite(ENA,120);
  analogWrite(ENB,120);
  digitalWrite(in1,HIGH);
  digitalWrite(in2,LOW);
  digitalWrite(in3,LOW);
  digitalWrite(in4,HIGH);
  Serial.println("Right");
}

void _mStop(){
   digitalWrite(ENA, LOW);
   digitalWrite(ENB, LOW);
   Serial.println("Stop!");
} 

void setup(){
  Serial.begin(9600);
  pinMode(in1,OUTPUT);
  pinMode(in2,OUTPUT);
  pinMode(in3,OUTPUT);
  pinMode(in4,OUTPUT);
  pinMode(ENA,OUTPUT);
  pinMode(ENB,OUTPUT);
}


void regSx() {
  _mForward();
  delay(100);
  while(!DESTRO) {
    if(SINISTRO)
      _mLeft();
    else
      _mForward();
  }
}

void regDx() {
  _mForward();
  delay(100);
  while(!SINISTRO) {
    if(DESTRO)
      _mRight();
    else
      _mForward();
  }
}

void loop() {
  /** Alter
  if(CENTRALE && !SINISTRO && !DESTRO){
    _mForward();
  } else if(SINISTRO) {
    while(true) {
      _mLeft();
      if(DESTRO) {
        regSx();
        break;
      }
    }
  } else if(DESTRO) {
    while(true) {
      _mLeft();
      if(SINISTRO) {
        regDx();
        break;
      }
    }
  } else {
    _mStop();
  }*/

  if(CENTRALE && !SINISTRO && !DESTRO){
    _mForward();
  } else if(SINISTRO) {
    while(true) {
      _mLeft();
      if(DESTRO) {
        _mForward();
        delay(100);
        break;
      }
    }
  } else if(DESTRO) {
    while(true) {
      _mRight();
      if(SINISTRO) {
        _mForward();
        delay(100);
        break;
      }
    }
  } else {
    _mStop();
  }
  
}

