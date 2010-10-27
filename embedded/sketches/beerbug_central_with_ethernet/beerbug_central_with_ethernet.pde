/*
  Web  Server
 
 A simple web server that shows the value of the analog input pins.
 using an Arduino Wiznet Ethernet shield. 
 
 Circuit:
 * Ethernet shield attached to pins 10, 11, 12, 13
 * Analog inputs attached to pins A0 through A5 (optional)
 
 created 18 Dec 2009
 by David A. Mellis
 modified 4 Sep 2010
 by Tom Igoe
 
 */

#include <SPI.h>
#include <Ethernet.h>
#include <Time.h>
#include <VirtualWire.h>

// Enter a MAC address and IP address for your controller below.
// The IP address will be dependent on your local network:
byte mac[] = { 0xC0, 0xFF, 0xEE, 0xC0, 0xFF, 0xEE };
byte ip[] = { 192, 168, 10, 250 };

// Initialize the Ethernet server library
// with the IP address and port you want to use 
// (port 80 is default for HTTP):
Server server(80);

void setup()
{
  // start the Ethernet connection and the server:
  Ethernet.begin(mac, ip);
  server.begin();
  // The ethernet shield uses 10 and 11.  VirtualWire requires PWM pins.
  vw_set_tx_pin(5);
  vw_set_rx_pin(6);
  vw_setup(2400);
  vw_rx_start();
}

void loop()
{
  static float lastReading;
  static long iteration;
  iteration += 1;
  // check for received data
  uint8_t inbound_buf[VW_MAX_MESSAGE_LEN];
  uint8_t inbound_buflen = VW_MAX_MESSAGE_LEN;
  if (vw_wait_rx_max(200)) {
    if (vw_get_message(inbound_buf, &inbound_buflen)) {
      if (inbound_buflen == 2) {
        lastReading = (float)((float)inbound_buf[0] + ((float)inbound_buf[1] / 255.0));
      }
    }
  }
  
  // listen for incoming clients
  Client client = server.available();
  if (client) {
    // an http request ends with a blank line
    boolean currentLineIsBlank = true;
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        // if you've gotten to the end of the line (received a newline
        // character) and the line is blank, the http request has ended,
        // so you can send a reply
        if (c == '\n' && currentLineIsBlank) {
          // send a standard http response header
          client.println("HTTP/1.1 200 OK");
          client.println("Content-Type: text/html");
          client.println();

          client.print("iteration: ");
          client.print(iteration);
          client.println("<br />");
          client.print("last reading: ");
          client.print(lastReading);
          client.println("<br />");
          break;
        }
        if (c == '\n') {
          // you're starting a new line
          currentLineIsBlank = true;
        } 
        else if (c != '\r') {
          // you've gotten a character on the current line
          currentLineIsBlank = false;
        }
      }
    }
    // give the web browser time to receive the data
    delay(1);
    // close the connection:
    client.stop();
  }
}
