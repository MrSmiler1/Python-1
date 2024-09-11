import json
import random
import asyncio
import time
from flask import Flask
from threading import Thread
from importlib import import_module
from highrise import *
from highrise.models import *
from asyncio import run as arun
from highrise.__main__ import *

class Bot(BaseBot):
    def __init__(self):
        super().__init__()

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        await self.highrise.tg.create_task(self.highrise.teleport(
            session_metadata.user_id, Position(10.5, 2.0, 9.5, "FrontLeft")))
  
    async def on_chat(self, user: User, message: str) -> None:
  
        if message.lower().startswith("hello"):
          await self.highrise.chat("hi there")

        if message.lower().startswith("hey"):
          await self.highrise.send_whisper(user.id, "hi there")



class WebServer:
    def __init__(self):
        self.app = Flask(__name__)

        @self.app.route('/')
        def index() -> str:
            return "Alive"

    def run(self) -> None:
        self.app.run(host='0.0.0.0', port=8080)

    def keep_alive(self):
        t = Thread(target=self.run)
        t.start()


class RunBot:
    room_id = "66b1c0a5ad7e47679341f7bb"
    bot_token = "b801e2dc0eba9ed0079a3f891867d6552a86313929ef5bc4bc016127fed1fe9f"
    bot_file = "main"
    bot_class = "Bot"

    def __init__(self) -> None:
        bot_class = getattr(import_module(self.bot_file), self.bot_class)
        self.definitions = [
            BotDefinition(
                bot_class(),
                self.room_id, self.bot_token)
        ]

    def run_loop(self) -> None:
        while True:
            try:
                arun(main(self.definitions))
            except Exception as e:
                import traceback
                print("Caught an exception:")
                traceback.print_exc()
                time.sleep(1)
                continue


if __name__ == "__main__":
    WebServer().keep_alive()
    RunBot().run_loop()