#include <VirtualWire.h>

void setup()
{
  Serial.begin(9600);
  vw_set_rx_pin(11);
  vw_setup(2400);
  vw_rx_start();
}

void loop()
{
  uint8_t inbound_buf[VW_MAX_MESSAGE_LEN];
  uint8_t inbound_buflen = VW_MAX_MESSAGE_LEN;
  vw_wait_rx();
  if (vw_get_message(inbound_buf, &inbound_buflen)) {
    if (inbound_buflen == 2) {
      Serial.print((float)((float)inbound_buf[0] + ((float)inbound_buf[1] / 255.0)));
      Serial.print(" degrees fahrenheit");
      Serial.println("");
    }
  }
}
