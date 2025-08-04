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
    _lastVal: int
    _pressed: bool
    _was_pressed: bool

    def __init__(self, pin: int, activeLow: bool = True):
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.activeLow = activeLow

        self._lastVal = 1 if activeLow else 0
        self._pressed = False
        self._was_pressed = False

    def poll(self) -> None:
        """Poll the button state. In order to accurately respond to the button,
        you probably want to call this every 50 to 100 ms."""
        val = self.pin.value()
        if not self._pressed and (val == 0 if self.activeLow else 1):
            self._pressed = True
            self._was_pressed = True
        elif val == 1 if self.activeLow else 0:
            self._pressed = False

    def pressed(self) -> bool:
        """Returns True if the button is currently pressed, False otherwise."""
        return self._pressed

    def was_pressed(self) -> bool:
        """Returns True if the button was pressed since you last checked, False otherwise."""
        retval = self._was_pressed
        self._was_pressed = False
        return retval
