from blinkt import clear, show, set_pixel, NUM_PIXELS
from Sleeper import Sleeper
from Pixel import Pixel


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
