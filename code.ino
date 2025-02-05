#include <DHT.h>
#include <ESP8266WiFi.h>

// DHT sensor setup
#define DHT_PIN 16
#define DHT_TYPE DHT11
DHT dht(DHT_PIN, DHT_TYPE);

const char* ssid = "YourSSID";
const char* password = "YourPassword";

void setup() {
  // Initialize serial communication
  Serial.begin(115200);  // Debugging via Serial Monitor
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
  }
  Serial.println("Connected to WiFi!");
  // Initialize the DHT sensor
  dht.begin();
}

void loop() {
  // Read humidity and temperature from the DHT sensor
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  // Send humidity to the serial port (to be read by Python)
  Serial.print(humidity);
  Serial.println();

  int rssi = WiFi.RSSI();  // Get WiFi signal strength (RSSI)
  Serial.println(rssi);     // Send the RSSI value to Python

  // Delay for 1 second
  delay(1000);
}
