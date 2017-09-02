#include <ESP8266WiFi.h>
#include <SPI.h>
#include <SD.h>

File myFile;




/////////////////////
// Pin Definitions //
/////////////////////
const int LED_PIN = 2; // Thing's onboard, green LED
const int ANALOG_PIN = A0; // The only analog pin on the Thing
const int DIGITAL_PIN = 12; // Digital pin to be read

WiFiServer server(80);

void setup() 
{
  initHardware();
  setupWiFi();
  server.begin();
  Serial.println("Initializing SD card...");
  SD.begin(4);
}

void loop() 
{
  // Check if a client has connected
  WiFiClient client = server.available();
  if (!client) {
    return;
  }

  // Read the first line of the request
  String req = client.readStringUntil('\r');
  Serial.println(req);
  client.flush();

  // Match the request
  int val = -1; // We'll use 'val' to keep track of both the
                // request type (read/set) and value if set.
  if (req.indexOf("/led/0") != -1)
    val = 0; // Will write LED low
  else if (req.indexOf("/led/1") != -1)
    val = 1; // Will write LED high
  else if (req.indexOf("/read") != -1)
    val = -2; // Will print pin reads
  // Otherwise request will be invalid. We'll say as much in HTML
  


  client.flush();
  

  
 if (val == -2)
  { 

    
    if(SD.exists("index.htm")){
      Serial.println("the file exists! wow..");
    }else{
      Serial.println("the file does not exist");
    }
    myFile = SD.open("index.htm");
if (myFile) {
  
  while (myFile.available()) {
  client.write(myFile.read());
  }

  Serial.println("File sent to client!");
    
    myFile.close();
}else{
  Serial.println("error opening file");
}

  
  delay(1);
  Serial.println("Client disonnected");

  // The client will actually be disconnected 
  // when the function returns and 'client' object is detroyed
}
}
void setupWiFi()
{
  WiFi.mode(WIFI_AP);

  // Do a little work to get a unique-ish name. Append the
  // last two bytes of the MAC (HEX'd) to "Thing-":
  uint8_t mac[WL_MAC_ADDR_LENGTH];
  WiFi.softAPmacAddress(mac);
  String macID = String(mac[WL_MAC_ADDR_LENGTH - 2], HEX) +
                 String(mac[WL_MAC_ADDR_LENGTH - 1], HEX);
  macID.toUpperCase();
  String AP_NameString = "InfoPlug";

  char AP_NameChar[AP_NameString.length() + 1];
  memset(AP_NameChar, 0, AP_NameString.length() + 1);

  for (int i=0; i<AP_NameString.length(); i++)
    AP_NameChar[i] = AP_NameString.charAt(i);

  WiFi.softAP(AP_NameChar);
}

void initHardware()
{
  Serial.begin(115200);
  pinMode(DIGITAL_PIN, INPUT_PULLUP);

  // Don't need to set ANALOG_PIN as input, 
  // that's all it can be.
}
