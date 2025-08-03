The ESP8266 goes into deep sleep mode after a period of inactivity. This code controls the logic for the wake signal and manages the display power:

- Power to the display tracks the active state of the ESP826 (esp on = display on, esp sleeping = display off)
- If the ESP8266 is asleep, then either a signal from the RTC (in the case of a timed sleep) or a press of the "next image" button will trigger a wake-up.

This code requires an ATTINY-85.
