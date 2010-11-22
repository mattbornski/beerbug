#include <SPI.h>
#include <Ethernet.h>
#include <Time.h>
#include <VirtualWire.h>

// Ethernet configuration
// ======================
byte mac[] = { 0xC0, 0xFF, 0xEE, 0xC0, 0xFF, 0xEE };
// TODO remove this hardcoded IP when DHCP is operational
byte ip[] = { 192, 168, 10, 250 };

// Beerbug configuration
// =====================
char *server = "brewing.mattborn.net";
// TODO remove this hardcoded IP when DNS is operational
byte resolved[] = { 67, 205, 60, 63 };
int port = 80;
char *url = "/report";

char secret[] = "123987";

Client client = Client(resolved, port);

void setup()
{
  // Ethernet initialization
  // =======================
  // Obtain an IP address from the DHCP server
  //EthernetDHCP.begin(mac);
  // Configure the DNS server
  //EthernetDNS.setDNSServer(EthernetDHCP.dnsIpAddress());
  Ethernet.begin(ip, mac);
  // Connect to the designated server
  //byte resolved[4];
  //EthernetDNS.resolveHostName(server, resolved);
  //client = Client(resolved, port);

  // Wireless initialization
  // =======================
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
    client.print("GET ");
    client.print(url);
    client.print("?secret=");
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
