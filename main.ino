#include <WiFi.h>
#include <WebSocketsClient.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// Configuration
const char* ssid = "HUAWEI-B525-C12D";
const char* password = "4TL3ETGD4GH";
const char* server_ip = "192.168.8.128";
const int port = 5000;

const char* esp_id = "001";          // This specific ESP board
const char* device_id = "led";       // The LED on this ESP board

#define LED_PIN 12

WebSocketsClient webSocket;

void printJsonDocument(JsonDocument& doc) {
  Serial.println("\n╔══════════════════════════════════════╗");
  Serial.println("║          JSON DOCUMENT DUMP          ║");
  Serial.println("╚══════════════════════════════════════╝");
  
  // Pretty print the JSON
  Serial.println("Formatted JSON:");
  serializeJsonPretty(doc, Serial);
  Serial.println();
  
}

// Send state to server
void sendStateToServer(int state) {
  HTTPClient http;
  
  // Build endpoint for THIS ESP's components
  String endpoint = "http://" + String(server_ip) + ":5000/device/actual_state";
  
  if (!http.begin(endpoint)) {
    Serial.println("HTTP begin failed");
    return;
  }

  http.addHeader("Content-Type", "application/json");

  StaticJsonDocument<192> doc;
  doc["esp_id"] = esp_id;           // Which ESP is reporting
  doc["device_id"] = device_id;     // Which component on that ESP
  doc["actual_state"] = state;      // The state of that component

  String body;
  serializeJson(doc, body);
  
  int httpCode = http.POST(body);
  
  if (httpCode > 0) {
    Serial.printf("State sent - ESP:%s, Device:%s, State:%d\n", 
                  esp_id, device_id, state);
  } else {
    Serial.printf("HTTP failed: %s\n", http.errorToString(httpCode).c_str());
  }

  http.end();
}

// Handle incoming WebSocket messages
void webSocketEvent(WStype_t type, uint8_t* payload, size_t length) {
  if (type == WStype_CONNECTED) {
    Serial.println("WebSocket connected");
    
    // Register THIS ESP with the server
    StaticJsonDocument<128> doc;
    doc["type"] = "register";
    doc["esp_id"] = esp_id;  // Tell server which ESP this is
    
    String msg;
    serializeJson(doc, msg);
    webSocket.sendTXT(msg);
  }
  else if (type == WStype_TEXT) {
    Serial.printf("Received: %s\n", payload);
    
    StaticJsonDocument<256> doc;
    DeserializationError err = deserializeJson(doc, payload, length);
    
    if (err) {
      Serial.printf("JSON error: %s\n", err.c_str());
//    printJsonDocument(doc);
      return;
    }

    // Check which device on THIS ESP to control
    if (doc.containsKey("desired_state")) {
      int desired_state = doc["desired_state"];
        
      Serial.printf("Setting LED on ESP:%s to: %d\n", esp_id, desired_state);
      digitalWrite(LED_PIN, desired_state);
        
      // Confirm the change
      sendStateToServer(desired_state);
    }
  }
}

void setup() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  Serial.begin(115200);

  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected: " + WiFi.localIP().toString());

  // Setup WebSocket
  webSocket.begin(server_ip, port, "/ws");
  webSocket.onEvent(webSocketEvent);
  webSocket.setReconnectInterval(5000);
  
  // Send initial state
  sendStateToServer(0);
}

void loop() {
  webSocket.loop();
}
