import asyncio
from random import choice
from ..application.color import ColorWhite, ColorRed, ColorGreen, ColorBlue, ColorPurple
import logging
from ..application.button import Button
from functools import partial

logger = logging.getLogger(__name__)

class DummyMode:
    def __init__(self, manager):
        ''' Constructor '''
        self.manager = manager
        self.pressed_event = asyncio.Event()
        self.running = False
        self.player_one_score = 0
        self.player_two_score = 0

    def start(self):
        ''' starts mode '''
        if not self.running:
            asyncio.ensure_future(self.run())

    def stop(self):
        self.running = False

    # def button_pressed_callback(self, future: asyncio.Future):
    #     ''' If there is pressed some button '''
    #     future.result().add_done_callback(self.button_pressed_callback)
    #     self.pressed_event.set()

    def button_pressed_callback(self, future: asyncio.Future, button: Button):
        ''' If there is pressed some button '''

        future.result().add_done_callback(partial (self.button_pressed_callback, button= button))
        
       
        if button.id % 2 == 0 and not button.color.compare(ColorWhite()):
            self.player_one_score = self.player_one_score +1
        elif button.id % 2 == 1 and not button.color.compare(ColorWhite()):
            self.player_two_score = self.player_two_score +1

        self.pressed_event.set()


    def button_releasse_callback(self, future: asyncio.Future, button: Button):
        ''' If there is released some button '''

        future.result().add_done_callback(partial (self.button_releasse_callback, button= button))
        self.pressed_event.clear()

    # def button

    async def run(self):
        '''
        Simple method to demonstrate functionality
        If there is some button pressed then starts random color changing cycle
        '''
       
        colors = [ColorWhite(), ColorRed(), ColorGreen(), ColorBlue(), ColorPurple()]
        if not self.running:
            self.running = True

            for button in self.manager.buttons.values():
                button.pressed_future.add_done_callback(partial(self.button_pressed_callback, button=button))
                button.released_future.add_done_callback(partial(self.button_releasse_callback, button=button))

                 

            while self.running:
                await self.pressed_event.wait()

                for button in self.manager.buttons.values():
                    button.set_color(ColorWhite())

                while True: 
                # for button in self.manager.buttons.values():
                    if not self.pressed_event.is_set():
                        break

                    button= choice(self.manager.buttons)
                    logger.debug("###############  for button id: %d ############", button.id)
                    button.set_color(choice(colors))

                    await asyncio.sleep(0.1)
