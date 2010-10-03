#include <VirtualWire.h>

void setup()
{
  Serial.begin(9600);
  vw_setup(2400);
  vw_rx_start();
}

void loop()
{
  uint8_t inbound_buf[VW_MAX_MESSAGE_LEN];
  uint8_t inbound_buflen = VW_MAX_MESSAGE_LEN;
  vw_wait_rx();
  if (vw_get_message(inbound_buf, &inbound_buflen)) {
    // Non-blocking
    int i;
    // Message with a good checksum received, dump it.
    for (i = 0; i < inbound_buflen; i++) {
      Serial.print((int)inbound_buf[i]);
      Serial.print(" ");
    }
    Serial.print("degrees fahrenheit");
    Serial.println("");
  }
}
