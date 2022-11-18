#include "EspMQTTClient.h"
#include <Adafruit_Sensor.h>

int led = 16;
int btn = 18;
EspMQTTClient client(
  "Hhyos",
  "gy!132tkd!132",
  "192.168.0.8",
  "MQTTUsername",
  "MQTTPassword",
  "hifaker",
  1883        
);

char *topic = "myroom/led1";


void LED_ON(){
    digitalWrite(led, HIGH);
    client.publish("myroom/enter", "LED1 ON!");
}

void LED_OFF(){
    digitalWrite(led, LOW);
    client.publish("myroom/enter", "LED1 OFF!");
}
void Action(){
  if(digitalRead(btn)==0){
    LED_ON();
  }
  else{
    LED_OFF();
  }
}
void setup()
{
  Serial.begin(115200);
  pinMode(led,OUTPUT);
  pinMode(btn,INPUT_PULLUP);
  client.enableDebuggingMessages();
  client.enableHTTPWebUpdater(); // Enable the web updater. User and password default to values of MQTTUsername and MQTTPassword. These can be overridded with enableHTTPWebUpdater("user", "password").
  client.enableOTA(); // Enable OTA (Over The Air) updates. Password defaults to MQTTPassword. Port is the default OTA port. Can be overridden with enableOTA("password", port).
  client.enableLastWillMessage("TestClient/lastwill", "I am going offline");  // You can activate the retain flag by setting the third parameter to true
}

void onConnectionEstablished()
{
  client.subscribe("myroom/led1", [](const String & payload) {
    Serial.println(payload);
    if(payload.equals("ON") ){
      LED_ON();
    }
    if( payload.equals("OFF") ){
      LED_OFF();
    }
  });
}

void loop()
{ 
  Action();
  client.loop();
  delay(1000);
}
