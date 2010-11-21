#include <SPI.h>
#include <Ethernet.h>
#include <Time.h>
#include <VirtualWire.h>

// Enter a MAC address and IP address for your controller below.
// The IP address will be dependent on your local network:
byte mac[] = { 0xC0, 0xFF, 0xEE, 0xC0, 0xFF, 0xEE };
byte ip[] = { 192, 168, 10, 250 };
byte server[] = { 67, 205, 60, 63 };
int port = 80;

char secret[] = "123987";

Client client(server, port);

void setup()
{
  // start the Ethernet connection and the server:
  Ethernet.begin(mac, ip);
  // The ethernet shield uses 10 and 11.  VirtualWire requires PWM pins.
  vw_set_tx_pin(5);
  vw_set_rx_pin(6);
  vw_setup(2400);
  vw_rx_start();
}

void loop()
{
  static float lastReading;
  static bool uploadPending;
  // check for received data
  uint8_t inbound_buf[VW_MAX_MESSAGE_LEN];
  uint8_t inbound_buflen = VW_MAX_MESSAGE_LEN;
  if (vw_wait_rx_max(200)) {
    if (vw_get_message(inbound_buf, &inbound_buflen)) {
      if (inbound_buflen == 2) {
        lastReading = (float)((float)inbound_buf[0] + ((float)inbound_buf[1] / 255.0));
        uploadPending = true;
      }
    }
  }
  
  if (uploadPending && client.connect()) {
    client.print("GET /beerbug/report?secret=");
    client.print(secret);
    client.print("&temperature=");
    client.print(lastReading);
    client.println();
    // give the web browser time to receive the data
    delay(1);
    // close the connection:
    client.stop();
    uploadPending = false;
  }
}
