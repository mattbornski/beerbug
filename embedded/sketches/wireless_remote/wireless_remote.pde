#include <VirtualWire.h>

void setup()
{
  Serial.begin(9600);
  Serial.println("setup start");
  vw_set_tx_pin(10);
  vw_setup(2400);
  vw_rx_start();
}

void loop()
{
  uint8_t inbound_buf[VW_MAX_MESSAGE_LEN];
  uint8_t outbound_buf[VW_MAX_MESSAGE_LEN];
  uint8_t inbound_buflen = VW_MAX_MESSAGE_LEN;
  vw_wait_rx();
  Serial.println("Received");
  if (vw_get_message(inbound_buf, &inbound_buflen)) {
    // Non-blocking
    int i;
    // Message with a good checksum received, dump it.
    // Reverse characters and send back.
    Serial.print("Got: ");
    for (i = 0; i < inbound_buflen; i++) {
      Serial.print(inbound_buf[i], HEX);
      Serial.print(" ");
      outbound_buf[inbound_buflen - i - 1] = inbound_buf[i];
    }
    outbound_buf[inbound_buflen] = inbound_buf[inbound_buflen];
    Serial.println("");
    // Send the reply.
    vw_send(outbound_buf, inbound_buflen);
  }
}
