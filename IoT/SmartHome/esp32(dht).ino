#include "EspMQTTClient.h"
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

#define DHTPIN 13  
#define DHTTYPE DHT11
DHT_Unified dht(DHTPIN, DHTTYPE);

int led = 16;
const int freq = 5000;
const int resolution = 8;
const int ledChannel = 0;
int flag = 0;
int duty = 125;
EspMQTTClient client(
  "Hhyos",
  "gy!132tkd!132",
  "192.168.0.8",
  "MQTTUsername",
  "MQTTPassword",
  "hifaker",
  1883        
);

char *topic = "myroom/led2";
int t,h;


void LED_ON(){
    client.publish("myroom/enter", "LED2 ON!");
    client.publish("myroom/ledon", "1");
    if(flag == 0){
      flag = 1;
      if(duty ==0)
        duty = 100;
      ledcWrite(ledChannel,duty);
      client.publish("myroom/duty",String(duty));
    }
}

void LED_OFF(){
    client.publish("myroom/enter", "LED2 OFF!");
    client.publish("myroom/ledoff", "0");
    if(flag){
      flag = 0;
      ledcWrite(ledChannel,0);
      duty = 0;
      client.publish("myroom/duty",String(duty));
    }
}

void GetValue(){
  sensors_event_t event;
  dht.temperature().getEvent(&event);
  if (isnan(event.temperature)) {
    Serial.println(F("Error reading temperature!"));
  }
  else {
    t = event.temperature;
    client.publish("myroom/temp_info", "temp:"+String(t));
    client.publish("myroom/temp", String(t));
  }
  dht.humidity().getEvent(&event);
  if (isnan(event.relative_humidity)) {
    Serial.println(F("Error reading humidity!"));
  }
  else {
    h = event.relative_humidity;
    client.publish("myroom/humid_info", "humid:"+String(h));
    client.publish("myroom/humid", String(h));
  }
}

void setup()
{
  Serial.begin(115200);

  ledcSetup(ledChannel,freq,resolution);

  ledcAttachPin(led,ledChannel);
  dht.begin();
  client.enableDebuggingMessages();
  client.enableHTTPWebUpdater(); // Enable the web updater. User and password default to values of MQTTUsername and MQTTPassword. These can be overridded with enableHTTPWebUpdater("user", "password").
  client.enableOTA(); // Enable OTA (Over The Air) updates. Password defaults to MQTTPassword. Port is the default OTA port. Can be overridden with enableOTA("password", port).
  client.enableLastWillMessage("TestClient/lastwill", "I am going offline");  // You can activate the retain flag by setting the third parameter to true
}

void onConnectionEstablished()
{
  client.subscribe("myroom/led2", [](const String & payload) {
    Serial.println(payload);
    if(payload.equals("ON") ){
      LED_ON();
    }
    else if( payload.equals("OFF") ){
      LED_OFF();
    }
    else{
      if(flag){
        duty = payload.toInt();
        ledcWrite(ledChannel,duty);
      }
    }
  });
}

void loop()
{ 
  GetValue();
  client.loop();
  delay(1000);
}
