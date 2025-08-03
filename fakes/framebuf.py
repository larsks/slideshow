# pyright: reportUnusedParameter=false

MONO_VLSB = 0
MONO_HLSB = 3


class FrameBuffer:
    def __init__(self, data: bytearray, width: int, height: int, kind: int): ...
    def blit(self, fb: "FrameBuffer", w: int, h: int): ...
    def fill(self, val: int): ...
