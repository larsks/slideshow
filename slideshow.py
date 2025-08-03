# pyright: reportImplicitRelativeImport=false,reportShadowedImports=false
import os
import pbm
import random
import ssd1306

from button import Button


try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False  # pyright:ignore[reportConstantRedefinition]

if TYPE_CHECKING:
    from fakes import time
    from fakes import framebuf
    from fakes import machine
    from typing import TypeVar
    from collections.abc import Iterable

    T = TypeVar("T")
else:
    import time
    import framebuf
    import machine

    T = int


# micropython on esp8266 does not have random.choice
def choice(items: list[T]) -> T:
    if len(items) < 256:
        r = random.getrandbits(8)
    else:
        r = random.getrandbits(16)

    return items[r % len(items)]


class SlideShow:
    images: list[str]
    _iter: Iterable[framebuf.FrameBuffer] | None

    def __init__(self, imageDir: str = "pbms"):
        self.images = os.listdir(imageDir)
        self._iter = None

    def __iter__(self):
        self._iter = self.slideshow()
        return self

    def __next__(self):
        if self._iter is None:
            self._iter = self.slideshow()
        return next(self._iter)

    def slideshow(self):
        while True:
            imgName = choice(self.images)
            print(f"IMAGE: {imgName}")
            try:
                fb, _, _ = pbm.read_pbm_p4(f"pbms/{imgName}")
                yield fb
            except OSError as err:
                print(f"Failed to read {imgName}: {err}")
                self.images.remove(imgName)


class Projector:
    slides: SlideShow
    display: ssd1306.SSD1306
    playButton: Button = Button(13)
    nextButton: Button = Button(12)

    # interval between slides in seconds
    slideInterval: float = 2

    # polling interval in ms
    pollInterval: int = 50

    # max loops with no user interaction before deep sleep
    maxIdleLoops: int = (10 * 1000) // pollInterval

    MODE_PLAY: int = 0
    MODE_MANUAL: int = 1

    def __init__(
        self,
        display: ssd1306.SSD1306,
        slides: SlideShow,
        slideInterval: float | None = None,
        playButton: Button | None = None,
        nextButton: Button | None = None,
    ):
        self.display = display
        self.slides = slides
        if playButton is not None:
            self.playButton = playButton
        if nextButton is not None:
            self.nextButton = nextButton
        if slideInterval is not None:
            self.slideInterval = slideInterval

    def show(self, fb: framebuf.FrameBuffer):
        self.display.blit(fb, 0, 0)
        self.display.show()

    def play(self, startPaused: bool = False):
        buttons = [self.playButton, self.nextButton]
        mode = self.MODE_MANUAL if startPaused else self.MODE_PLAY
        lastSlideTime = 0
        idleLoops = 0
        autoNext = startPaused

        print(f"START{' PAUSED' if startPaused else ''}")

        while True:
            now = time.ticks_ms()
            idleLoops += 1
            for button in buttons:
                _ = button.poll()

            if mode == self.MODE_PLAY:
                if time.ticks_diff(now, lastSlideTime) > self.slideInterval * 1000:
                    self.show(next(self.slides))
                    lastSlideTime = now

                if self.playButton.check():
                    idleLoops = 0
                    print("STOP")

                    # clear any pending button press
                    _ = self.nextButton.check()
                    mode = self.MODE_MANUAL
            elif mode == self.MODE_MANUAL:
                if self.playButton.check():
                    idleLoops = 0
                    print("PLAY")
                    mode = self.MODE_PLAY
                elif self.nextButton.check() or autoNext:
                    autoNext = False
                    idleLoops = 0
                    print("NEXT")
                    self.show(next(self.slides))

                if idleLoops >= self.maxIdleLoops:
                    print("SLEEP")
                    _ = machine.RTC().memory(b"\x01")
                    machine.deepsleep()

            delta = time.ticks_diff(time.ticks_ms(), now)
            if delta < self.pollInterval:
                machine.lightsleep(self.pollInterval - delta)
