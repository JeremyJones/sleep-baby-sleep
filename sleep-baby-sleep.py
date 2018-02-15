"""
A red sleep light for my baby.

Jeremy Jones, 2018
"""

from datetime import datetime
from time import sleep
from blink import clear, show, set_pixel, NUM_PIXELS


class Light:

    def __init__(self, red, green, blue) -> None:
        self.red = red
        self.green = green
        self.blue = blue
        self.brightness = 0.0

    def __len__(self) -> float:
        return self.brightness

    def brighter(self) -> None:
        self.set_brightness(
            (self.get_brightness() * (0.1)
             if self.get_brightness() > 0.0
             else 0.1)
        )
        
    def set_brightness(self, brightness):
        pass


def main() -> None:
    pass


if __name__ == "__main__":
    main()