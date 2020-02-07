import asyncio
import logging
import os
import json
from functools import partial
from aiohttp.web import Application, Response, WebSocketResponse, FileResponse
from .manager import Manager
from .application import Button


logger = logging.getLogger(__name__)


class Web:
    ''' Simple web interface '''

    def __init__(self, manager, loop=None):
        # basic variables
        self.manager = manager
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.clients = []

        self.path = os.path.join(os.path.dirname(__file__), "statics")
        self.app = Application()

        # define web routes
        self.app.router.add_get("/api/websocket", self.websocket)
        self.app.router.add_get("/", self.index)
        self.app.router.add_static("/", self.path)

    async def index(self, request):
        ''' index response '''
        return FileResponse(os.path.join(self.path, "index.html"))

    async def websocket(self, request):
        ''' websocket channel '''
        ws = WebSocketResponse()
        try:
            await ws.prepare(request)
            self.clients.append(ws)

            await ws.send_json({
                "action": "connect",
                "body": {button.id: button.color.html() for button in self.manager.buttons.values()}
            })

            async for msg in ws:
                obj = json.loads(msg.data)
                button = self.manager.buttons[obj["button"]]
                action = obj["action"]
                if action == "press":
                    button.press()

                if action == "release":
                    button.release()

            return ws

        except Exception as e:
            logger.exception(e)

        await ws.close()
        if ws in self.clients:
            self.clients.remove(ws)

    def send_status(self, button: Button):
        ''' send button color changes to web page '''
        for ws in self.clients:
            asyncio.ensure_future(ws.send_json({
                "action": "color",
                "button": button.id,
                "body": button.color.html(),
            }))

    async def run(self):
        ''' Start webserver '''
        self.server = await self.loop.create_server(
            self.app.make_handler(), "0.0.0.0", 5003
        )


class Simulator:
    ''' Glue between manager and web interface '''
    def __init__(self, button_cnt: int = 10):

        self.manager = Manager(button_cnt)
        self.web = Web(self.manager)

        for button in self.manager.buttons.values():
            button.color_future.add_done_callback(
                partial(self.color_changed_callback, button=button)
            )

    def color_changed_callback(self, future: asyncio.Future, button: Button):
        ''' Color change event '''
        future.result().add_done_callback(
            partial(self.color_changed_callback, button=button)
        )
        self.web.send_status(button)

    async def run(self):
        await self.web.run()
        await self.manager.run()
