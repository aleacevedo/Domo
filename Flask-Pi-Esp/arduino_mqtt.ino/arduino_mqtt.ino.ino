#include <EEPROM.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>

 
// Connect to the WiFi
const char* ssid = "Three Mile Island";
const char* password = "11235813fibo";
const char* mqtt_server = "192.168.0.5";
 
WiFiClient espClient;
PubSubClient client(espClient);
 
const byte ledPin5 = 5;
const byte ledPin2 = 2;
const byte ledPin4 = 4;
const byte ledPin0 = 0;

char* topic1 = "1";
char* topic2 = "turnOff";

void callback(char* topic, byte* payload, unsigned int length) {
 Serial.print("Message arrived [");
 Serial.print(topic);
 Serial.print("] ");
 char receivedChar;
 for (int i=0;i<length;i++) 
    receivedChar = (char)payload[i];
 int ledInt = receivedChar - '0';
 if ( strcmp(topic, topic1) == 0){
   digitalWrite(ledInt, HIGH);
 }
 if ( strcmp(topic, topic2) == 0){
   digitalWrite(ledInt, LOW);
 }
  Serial.println();
}
 
 
void reconnect() {
 // Loop until we're reconnected
 while (!client.connected()) {
 Serial.print("Attempting MQTT connection...");
 // Attempt to connect
 if (client.connect("ESP8266 Client")) {
  Serial.println("connected");
  // ... and subscribe to topic
  client.subscribe(topic1);
  client.subscribe(topic2);
 } else {
  Serial.print("failed, rc=");
  Serial.print(client.state());
  Serial.println(" try again in 5 seconds");
  // Wait 5 seconds before retrying
  delay(5000);
  }
 }
}
 
void setup()
{
 Serial.begin(9600);
 WiFi.begin(ssid,password);
   while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
 client.setServer(mqtt_server, 1883);
 client.setCallback(callback);

 pinMode(ledPin5, OUTPUT);
 pinMode(ledPin0, OUTPUT);
 pinMode(ledPin2, OUTPUT);
 pinMode(ledPin4, OUTPUT);
}
 
void loop()
{
 if (!client.connected()) {
  reconnect();
 }
 client.loop();
}
