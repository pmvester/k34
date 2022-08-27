#include "DHT.h"
#include <WiFi.h>
#include <ESPmDNS.h>
#include <WiFiUdp.h>
#include <ArduinoOTA.h>
#include <PubSubClient.h>
#include "RunningMedian.h"

#define DHTPIN 15
#define DHTTYPE DHT21

DHT dht(DHTPIN, DHTTYPE);

const char* ssid = "k34 Network";
const char* password = "deadbeef00";
const char* mqtt_server = "k34.mine.nu";

char hname[] = "esp32-matsal";
char topic[] = "k34/matsal";

WiFiClient espClient;
PubSubClient client(espClient);

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect(hname)) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish(topic, "{\"state\":\"active\"}");      
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup(void) 
{
  Serial.begin(115200);
  Serial.println("Booting");
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.println("Connection Failed! Rebooting...");
    delay(5000);
    ESP.restart();
  }

  ArduinoOTA.setHostname(hname);

  ArduinoOTA
    .onStart([]() {
      String type;
      if (ArduinoOTA.getCommand() == U_FLASH)
        type = "sketch";
      else // U_SPIFFS
        type = "filesystem";

      // NOTE: if updating SPIFFS this would be the place to unmount SPIFFS using SPIFFS.end()
      Serial.println("Start updating " + type);
    })
    .onEnd([]() {
      Serial.println("\nEnd");
    })
    .onProgress([](unsigned int progress, unsigned int total) {
      Serial.printf("Progress: %u%%\r", (progress / (total / 100)));
    })
    .onError([](ota_error_t error) {
      Serial.printf("Error[%u]: ", error);
      if (error == OTA_AUTH_ERROR) Serial.println("Auth Failed");
      else if (error == OTA_BEGIN_ERROR) Serial.println("Begin Failed");
      else if (error == OTA_CONNECT_ERROR) Serial.println("Connect Failed");
      else if (error == OTA_RECEIVE_ERROR) Serial.println("Receive Failed");
      else if (error == OTA_END_ERROR) Serial.println("End Failed");
    });

  ArduinoOTA.begin();

  client.setServer(mqtt_server, 1883);

  Serial.println("Ready");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  
  dht.begin();

  /* We're ready to go! */
  Serial.println("");
}

#define MSG_BUFFER_SIZE  (100)
char msg[MSG_BUFFER_SIZE];

#define SAMPLE_SIZE (29) // can't be be bigger than 255

RunningMedian h = RunningMedian(SAMPLE_SIZE);
RunningMedian t = RunningMedian(SAMPLE_SIZE);

void loop(void) 
{  
  for (int i = 0; i < SAMPLE_SIZE; i++) {
    h.add(dht.readHumidity());
    t.add(dht.readTemperature());      
    ArduinoOTA.handle();
    client.loop();
    delay(2000); // can take up to 2 seconds to produce a sample
  }

  // construct message
  snprintf (msg, MSG_BUFFER_SIZE, "{\"humidity\": %f, \"temperature\": %f}", h.getMedian(), t.getMedian());  

  if (!client.connected()) {
    reconnect();
  }
  Serial.print(topic); Serial.print(" "); Serial.println(msg);  
  client.publish(topic, msg);

  ArduinoOTA.handle();
  client.loop();
}
