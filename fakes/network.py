STA_IF: int = 0
AP_IF: int = 1


class WLAN:
    def __init__(self, iface: int): ...
    def active(self, _: bool): ...
