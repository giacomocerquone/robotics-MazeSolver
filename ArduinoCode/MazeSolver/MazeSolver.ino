/* Code written by Gianluca di Francesco and Giacomo Cerquone */

#include <ros.h>
#include <std_msgs/Int16MultiArray.h>
#include <std_msgs/String.h>

#define SINISTRO digitalRead(11) // sinistro
#define CENTRALE digitalRead(4) // centrale
#define DESTRO digitalRead(2) // destro

#define BZ 13
#define ENA 10
#define ENB 5
#define in1 9
#define in2 8
#define in3 7
#define in4 6

#define ABS 80

#define  B6    1975.53
#define  C7    2093
#define  D7    2349.32

unsigned int LASTSENSOR = 0;
unsigned int sx = 0;
unsigned int dx = 0;
unsigned int rounds = 0;
unsigned long tsx = millis();
unsigned long tdx = millis();
unsigned long arriving = 0;
bool run = true;

ros::NodeHandle nh;



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

void _playSong() {
  tone(BZ, B6, 50);
  delay(50);
  tone(BZ, C7, 50);
  delay(50);
  tone(BZ, D7, 50);
  delay(250);
  tone(BZ, B6, 100);
  delay(100);
  tone(BZ, D7, 400);
  delay(400);
}

void leftlogic(const std_msgs::String& toggle_msg){
 _mLeft();
      if((millis() - tdx) > 400) {
        rounds++;
        tone(BZ, D7, 400);
        tsx = millis();
      } else if((millis() - tdx) > 250) {
        dx++;
        tone(BZ, C7, 400);
      }
      tdx = millis();
      LASTSENSOR = 0;
}
void forwardlogic(const std_msgs::String& toggle_msg){
_mForward();
      if(DESTRO)
        LASTSENSOR = 2;
      if((millis() - tsx) > 1000)
        rounds++;
      else if((millis() - tsx) > 250) {
        sx++;
        tone(BZ, D7, 400);
      }
      if((millis() - tdx) > 400) {
        rounds++;
        tone(BZ, D7, 400);
      } else if((millis() - tdx) > 250) {
        dx++;
        tone(BZ, C7, 400);
      }
      tsx = millis();
      tdx = millis();

}
void rightlogic(const std_msgs::String& toggle_msg){
  _mRight();
      if((millis() - tsx) > 400) {
        rounds++;
        tone(BZ, D7, 400);
        tdx = millis();
      } else if((millis() - tsx) > 250) {
        sx++;
        tone(BZ, D7, 400);
      }
      tsx = millis();
      LASTSENSOR = 2;

}
void leftfinal(const std_msgs::String& toggle_msg){
  _mLeft();
      tdx = millis();

}
void rightfinal(const std_msgs::String& toggle_msg){
  _mRight();
     tsx = millis();

}
void right(const std_msgs::String& toggle_msg){
  if(arriving == 0)
        arriving = millis();
      else if((millis() - arriving) > 3000)
         _mStop();
  Serial.println("Maze solved!");
  //_playSong();

}
void arriving1(const std_msgs::String& toggle_msg){
 arriving = 0;

}



std_msgs::Int16MultiArray s_array;
ros::Publisher chatter("sensors", &s_array);
ros::Subscriber<std_msgs::String> sub("leftlogic", &leftlogic);
ros::Subscriber<std_msgs::String> sub1("forwardlogic", &forwardlogic);
ros::Subscriber<std_msgs::String> sub2("rightlogic", &rightlogic);
ros::Subscriber<std_msgs::String> sub3("leftfinal", &leftfinal);
ros::Subscriber<std_msgs::String> sub4("rightfinal", &rightfinal);
ros::Subscriber<std_msgs::String> sub5("right", &right);
ros::Subscriber<std_msgs::String> sub6("arriving", &arriving1);

void setup(){
  Serial.begin(9600);
  pinMode(in1,OUTPUT);
  pinMode(in2,OUTPUT);
  pinMode(in3,OUTPUT);
  pinMode(in4,OUTPUT);
  pinMode(ENA,OUTPUT);
  pinMode(ENB,OUTPUT);
  digitalWrite(BZ, HIGH);
  tone(BZ, D7, 500);
  
  nh.initNode();
  nh.advertise(chatter);
  nh.subscribe(sub);
  nh.subscribe(sub1);
  nh.subscribe(sub2);
  nh.subscribe(sub3);
  nh.subscribe(sub4);
  nh.subscribe(sub5);
  nh.subscribe(sub6);


}

void loop() {
  
  s_array.data_length = 5;
  
  s_array.data[1] = SINISTRO;
  s_array.data[2] = CENTRALE;
  s_array.data[3] = DESTRO;
  s_array.data[4]= LASTSENSOR;
  
  chatter.publish( &s_array );
  nh.spinOnce();
  delay(20);

/*
  while(run) {

    if(SINISTRO) {
      _mLeft();
      if((millis() - tdx) > 400) {
        rounds++;
        tone(BZ, D7, 400);
        tsx = millis();
      } else if((millis() - tdx) > 250) {
        dx++;
        tone(BZ, C7, 400);
      }
      tdx = millis();
      LASTSENSOR = 0;

    } else if(CENTRALE) {
      _mForward();
      if(DESTRO)
        LASTSENSOR = 2;
      if((millis() - tsx) > 1000)
        rounds++;
      else if((millis() - tsx) > 250) {
        sx++;
        tone(BZ, D7, 400);
      }
      if((millis() - tdx) > 400) {
        rounds++;
        tone(BZ, D7, 400);
      } else if((millis() - tdx) > 250) {
        dx++;
        tone(BZ, C7, 400);
      }
      tsx = millis();
      tdx = millis();

    } else if(DESTRO) {
      _mRight();
      if((millis() - tsx) > 400) {
        rounds++;
        tone(BZ, D7, 400);
        tdx = millis();
      } else if((millis() - tsx) > 250) {
        sx++;
        tone(BZ, D7, 400);
      }
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
  _playSong();
  while(true);
*/
}
