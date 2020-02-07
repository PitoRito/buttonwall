''' Module to demonstrate button functionality '''
import asyncio
import logging
from .color import Color, ColorWhite, ColorRed

__all__ = ['Button']
logger = logging.getLogger(__name__)


class Button:
    ID = 0
    @classmethod
    def get_id(cls):
        cls.ID += 1
        return cls.ID

    def __init__(self, loop: asyncio.AbstractEventLoop = None):
        self.id = self.get_id()
        self.color = ColorWhite()
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.pressed_future = self.loop.create_future()
        self.released_future = self.loop.create_future()
        self.color_future = self.loop.create_future()

    def press(self):
        logger.debug("Pressed: %d", self.id)
        future = self.pressed_future
        self.pressed_future = self.loop.create_future()
        future.set_result(self.pressed_future)

    def release(self):
        logger.debug("Released: %d", self.id)
        future = self.released_future
        self.released_future = self.loop.create_future()
        future.set_result(self.released_future)

    def set_color(self, color: Color):
        logger.debug("Color is set to: %s", color.html())
        future = self.color_future
        self.color_future = self.loop.create_future()
        self.color = color
        future.set_result(self.color_future)
