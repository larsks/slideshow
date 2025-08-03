SRCS = slideshow.py \
			 button.py \
			 pbm.py \
			 ssd1306.py

MPYFILES = $(SRCS:.py=.mpy)

MPREMOTE ?= mpremote
DEVICE ?= u0
MPYCROSS ?= mpy-cross

%.mpy: %.py
	$(MPYCROSS) -march=xtensa -o $@ $<

all: $(MPYFILES)

install: all
	$(MPREMOTE) $(DEVICE) cp main.py $(MPYFILES) :

install-pbm:
	$(MPREMOTE) $(DEVICE) mkdir pbms || :
	$(MPREMOTE) $(DEVICE) fs cp pbms/* :pbms

connect:
	$(MPREMOTE) $(DEVICE)

clean:
	rm -f $(MPYFILES)
