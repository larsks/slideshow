/*
 * RESET LOGIC
 *
 * Power OLED display only when esp8266 is on. When esp8266 is in deep sleep
 * mode, allow "next image" button to wake the esp8266 (but prevent the button
 * from resetting the esp8266 when it's active).
 *
 *  ATTiny overview
 *                           +-\/-+
 *                Reset PB5 1|    |8 VCC
 *        display power PB3 2|    |7 PB2  input c -- W̅A̅K̅E̅ (GPIO16)
 *      R̅E̅S̅E̅T̅ ((a|b)&c) PB4 3|    |6 PB1  input b -- N̅E̅X̅T̅ (button))
 *                      GND 4|    |5 PB0  input a -- ACTIVE (GPIO14)
 *                            ----
 */

#define READ_BIT(var, pos) (((var) >> (pos)) & 1)
#define SET_BIT(var, pos) ((var) |= (1U << (pos)))
#define CLEAR_BIT(var, pos) ((var) &= (~(1U << (pos))))

#define INA 0
#define INB 1
#define INC 2

#define DISPLAY 3
#define RESET 4

void setup() {
  DDRB = B00011000; // set PORTB outputs
  PORTB = B00000111; //enable all pull ups
}
 
void loop() {

  // espActive is high if the esp8266 is active,
  // low if it is asleep
  boolean espActive = READ_BIT(PINB, INA);

  // wakeReq is low if the user has requested
  // wake via button AND the esp8266 is sleeping
  boolean wakeReq = (espActive | READ_BIT(PINB, INB)) ;

  // reset signal goes low if user requests wake or if rtc lowers WAKE pin
  boolean resetVal = (wakeReq & READ_BIT(PINB, INC));

  // set outputs
  byte output = B00000000;
  espActive ? SET_BIT(output, DISPLAY) : CLEAR_BIT(output, DISPLAY);
  resetVal ? SET_BIT(output, RESET) : CLEAR_BIT(output, RESET);
  PORTB = output;
}

