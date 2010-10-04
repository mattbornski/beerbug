#include <VirtualWire.h>

void setup()
{
  vw_set_tx_pin(10);
  vw_setup(2400);
}

float getVoltage(int pin)
{
  return analogRead(pin) * 0.004882814;
}

void loop()
{
  float voltage = getVoltage(0);
  float centigrade = (voltage - 0.5) * 100;
  float fahrenheit = (centigrade * 1.8) + 32;
  
  uint8_t integral = (uint8_t)fahrenheit;
  uint8_t fractional = (uint8_t)((fahrenheit - (float)integral) * 255.0);
  
  uint8_t outbound_buf[VW_MAX_MESSAGE_LEN];
  uint8_t outbound_buflen = VW_MAX_MESSAGE_LEN;
  outbound_buf[0] = integral;
  outbound_buf[1] = fractional;
  outbound_buflen = 2;
  // Send the measurement.
  vw_send(outbound_buf, outbound_buflen);
  // Wait for next measurement interval.
  delay(300000);
}
