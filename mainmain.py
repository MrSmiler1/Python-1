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
from kiy import*


class Bot(BaseBot):
    def __init__(self):
        super().__init__()

    async def on_chat(self, user: User, message: str) -> None:

        if message.lower().startswith("getoutfit"):
            response = await self.highrise.get_my_outfit()
            for item in response.outfit:
                await self.highrise.chat(item.id)

        
        if message.lower().startswith("inv"):
            inventory = await self.highrise.get_inventory()
            print(inventory)

        if message.lower().startswith("rest"):
            await self.highrise.send_emote(emote_id="sit-idle-cute")
        
        if message.lower().startswith("out"):
            print(await self.highrise.get_user_outfit(user.id))

        if message.lower() == "benol":
            user_outfit = await self.highrise.get_user_outfit(user.id)
            if user_outfit and user_outfit.outfit:
                await self.highrise.set_outfit(outfit=user_outfit.outfit)
                print(f"Bot has copied the outfit of {user.username}.")

        if message.lower() == "copy":
            user_outfit = await self.highrise.get_user_outfit(user.id)
            if user_outfit and user_outfit.outfit:
                bot_inventory = await self.highrise.get_inventory()
                owned_items = {item.id for item in bot_inventory.items}  # Set of item IDs owned by the bot
                
                # Filter the user's outfit to only include items the bot owns
                wearable_outfit = [item for item in user_outfit.outfit if item.id in owned_items]
                
                if wearable_outfit:
                    await self.highrise.set_outfit(outfit=wearable_outfit)
                    print(f"Bot has copied the outfit of {user.username}, wearing {len(wearable_outfit)} items.")
                else:
                    print(f"Bot cannot wear any items from {user.username}'s outfit.")  


        if message.lower().startswith("degis2"):
            # Randomly select active color palettes
            hair_active_palette = random.randint(0, 82)
            skin_active_palette = random.randint(0, 88)
            eye_active_palette = random.randint(0, 49)
            lip_active_palette = random.randint(0, 58)
            
            # Set the outfit with randomly chosen items and color palettes
            outfit = [
                Item(type='clothing', amount=1, id='body-flesh', account_bound=False, active_palette=skin_active_palette),
                Item(type='clothing', amount=1, id=random.choice(item_shirt), account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id=random.choice(item_bottom), account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id=random.choice(item_accessory), account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id=random.choice(item_shoes), account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id=random.choice(item_freckle), account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id=random.choice(item_eye), account_bound=False, active_palette=eye_active_palette),
                Item(type='clothing', amount=1, id=random.choice(item_mouth), account_bound=False, active_palette=lip_active_palette),
                Item(type='clothing', amount=1, id=random.choice(item_nose), account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id=random.choice(item_hairback), account_bound=False, active_palette=hair_active_palette),
                Item(type='clothing', amount=1, id=random.choice(item_hairfront), account_bound=False, active_palette=hair_active_palette),
                Item(type='clothing', amount=1, id=random.choice(item_eyebrow), account_bound=False, active_palette=hair_active_palette)
            ]
            
            # Set the outfit for the character
            await self.highrise.set_outfit(outfit=outfit)


        if message.lower().startswith("buy "):
            parts = message.split(" ")
            if len(parts) != 2:
                await self.highrise.chat("Invalid command")
                return
            item_id = parts[1]
            try:
                response = await self.highrise.buy_item(item_id)
                await self.highrise.chat(f"Item bought: {response}")
            except Exception as e:
                await self.highrise.chat(f"Error: {e}")


        if message.lower().startswith("buyme"):
            try:
                # Get the outfit the user is wearing
                user_outfit = await self.highrise.get_user_outfit(user.id)
                
                # Try to buy each item in the user's outfit
                for item in user_outfit.outfit:
                    try:
                        response = await self.highrise.buy_item(item.id)
                        await self.highrise.chat(f"Bought item: {item.id}")
                    except Exception as e:
                        await self.highrise.chat(f"Failed to buy item {item.id}: {e}")
                        
            except Exception as e:
                await self.highrise.chat(f"Error while buying items: {e}")
    
    
    async def on_start(self, session_metadata: SessionMetadata) -> None:
        await self.highrise.tg.create_task(self.highrise.teleport(
            session_metadata.user_id, Position(10.5, 2.0, 9.5, "FrontLeft")))


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