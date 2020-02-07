import asyncio
import logging
from .application import Button, Color
from .modes import DummyMode


logger = logging.getLogger(__name__)


class Manager:
    def __init__(self, button_cnt: int):
        self.button_cnt = button_cnt
        self.buttons = {}
        self.mode = DummyMode(self)

        for _ in range(button_cnt):
            button = Button()
            self.buttons[button.id] = button

    async def run(self):
        await self.mode.run()
