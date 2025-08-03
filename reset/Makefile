all:
	arduino-cli compile -b ATTinyCore:avr:attinyx5

install: all
	arduino-cli upload -b ATTinyCore:avr:attinyx5 --port /dev/ttyUSB3 -P arduinoasisp
