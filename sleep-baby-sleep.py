"""
A red sleep light for my baby.

Jeremy Jones, 2018
"""

from datetime import datetime
from blinkt import clear, show, set_pixel, NUM_PIXELS
from asyncio import get_event_loop
from asyncio import sleep


sleep_length = 3.5
loop = get_event_loop()


class Pixel:

    def __init__(self, colr=None) -> None:
        self.colr = colr

        for c in ['red', 'green', 'blue']:
            setattr(self, c, 0)

        if colr is not None:
            setattr(self, colr, 255)

        self.brightness = 0.0

    def __repr__(self) -> str:
        return "Pixel({})".format('"{}"'.format(self.colr)
                                  if self.colr else 'None')

    def brighter(self) -> None:
        self.set_brightness(
            (self.get_brightness() * (0.1)
             if self.get_brightness() > 0.0
             else 0.1)
        )

    def darker(self) -> None:
        self.set_brightness(
            (self.get_brightness() / (0.1)
             if self.get_brightness() > 0.1
             else 0.0)
        )

    def set_brightness(self, brightness) -> None:
        self.brightness = brightness

    def get_brightness(self) -> float:
        return self.brightness


class LightBoard:

    num_pixels = NUM_PIXELS
    colr = 'red'
    default_brightness = 0.1

    def __init__(self, num_pixels=None) -> None:
        self.num_pixels = num_pixels or self.num_pixels
        self.pixels = [Pixel(self.colr) for l in range(self.num_pixels)]
        self._clear = clear
        self._show = show
        self.set_pixel = set_pixel

    def clear(self) -> None:
        self._clear()
        self.show()

    def show(self) -> None:
        self._show()

    def __len__(self) -> int:
        return self.num_pixels

    def __repr__(self) -> str:
        return "{header}\n  {pixels}\n".format(
            header="Lightboard({n})".format(n=self.num_pixels),
            pixels="\n  ".join(["{}".format(p) for i, p in self.next()])
        )

    def next(self):
        for i in range(len(self)):
            yield i, self.pixels[i]

    def light(self) -> None:
        for pixel_num, pixel in self.next():
            self.set_pixel(pixel_num, pixel.red, pixel.green, pixel.blue,
                           pixel.get_brightness() or self.default_brightness)
            await sleep(0)
        self.show()

    def set_brightness(self, b) -> None:
        for num, pix in self.next():
            pix.set_brightness(b)
            await sleep(0)


async def main() -> None:
    b = LightBoard()

    while True:
        for step in range(len(b), 1, -1):
            b.set_brightness(1/(step+1))
            b.light()
            await sleep(sleep_length)

        b.clear()
        await sleep(sleep_length)


if __name__ == "__main__":
    loop.run_until_complete(main())
