
/* Arranca configura pines led ROJO, configura wifi led AZUL, busca DNS service titila led ROJO, conecta mqtt led VIOLETA*/


#include <RestClient.h>
#include <PubSubClient.h>
#include <ESP8266mDNS.h>

#define wifi_ssid "Three Mile Island" 
#define wifi_password "11235813fibo"

#define server "domo"
#define uniqueID "1"

#define INTERRUPT_PIN 5
#define OUTPUT_PIN 4
#define RED_PIN 15
#define BLUE_PIN 13
#define GREEN_PIN 12


#define STEP_VALUE 51

String serverIP;
int state;
int steps;

WiFiClient espClient;
PubSubClient mqttClient(espClient);

int setupWIFI(const char* ssid, const char* pass){
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    on_BLUE();
    delay(250);
    off_RGB();
    delay(250);
  }
  return WiFi.status();
}

void highInterrupt(){
  for(int i = 0; i<1000; i++){
    delayMicroseconds(1000);
  }
  if(digitalRead(INTERRUPT_PIN)==LOW){
    while(digitalRead(INTERRUPT_PIN)==LOW){
      ESP.wdtFeed();
    }
    if(steps == 0){
      steps = 5;
    }
    else{
      steps = 0;
    }
    executeNewState(true);
    return;
  }
  if(steps == 5){
    steps = -1;
  }
  steps++;
  executeNewState(true);
}

void  executeNewState(bool chgState){
  RestClient restClient = RestClient(serverIP.c_str(), 5555);
  char* formato = "/Data/api/v1.0/UMod/%s/%i";
  char url[30];
  if(chgState == true){
      state = steps * STEP_VALUE;
  }
  on_RGB(state,state,state);
  sprintf(url, formato, uniqueID, state);
  restClient.put(url, "");
}

void callback(char* topic, byte* payload, unsigned int length) {
  state = 0;
  for(int i = length-1; i>=0; i--){
    state =  state + (pow(10,length-i-1)*(payload[i]-48));
  }
  steps = state / STEP_VALUE;
  executeNewState(false);
}

void reconnect() {
  while (!mqttClient.connected()) {
    if (mqttClient.connect("ESP8266Client")) {
      mqttClient.subscribe(uniqueID);
    } 
  }
}

void on_RGB(int green, int blue, int red){
  off_RGB();
  analogWrite(GREEN_PIN, green);
  analogWrite(BLUE_PIN, blue);
  analogWrite(RED_PIN, red);
}

void off_RGB(){
  analogWrite(GREEN_PIN, 0);
  analogWrite(BLUE_PIN, 0);
  analogWrite(RED_PIN, 0);
}

void on_RED(){
  on_RGB(0,0,255);
}

void on_BLUE(){
  on_RGB(0,255,0);
}

void on_GREEN(){
  on_RGB(255,0,0);
}

void on_VIOLET(){
  on_RGB(0,255,255);
}


void setup() {
  Serial.begin(115200);
  pinMode(INTERRUPT_PIN, INPUT_PULLUP);
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
  on_RED;
  WiFi.hostname(uniqueID);
  setupWIFI(wifi_ssid, wifi_password);
  MDNS.begin(uniqueID);
  int n = MDNS.queryService("domo", "tcp"); // Send out query for esp tcp services
  while(n==0){
    n = MDNS.queryService("domo", "tcp"); // Send out query for esp tcp services
    on_RED();
    delay(100);
    off_RGB();
    delay(100);
  }
  mqttClient.setServer(MDNS.IP(0), 1883);
  mqttClient.setCallback(callback);
  serverIP = MDNS.IP(0).toString();
  on_GREEN();
}

void loop() {
  if (!mqttClient.connected()) {
    on_RGB(255,255,0);
    reconnect();
  }
  mqttClient.loop();
  if(digitalRead(INTERRUPT_PIN) == LOW){
    highInterrupt();
  }
  delay(100);
  off_RGB();
}
