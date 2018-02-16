from Sleeper import Sleeper


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
