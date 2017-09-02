#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <SPI.h>
#include <SD.h>

#define DBG_OUTPUT_PORT Serial


const char* host = "esp8266sd";

ESP8266WebServer server(80);

static bool hasSD = false;
File uploadFile;
String webSite,javaScript,XML;

int analog;
int analogSend;

void returnOK() {
  server.send(200, "text/plain", "");
}

void returnFail(String msg) {
  server.send(500, "text/plain", msg + "\r\n");
}

bool loadFromSdCard(String path){
  String dataType = "text/plain";
  if(path.endsWith("/")) path += "index.htm";

  if(path.endsWith(".src")) path = path.substring(0, path.lastIndexOf("."));
  else if(path.endsWith(".htm")) dataType = "text/html";
  else if(path.endsWith(".css")) dataType = "text/css";
  else if(path.endsWith(".js")) dataType = "application/javascript";
  else if(path.endsWith(".png")) dataType = "image/png";
  else if(path.endsWith(".gif")) dataType = "image/gif";
  else if(path.endsWith(".jpg")) dataType = "image/jpeg";
  else if(path.endsWith(".ico")) dataType = "image/x-icon";
  else if(path.endsWith(".xml")) dataType = "text/xml";
  else if(path.endsWith(".pdf")) dataType = "application/pdf";
  else if(path.endsWith(".zip")) dataType = "application/zip";

  File dataFile = SD.open(path.c_str());
  if(dataFile.isDirectory()){
    path += "/index.htm";
    dataType = "text/html";
    dataFile = SD.open(path.c_str());
  }

  

  if (!dataFile)
    return false;

  if (server.hasArg("download")) dataType = "application/octet-stream";

 
    
  Serial.println(path);
  if(path == "/Index.htm"){

  }else{

    server.streamFile(dataFile, dataType);
  }

  dataFile.close();
  return true;
}



void buildWebsite(){
  buildJavascript();
  webSite="<!DOCTYPE HTML>\n";
  webSite+=javaScript;
  
  webSite+="<head>";
  webSite+="<link rel='stylesheet' type='text/css' href='style.css'>";
  webSite+="<meta name='theme-color' content='#ff6905' />";
  webSite+="</head>";
  webSite+="<script type=text/javascript src='jquery.js'></script>";
  webSite+=javaScript;
 webSite+="<div id='fade'>";
 webSite+="<div class='navbar'>"
 "<a onclick='openNav()'>&#9776;</a>"
 "<span>InfoPlug</span>"
 " </div>"
 " <div id='mySidenav' class='sidenav'>"
 "<a href='javascript:void(0)' class='closebtn' "
 "onclick='closeNav()'>&times;</a>"
 "<a href='#'>Home</a>"
"<a href='Settings.htm'>Settings</a>"
"<a href='About.htm'>About</a>"
"</div>"
"<div class='main'>"
"<table class='headerTable'>"
"<tr>"
" <td class='currentHeader'>WATTAGE</td>"
"<td class='totalHeader'>VOLTAGE</td>"
 "</tr>"
"<tr>"
"<td class='current' id='runtime'></td>"
"<td class='total' id='total'></td>"
"</tr>"
"</table>"
"<hr>""<table class='mainTable'>"
" <tr>"
"<th><img src='Images/laptop_orange.png' style='height: 150px;float: left;'>Laptop<div id='current1'>"
"</div>watts</th>"
"</tr>"
"<tr>"
"<th>Appliance (Placeholder)</th>"
"</tr>"
"<tr>"
"<th>Appliance (Placeholder)</th>"
"</tr>"
"<tr>"
"<th>Appliance (Placeholder)</th>"
"</tr>"
"<tr>"
"<th>Appliance (Placeholder)</th>"
"</tr>"
"<tr>"
"<th>Appliance (Placeholder)</th>"
"</tr>"
"<tr>"
"<th>Appliance (Placeholder)</th>"
"</tr>"
"<tr>"
"<th>Appliance (Placeholder)</th>"
"</tr>"
"<tr>"
"<th>Appliance (Placeholder)</th>"
"</tr>"
"<tr>"
"<th>Appliance (Placeholder)</th>"
"</tr>"
"<tr>"
"<th>Appliance (Placeholder)</th>"
"</tr>"
"<tr>"
"<th>Appliance (Placeholder)</th>"
"</tr>"
"</table>"
"</div>"
"<button class='kc_fab_main_btn' onclick='addDevice()'>+</button>"
"</div>"
 "<script src='main.js'></script>";
  
webSite+="</html>";


  
  webSite+="</HTML>\n";
}

void buildJavascript(){
  javaScript="<SCRIPT>\n";
  javaScript+="var xmlHttp=createXmlHttpObject();\n";

  javaScript+="function createXmlHttpObject(){\n";
  javaScript+=" if(window.XMLHttpRequest){\n";
  javaScript+="    xmlHttp=new XMLHttpRequest();\n";
  javaScript+=" }else{\n";
  javaScript+="    xmlHttp=new ActiveXObject('Microsoft.XMLHTTP');\n";
  javaScript+=" }\n";
  javaScript+=" return xmlHttp;\n";
  javaScript+="}\n";

  javaScript+="function process(){\n";
  javaScript+=" if(xmlHttp.readyState==0 || xmlHttp.readyState==4){\n";
  javaScript+="   xmlHttp.open('PUT','xml',true);\n";
  javaScript+="   xmlHttp.onreadystatechange=handleServerResponse;\n"; // no brackets?????
  javaScript+="   xmlHttp.send(null);\n";
  javaScript+=" }\n";
  javaScript+=" setTimeout('process()',1000);\n";
  javaScript+="}\n";
  
  javaScript+="function handleServerResponse(){\n";
  javaScript+=" if(xmlHttp.readyState==4 && xmlHttp.status==200){\n";
  javaScript+="   xmlResponse=xmlHttp.responseXML;\n";
  javaScript+="   xmldoc = xmlResponse.getElementsByTagName('response');\n";
  javaScript+="   message = xmldoc[0].firstChild.nodeValue;\n";
  javaScript+="   document.getElementById('runtime').innerHTML=message;\n";
  javaScript+=" }\n";
  javaScript+="}\n";
  javaScript+="process();";
  javaScript+="</SCRIPT>\n";
}

void buildXML(){
  XML="<?xml version='1.0'?>";
  XML+="<response>";
  XML+=wattAve();
  XML+="</response>";
}

String wattAve(){

/*
int analog[20];
int max_amps = 0;
int max_amps_index = 0;
for (int i = 0;i<20;i++){
  analog[i] = analogRead(0);
  
}

for (int n = 0;n<20;n++){
  if(analog[n] > max_amps){
    max_amps = analog[n];
    max_amps_index = n;
  }
}

  String max_amps_string = String(max_amps);


 for(int i = 0;i<60;i++){
    analog += abs(analogRead(0));
  }
analogSend = analog / 60;
analog = 0;
  return String(analogSend);
 */
 return "test";
}



void handleWebsite(){
  buildWebsite();
  server.send(200,"text/html",webSite);
}

void handleXML(){
  buildXML();
  server.send(200,"text/xml",XML);
}

void handleNotFound(){
  if(hasSD && loadFromSdCard(server.uri())) return;
  String message = "SDCARD Not Detected\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET)?"GET":"POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i=0; i<server.args(); i++){
    message += " NAME:"+server.argName(i) + "\n VALUE:" + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);
  DBG_OUTPUT_PORT.print(message);
}

void setup(void){
  DBG_OUTPUT_PORT.begin(115200);
  DBG_OUTPUT_PORT.setDebugOutput(true);
  DBG_OUTPUT_PORT.print("\n");
  WiFi.mode(WIFI_AP);
  String AP_NameString = "InfoPlug";

  char AP_NameChar[AP_NameString.length() + 1];
  memset(AP_NameChar, 0, AP_NameString.length() + 1);

  for (int i=0; i<AP_NameString.length(); i++)
    AP_NameChar[i] = AP_NameString.charAt(i);

  WiFi.softAP(AP_NameChar);
  DBG_OUTPUT_PORT.println("Made soft access point");

  // Wait for connection
  uint8_t i = 0;
  while (WiFi.status() != WL_CONNECTED && i++ < 20) {//wait 10 seconds
    delay(500);
  }
 
  DBG_OUTPUT_PORT.println("Connected! IP address: 192.168.4.1");

  if (MDNS.begin(host)) {
    MDNS.addService("http", "tcp", 80);
  }

  server.on("/",handleWebsite);
  server.on("/xml",handleXML);
 
  server.onNotFound(handleNotFound);

  server.begin();
  DBG_OUTPUT_PORT.println("HTTP server started");

  if (SD.begin(4)){
     DBG_OUTPUT_PORT.println("SD Card initialized.");
     hasSD = true;
  }
}

void loop(void){
  server.handleClient();
  Serial.println(analogRead(0));
}

