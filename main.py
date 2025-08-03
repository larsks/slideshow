try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False  # pyright:ignore[reportConstantRedefinition]
import os
import ssd1306
import slideshow

if TYPE_CHECKING:
    from fakes import machine
    from fakes import network
else:
    import machine
    import network


def disable_network():
    network.WLAN(network.STA_IF).active(False)
    network.WLAN(network.AP_IF).active(False)


disable_network()

# power on display and prevent next button from resetting device
ctrl = machine.Pin(14, machine.Pin.OUT)
ctrl.on()

# i2c = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15))
i2c = machine.I2C(sda=machine.Pin(4), scl=machine.Pin(5))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

slides = slideshow.SlideShow()
projector = slideshow.Projector(oled, slides)
rtc = machine.RTC()

try:
    startPaused = rtc.memory()[0] == 1
except IndexError:
    startPaused = False

if "RUN_SLIDESHOW" in os.listdir():
    try:
        projector.play(startPaused=startPaused)
    finally:
        oled.clear()
