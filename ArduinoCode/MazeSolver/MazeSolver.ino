/* Code written by Gianluca di Francesco and Giacomo Cerquone */

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

unsigned int LASTSENSOR = 0;
unsigned int sx = 0;
unsigned int dx = 0;
unsigned int rounds = 0;
unsigned long tsx = millis();
unsigned long tdx = millis();
unsigned long arriving = 0;
bool run = true;


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

void loop() {
  
  while(run) {

    if(SINISTRO) {
      _mLeft();
      if((millis() - tdx) > 1000) {
        rounds++;
        tsx = millis();
      } else if((millis() - tdx) > 350)
        dx++;
      tdx = millis();
      LASTSENSOR = 0;

    } else if(CENTRALE) {
      _mForward();
      if(DESTRO)
        LASTSENSOR = 2;
      if((millis() - tsx) > 1000)
        rounds++;
      else if((millis() - tsx) > 350)
        sx++;
      if((millis() - tdx) > 1000)
        rounds++;
      else if((millis() - tdx) > 350)
        dx++;
      tsx = millis();
      tdx = millis();

    } else if(DESTRO) {
      _mRight();
      if((millis() - tsx) > 1000) {
        rounds++;
        tdx = millis();
      } else if((millis() - tsx) > 350)
        sx++;
      tsx = millis();
      LASTSENSOR = 2;

    } else if(LASTSENSOR == 0) {
      _mLeft();
      tdx = millis();

    } else if(LASTSENSOR == 2) {
      _mRight();
      tsx = millis();
    }
    if(DESTRO) {
      if(arriving == 0)
        arriving = millis();
      else if((millis() - arriving) > 3000)
        run = false;
    } else arriving = 0;

    delay(5);
  }

  _mStop();
  Serial.println("Maze solved!");
  
  while(true);
}
