/* LTA node for LTA Packets
 *  This node is the node running on the LTA.  It monitors the shields, allows
 *  for firing the laser canon and also recieves commands for manual shutdown
 *  Based on RFM69 Library and code by Felix Rusu - felix@lowpowerlab.com
 *  Libraries at:  https://github.com/LowPowerLab/
 *  
 */

/*
// **********************************************************************************
// License
// **********************************************************************************
// This program is free software; you can redistribute it 
// and/or modify it under the terms of the GNU General    
// Public License as published by the Free Software       
// Foundation; either version 3 of the License, or        
// (at your option) any later version.                    
//                                                        
// This program is distributed in the hope that it will   
// be useful, but WITHOUT ANY WARRANTY; without even the  
// implied warranty of MERCHANTABILITY or FITNESS FOR A   
// PARTICULAR PURPOSE. See the GNU General Public        
// License for more details.                              
//                                                        
// You should have received a copy of the GNU General    
// Public License along with this program.
// If not, see <http://www.gnu.org/licenses></http:>.
//                                                        
// Licence can be viewed at                               
// http://www.gnu.org/licenses/gpl-3.0.txt
//
// Please maintain this license information along with authorship
// and copyright notices in any redistribution of this code
// **********************************************************************************/

#include <RFM69.h>
#include <SPI.h>

//*********************************************************************************************
// *********** IMPORTANT SETTINGS - YOU MUST CHANGE/ONFIGURE TO FIT YOUR HARDWARE *************
//*********************************************************************************************
#define NETWORKID     100  // The same on all nodes that talk to each other
#define NODEID        2    // The unique identifier of this node
#define RECEIVER      1    // The recipient of packets

//Match frequency to the hardware version of the radio on your Feather
//#define FREQUENCY     RF69_433MHZ
//#define FREQUENCY     RF69_868MHZ
#define FREQUENCY     RF69_915MHZ
#define ENCRYPTKEY    "sampleEncryptKey" //exactly the same 16 characters/bytes on all nodes!
#define IS_RFM69HCW   true // set to 'true' if you are using an RFM69HCW module

//*********************************************************************************************
#define SERIAL_BAUD   115200

// for Feather 32u4 Radio
#define RFM69_CS      8
#define RFM69_IRQ     7
#define RFM69_IRQN    4  // Pin 7 is IRQ 4!
#define RFM69_RST     4

#define LED           13  // onboard blinky
#define SHIELD1        0 // Pin number for shields, must be interuppt pins (0,1,2, or 3)
#define SHIELD2        1
#define SHIELD3        2
#define SHIELD4        3

#define LASER_FIRE    1000  // Time in ms the canon fires for, this will be multiplied by 2 for cooldown

int shield_gen=4;  // How many hits till the shields go off

int16_t packetnum = 0;  // packet counter, we increment per xmission

RFM69 radio = RFM69(RFM69_CS, RFM69_IRQ, IS_RFM69HCW, RFM69_IRQN);

void setup() {
  // while (!Serial); // wait until serial console is open, remove if not tethered to computer. Delete this line on ESP8266
  Serial.begin(SERIAL_BAUD);

  Serial.print("LTA Killswitch board Node :");
  Serial.println(NODEID);
  Serial.print("Radio Type: ");
  Serial.println(FREQUENCY);
  
  // Hard Reset the RFM module
  pinMode(RFM69_RST, OUTPUT);
  digitalWrite(RFM69_RST, HIGH);
  delay(100);
  digitalWrite(RFM69_RST, LOW);
  delay(100);

  // Initialize radio
  radio.initialize(FREQUENCY,NODEID,NETWORKID);
  if (IS_RFM69HCW) {
    radio.setHighPower();    // Only for RFM69HCW & HW!
  }
  radio.setPowerLevel(31); // power output ranges from 0 (5dBm) to 31 (20dBm)
  
  radio.encrypt(ENCRYPTKEY);
  
  pinMode(LED, OUTPUT);
  Serial.print("\nTransmitting at ");
  Serial.print(FREQUENCY==RF69_433MHZ ? 433 : FREQUENCY==RF69_868MHZ ? 868 : 915);
  Serial.println(" MHz");

  //Setup interrupt
  pinMode(SHIELD1, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(SHIELD1),ShieldHit,RISING);
}

//ISR for the Shields
void ShieldHit()
{
  if (digitalRead(SHIELD1) == HIGH)
    --shield_gen;
}


void loop() {
  delay(1000);  // Wait 1 second between transmits, could also 'sleep' here!
    
  char radiopacket[20] = "Test packet #";
  itoa(packetnum++, radiopacket+13, 10);
  Serial.print("Sending "); Serial.println(radiopacket);
    
  if (radio.sendWithRetry(RECEIVER, radiopacket, strlen(radiopacket))) { //target node Id, message as string or byte array, message length
    Serial.println("OK");
    Blink(LED, 50, 3); //blink LED 3 times, 50ms between blinks
  }

  radio.receiveDone(); //put radio in RX mode
  Serial.flush(); //make sure all serial data is clocked out before sleeping the MCU
}

void Blink(byte PIN, byte DELAY_MS, byte loops)
{
  for (byte i=0; i<loops; i++)
  {
    digitalWrite(PIN,HIGH);
    delay(DELAY_MS);
    digitalWrite(PIN,LOW);
    delay(DELAY_MS);
  }
}
