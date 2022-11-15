#include <WiFi.h>
#include <FirebaseESP32.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include <string.h>

#define DHTPIN 13
#define DHTTYPE    DHT11
DHT_Unified dht(DHTPIN, DHTTYPE);
uint32_t delayMS;

#define FIREBASE_HOST "https://mymy-1574815720980-default-rtdb.firebaseio.com/"
#define FIREBASE_AUTH "Z2jkJ7SAKQUdmoNWc68Bjk4bNphDLf9p94YQJJlU"

FirebaseData firebaseData;
FirebaseJson json;

#define WIFI_SSID "SSAFY_EMB_2"
#define WIFI_PASSWORD "1210@ssafy"

int adc_val = 0;


float t,h;
void setup()
{
  pinMode(A0, INPUT);

  dht.begin();
  sensor_t sensor;
  dht.temperature().getSensor(&sensor);
  dht.humidity().getSensor(&sensor);
  delayMS = sensor.min_delay / 1000;
  
  Serial.begin(115200);
  
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo native USB port only
  }
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.println(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();
  
  Serial.printf("Firebase Client v%s\n\n", FIREBASE_CLIENT_VERSION);
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
}

void loop()
{
    adc_val = analogRead(A0);
    char ondo[30] = {0};
    char sepdo[30] = {0};
    
    sensors_event_t event;
    dht.temperature().getEvent(&event);
    if (isnan(event.temperature)) {
      Serial.println(F("Error reading temperature!"));
    }

    
    if (isnan(event.relative_humidity)) {
      Serial.println(F("Error reading humidity!"));
    }
    t = event.temperature;
    dht.humidity().getEvent(&event);
    h = event.relative_humidity;
    sprintf(ondo,"%f°C",t);
   // json.set("Temperature", ondo);
    sprintf(sepdo,"%f%%",h);
    Serial.printf("%s %s\n",ondo,sepdo);
    json.set("Temperature",ondo);
    json.set("humidity",sepdo);

    Firebase.pushJSON(firebaseData, "/humid", json); // 보내기  , 송신
    Serial.println("PATH: " + firebaseData.dataPath());
    Serial.println("PUSH NAME: " + firebaseData.pushName());    
    
    delay(2000);
}
