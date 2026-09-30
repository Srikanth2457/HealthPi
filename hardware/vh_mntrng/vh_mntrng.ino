#include <LiquidCrystal.h>
#include "secrets.h"
#include "DHT.h"
#define DHTPIN 7
#include <OneWire.h>
#include <DallasTemperature.h>
#include <Adafruit_BMP085.h>
#define ONE_WIRE_BUS 6
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
Adafruit_BMP085 bmp;
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);
int rpm=0;
// Define the LCD pins
#define RS_PIN 8
#define EN_PIN 9
#define D4_PIN 10
#define D5_PIN 11
#define D6_PIN 12
#define D7_PIN 13
#define buz 5
int th=A2;
int cnt=0;
int xx=0;
int ir=A3;
int rt=0;
LiquidCrystal lcd(RS_PIN, EN_PIN, D4_PIN, D5_PIN, D6_PIN, D7_PIN);

long st=0;

void setup()
{
  // Initialize the LCD
  Serial.begin(9600);
  lcd.begin(16, 2);
 dht.begin();
 bmp.begin();
  pinMode(buz,OUTPUT);
  sensors.begin();
  
   st=millis();
}


void loop()
{
  rt=(millis()-st)/1000;
 int pval=bmp.readPressure()/1000;
  sensors.requestTemperatures(); 
  int tempC = sensors.getTempCByIndex(0);
  int tval=dht.readTemperature();
  int hval=dht.readHumidity();
  int thval=map(analogRead(th),512,1023,0,100);
  if(thval<0)
  thval=0;
  lcd.clear();
  lcd.print("E"+String(tempC) + " T" +String(tval) + " H" +String(hval)+ " R:"+String(rt));
  lcd.setCursor(0,1);
  lcd.print("A:"+String(thval) + " P:"+String(pval) + " S:"+String(rpm));

  cnt=cnt+1;
  if(cnt>15)
  {
    cnt=0;
  Serial.print("3516531," THINGSPEAK_WRITE_API_KEY"0,0,SRC 24G,src@internet,"+String(tempC) + "," +String(tval) +"," +String(hval)+","+ String(rt)+"," + String(thval)+"," + String(pval)+"," + String(rpm)+",0\n");
    }

    xx=0;
    rpm=0;
    while(xx<1000)
    {
      delay(1);
      xx=xx+1;
      if(digitalRead(ir)==0)
      {
        long x=millis();
        while((digitalRead(ir)==0) && (millis()-x)<200)
        {
          if(digitalRead(ir)==1)
          rpm=rpm+1;
        }
        
      }
    }
    rpm=rpm*60;

    if(tempC>37 || tval>38 || thval>90 || pval>102 )
    {
      digitalWrite(buz,1);
      delay(200);
       digitalWrite(buz,0);
    }
    
  
}
