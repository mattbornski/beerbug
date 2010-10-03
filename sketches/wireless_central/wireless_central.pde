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
  const char *msg = "Fee Fie Foe Fum";
  uint8_t buf[VW_MAX_MESSAGE_LEN];
  uint8_t buflen = VW_MAX_MESSAGE_LEN;
  vw_send((uint8_t *)msg, strlen(msg));
  vw_wait_tx(); // Wait until the whole message is gone
  Serial.println("Sent");
  // Wait at most 500ms for a reply
  if (vw_wait_rx_max(500)) {
    if (vw_get_message(buf, &buflen)) {
      // Non-blocking
      int i;
      // Message with a good checksum received, dump it.
      Serial.print("Got reply: ");
      for (i = 0; i < buflen; i++) {
        Serial.print(buf[i], HEX);
        Serial.print(" ");
      }
      Serial.println("");
    }
  } else {
    Serial.println("Timout");
  }
}
