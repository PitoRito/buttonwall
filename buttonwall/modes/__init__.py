import asyncio
from random import choice
from ..application.color import ColorWhite, ColorRed, ColorGreen, ColorBlue, ColorPurple


class DummyMode:
    def __init__(self, manager):
        ''' Constructor '''
        self.manager = manager
        self.pressed_event = asyncio.Event()
        self.running = False

    def start(self):
        ''' starts mode '''
        if not self.running:
            asyncio.ensure_future(self.run())

    def stop(self):
        self.running = False

    def button_pressed_callback(self, future: asyncio.Future):
        ''' If there is pressed some button '''

        future.result().add_done_callback(self.button_pressed_callback)
        self.pressed_event.set()

    def button_releasse_callback(self, future: asyncio.Future):
        ''' If there is released some button '''

        future.result().add_done_callback(self.button_releasse_callback)
        self.pressed_event.clear()

    async def run(self):
        '''
        Simple method to demonstrate functionality
        If there is some button pressed then starts random color changing cycle
        '''
        colors = [ColorWhite(), ColorRed(), ColorGreen(), ColorBlue(), ColorPurple()]
        if not self.running:
            self.running = True

            for button in self.manager.buttons.values():
                button.pressed_future.add_done_callback(self.button_pressed_callback)
                button.released_future.add_done_callback(self.button_releasse_callback)

            while self.running:
                await self.pressed_event.wait()

                for button in self.manager.buttons.values():
                    if not self.pressed_event.is_set():
                        break

                    button.set_color(choice(colors))
                    await asyncio.sleep(0.1)
