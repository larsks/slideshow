try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False  # pyright:ignore[reportConstantRedefinition]

if TYPE_CHECKING:
    from fakes.machine import Pin
else:
    from machine import Pin


class Button:
    pin: Pin
    activeLow: bool
    lastVal: int
    pressed: bool
    was_pressed: bool

    def __init__(self, pin: int, activeLow: bool = True):
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.activeLow = activeLow
        self.lastVal = 1 if activeLow else 1
        self.pressed = False
        self.was_pressed = False

    def poll(self) -> bool:
        val = self.pin.value()
        if not self.pressed and (
            (val == 0 and self.activeLow) or (val == 1 and not self.activeLow)
        ):
            self.pressed = True
            self.was_pressed = True
        elif (val == 1 and self.activeLow) or (val == 0 and not self.activeLow):
            self.pressed = False

        return self.pressed

    def check(self) -> bool:
        retval = self.was_pressed
        self.was_pressed = False
        return retval
