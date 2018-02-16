"""
A red sleep light for my baby.
Other colours are available.
Jeremy Jones, 2018
"""

from asyncio import get_event_loop
from Lightboard import LightBoard


pause_length = 3.5
loop = get_event_loop()


async def main() -> None:
    board = LightBoard()

    while board.reset(pause_length):
        for light_no, _ in board.each(pause_length):
            brightness_level = light_no
            board.light_up(brightness_level)


if __name__ == '__main__':
    loop.run_until_complete(main())
