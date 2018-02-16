"""
A red sleep light for my baby.
Other colours are available.
Jeremy Jones, 2018
"""

from blinkt import clear, show, set_pixel, NUM_PIXELS
import asyncio


pause_length = 3.5
loop = asyncio.get_event_loop()


class Sleeper:
    def __init__(self) -> None:
        pass

    def sleep(self, time=0) -> None:
        await asyncio.sleep(time)


class Pixel(Sleeper):

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

    def set_brightness(self, brightness) -> None:
        self.brightness = brightness

    def get_brightness(self) -> float:
        return self.brightness


class LightBoard(Sleeper):

    num_pixels = NUM_PIXELS
    colr = 'red'
    default_brightness = 0.1

    def __init__(self, num_pixels=None) -> None:
        self.num_pixels = num_pixels or self.num_pixels
        self.pixels = [Pixel(self.colr) for l in range(self.num_pixels)]
        self._clear = clear
        self._show = show
        self.set_pixel = set_pixel

    def __repr__(self) -> str:
        return "{header}\n  {pixels}\n".format(
            header="Lightboard({n})".format(n=self.num_pixels),
            pixels="\n  ".join(["{}".format(p) for i, p in self.each()])
        )

    def __len__(self) -> int:
        return self.num_pixels

    def clear(self, pause=0) -> None:
        self._clear()
        self.show(pause)

    def show(self, pause=0) -> None:
        self._show()
        self.sleep(pause)

    def each(self, pause=0) -> tuple:
        for i, p in enumerate(self.pixels):
            self.sleep(pause)
            yield i, p

    def all_on(self) -> None:
        for pixel_num, pixel in self.each():
            self.set_pixel(pixel_num, pixel.red, pixel.green, pixel.blue,
                           pixel.get_brightness() or self.default_brightness)

    def light(self, pause=0) -> None:
        self.all_on()
        self.show(pause)

    def light_up(self, level=None) -> None:
        self.set_brightness(level)
        self.light()

    def _set_brightness(self, b) -> None:
        for _, pix in self.each():
            pix.set_brightness(b)

    def set_brightness(self, level=None) -> None:
        brightness = 1 - ((len(self) -
                          (level or 0)) / 10)  # between 0 and 1
        self._set_brightness(brightness)

    def reset(self, pause=0) -> bool:
        self.clear(pause)
        return True


async def main() -> None:
    board = LightBoard()

    while board.reset(pause_length):
        for brightness_level, _ in board.each(pause_length):
            board.light_up(brightness_level)


if __name__ == "__main__":
    loop.run_until_complete(main())
