#include <ESP8266WiFi.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include "DHT.h"

// Constants
#define DHTPIN 2          // GPIO2 (D4)
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

LiquidCrystal_I2C lcd(0x27, 16, 2);  // I2C LCD address may differ (check your module)

const char* ssid = "Net";    // Your WiFi SSID
const char* password = "areebazee30";     // Your WiFi Password

const char* host = "api.thingspeak.com";
String apiKey = "LJW0LWV8MLQCHLTX";    // Your provided ThingSpeak API key

void setup() {
  Serial.begin(115200);

  // Initialize I2C communication for the LCD
  Wire.begin(D2, D1);  // SDA = D2 (GPIO4), SCL = D1 (GPIO5)

  // Initialize LCD
  lcd.begin(16, 2);  // Initialize with 16 columns and 2 rows
  lcd.backlight();

  // Initialize DHT sensor
  dht.begin();

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  lcd.setCursor(0, 0);
  lcd.print("Connecting WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("Connected to WiFi");
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("WiFi Connected");
}

void loop() {
  // Read temperature and humidity from DHT11
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  // Read gas sensor value
  int gasValue = analogRead(A0);

  // Check if any reads failed
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("DHT Error");
    return;
  }

  // Display on LCD
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Temp: ");
  lcd.print(temperature);
  lcd.print("C");
  lcd.setCursor(0, 1);
  lcd.print("Hum: ");
  lcd.print(humidity);
  lcd.print("%");
  delay(2000);

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Gas: ");
  lcd.print(gasValue);
  delay(2000);

  // Send data to ThingSpeak
  sendDataToThingSpeak(temperature, humidity, gasValue);

  // Wait before sending again
  delay(10000);  // 15 seconds delay to match ThingSpeak free API rate limits
}

void sendDataToThingSpeak(float temperature, float humidity, int gasValue) {
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;

    if (client.connect(host, 80)) {
      String postStr = apiKey;
      postStr += "&field1=";
      postStr += String(temperature);
      postStr += "&field2=";
      postStr += String(humidity);
      postStr += "&field3=";
      postStr += String(gasValue);
      postStr += "\r\n\r\n";

      client.print("POST /update HTTP/1.1\n");
      client.print("Host: api.thingspeak.com\n");
      client.print("Connection: close\n");
      client.print("X-THINGSPEAKAPIKEY: " + apiKey + "\n");
      client.print("Content-Type: application/x-www-form-urlencoded\n");
      client.print("Content-Length: ");
      client.print(postStr.length());
      client.print("\n\n");
      client.print(postStr);

      Serial.println("Data sent to ThingSpeak");
      client.stop();
    } else {
      Serial.println("Failed to connect to ThingSpeak");
    }
  }
}
