import asyncio
from random import choice
from ..application.color import ColorWhite, ColorRed, ColorGreen, ColorBlue, ColorPurple
import logging
from ..application.button import Button
from functools import partial

logger = logging.getLogger(__name__)

class Player:
    def __init__(self):
        self.score = 0
        self.reaction_time = []

class DummyMode:
    def __init__(self, manager):
        ''' Constructor '''
        self.manager = manager
        self.pressed_event = asyncio.Event()
        self.running = False
        self.player_one = Player()
        self.player_two = Player()

    def start(self):
        ''' starts mode '''
        if not self.running:
            asyncio.ensure_future(self.run())

    def stop(self):
        self.running = False

    def button_pressed_callback(self, future: asyncio.Future, button: Button):
        ''' If there is pressed some button '''

        future.result().add_done_callback(partial (self.button_pressed_callback, button= button))
       
        if button.id % 2 == 0 and not button.color.compare(ColorWhite()):
            self.player_one.score = self.player_one.score +1
            reaction_time = button.reaction_time_end - button.reaction_time_start
            self.player_one.reaction_time.append(reaction_time)
        elif button.id % 2 == 1 and not button.color.compare(ColorWhite()):
            self.player_two.score = self.player_two.score +1
            reaction_time = button.reaction_time_end - button.reaction_time_start
            self.player_two.reaction_time.append(reaction_time)


        '''If there is pressed button of wrong color'''
        # if button.id % 2 == 0 and not button.color.compare(ColorGreen()):
        #     self.player_one.score = self.player_one.score -1
        # elif button.id % 2 == 1 and not button.color.compare(ColorGreen()):
        #     self.player_two.score = self.player_two.score -1

        self.pressed_event.set()


    def button_releasse_callback(self, future: asyncio.Future, button: Button):
        ''' If there is released some button '''

        future.result().add_done_callback(partial (self.button_releasse_callback, button= button))
        self.pressed_event.clear()

    def timeout(self):
        self.pressed_event.set()

    async def run(self):
        '''
        Simple method to demonstrate functionality
        If there is some button pressed then starts random color changing cycle
        '''
       
        colors = [ColorRed(), ColorGreen(), ColorBlue(), ColorPurple()]
        if not self.running:
            self.running = True

            for button in self.manager.buttons.values():
                button.pressed_future.add_done_callback(partial(self.button_pressed_callback, button=button))
                button.released_future.add_done_callback(partial(self.button_releasse_callback, button=button))
            
            timeout = 60
            loop = asyncio.get_event_loop()
            timeoutTimerHandle = loop.call_later(timeout, self.timeout)

            while self.running:

                await self.pressed_event.wait()
                
                timeoutTimerHandle.cancel()

                while True: 

                    if not self.pressed_event.is_set():
                        break

                    for button in self.manager.buttons.values():
                        button.set_color(ColorWhite())

                    button = choice(self.manager.buttons)
                    logger.debug("###############  for button id: %d ############", button.id)

                    if button.id % 2 == 0:
                        second_button = self.manager.buttons.get(button.id - 1)
                    else:
                        second_button = self.manager.buttons.get(button.id + 1)

                    new_color= choice(colors)
                    button.set_color(new_color)
                    second_button.set_color(new_color)
                    
                    
                    timeoutTimerHandle = loop.call_later(timeout, self.timeout)

                    self.pressed_event.clear()