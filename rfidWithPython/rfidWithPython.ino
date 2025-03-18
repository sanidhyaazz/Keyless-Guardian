// ESP32 Pin Assignments:

// 🔹 RFID MFRC522 (SPI)
//    - SS (SDA)  → GPIO 5
//    - SCK       → GPIO 18
//    - MOSI      → GPIO 23
//    - MISO      → GPIO 19
//    - RST       → GPIO 2
//    - RST       → GPIO 2
//    - VCC       → 3.3V
//    - GND       → GND

// 🔹 OLED Display (I2C)
//    - SDA       → GPIO 21
//    - SCL       → GPIO 22
//    - VCC       → 3.3V
//    - GND       → GND

// 🔹 Other Components:
//    - Solenoid Lock  → GPIO 25
//    - Red LED        → GPIO 14
//    - Green LED      → GPIO 27
//    - IR Sensor      → GPIO 15
//    - Pi Zero GPIO 4 → GPIO 33

#include <SPI.h>
#include <MFRC522.h>
#include <Wire.h>
#include <Adafruit_SSD1306.h>

// OLED Display (I2C)
#define OLED_SDA 21
#define OLED_SCL 22

// RFID MFRC522 (SPI)
#define RST_PIN 2  // Updated from GPIO 0
#define SS_PIN 5   // SPI SS pin (unchanged)

// Solenoid & LEDs
#define SOLENOID_PIN 25
#define redLED 14
#define greenLED 27

// IR Sensor
#define irSensor 15

//Pi Pin
#define PI_PIN 33

// Watchdog Timer Timeout (Seconds)
#define WDT_TIMEOUT 5  //5 seconds

//OLED Setup
#define SCREEN_WIDTH 126
#define SCREEN_HEIGHT 64

#define OLED_RESET -1
#define OLED_ADDRESS 0x3C

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_ADDRESS);

int pyread;

MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create MFRC522 instance

// Master Card UID (Replace with your tag's UID)
byte mastercardUID[4] = { 0xB3, 0xC5, 0xE3, 0xC9 };

void setup() {
  // Initialize SPI & RFID
  SPI.begin();
  mfrc522.PCD_Init();

  // Initialize Serial Communication
  Serial.begin(115200);

  // Initialize GPIOs
  pinMode(SOLENOID_PIN, OUTPUT);
  pinMode(redLED, OUTPUT);
  pinMode(greenLED, OUTPUT);
  pinMode(PI_PIN, OUTPUT);
  pinMode(irSensor, INPUT);

  // Ensure solenoid is initially off (locked)
  digitalWrite(PI_PIN, LOW);
  digitalWrite(SOLENOID_PIN, LOW);

  // Initialize OLED Display
  display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDRESS);
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 12);
  display.println("A.T.O.M. Robotics Lab");
  display.display();
}

void loop() {
  int sensorStatus = digitalRead(irSensor);
  if (sensorStatus == LOW) {
    Serial.println("Motion Detected at IR Sensor");
    digitalWrite(greenLED, HIGH);
    display.clearDisplay();
    display.setCursor(0, 12);
    display.println("Opening....");
    display.display();
    digitalWrite(SOLENOID_PIN, HIGH);
    delay(2000);
    digitalWrite(SOLENOID_PIN, LOW);
    digitalWrite(greenLED, LOW);
    display.clearDisplay();
    display.setCursor(0, 12);
    display.println("A.T.O.M. Robotics Lab");
    display.display();
  }

  // Look for new RFID card
  if (!mfrc522.PICC_IsNewCardPresent()) return;
  if (!mfrc522.PICC_ReadCardSerial()) return;

  // Print UID to Serial Monitor
  Serial.print("Scanned UID: ");
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    Serial.print(mfrc522.uid.uidByte[i], HEX);
    if (i < mfrc522.uid.size - 1) Serial.print(":");
  }
  Serial.println();

  digitalWrite(PI_PIN, HIGH);
  delay(1000);
  digitalWrite(PI_PIN, LOW);

  // Check if card is authorized
  if (isAuthorized(mfrc522.uid.uidByte, mfrc522.uid.size)) {
    digitalWrite(SOLENOID_PIN, HIGH);
    delay(2000);
    digitalWrite(SOLENOID_PIN, LOW);
  }

  pyread = Serial.read();

  while (!Serial.available()) {
  }

  String response = Serial.readString();
  Serial.println(response);
  response.trim();

  if (response != "False" && response !="Error" && response != "") {
    String Newresponse = "Welcome " + response;
    display.clearDisplay();
    display.setCursor(0, 12);
    display.println(Newresponse);
    display.display();
    digitalWrite(greenLED, HIGH);
    digitalWrite(SOLENOID_PIN, HIGH);
    delay(2000);
    digitalWrite(SOLENOID_PIN, LOW);
    digitalWrite(greenLED, LOW);
  }else if ( response == ""){
    display.clearDisplay();
    display.setCursor(0, 12);
    display.println("Error");
    display.display();
    digitalWrite(redLED, HIGH);
    delay(100);
    digitalWrite(redLED, LOW);
    delay(100);
    digitalWrite(redLED, HIGH);
    delay(100);
    digitalWrite(redLED, LOW);
    delay(1000);
  }else {
    display.clearDisplay();
    display.setCursor(0, 12);
    display.println("UNAUTHORIZED");
    display.display();
    digitalWrite(redLED, HIGH);
    delay(100);
    digitalWrite(redLED, LOW);
    delay(100);
    digitalWrite(redLED, HIGH);
    delay(100);
    digitalWrite(redLED, LOW);
    delay(1000);
  }
  display.clearDisplay();
  display.setCursor(0, 12);
  display.println("A.T.O.M. Robotics Lab");
  display.display();

  // Halt RFID Processing
  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();
}

// Function to check if UID matches the master card UID
bool isAuthorized(byte *uid, byte length) {
  for (byte i = 0; i < length; i++) {
    if (uid[i] != mastercardUID[i]) {
      return false;
    }
  }
  return true;
}