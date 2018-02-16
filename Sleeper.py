from asyncio import sleep as asyncsleep


class Sleeper:
    def __init__(self) -> None:
        pass

    def sleep(self, time=0) -> None:
        await asyncsleep(time)
