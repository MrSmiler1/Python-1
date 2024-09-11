from highrise import *
from highrise.models import *
import os
import importlib.util
from typing import Any, Literal, List
from datetime import datetime
from highrise import (
    BaseBot,
    ChatEvent,
    Highrise,
    __main__,
    UserJoinedEvent,
    UserLeftEvent,
)
from highrise.models import (
    AnchorPosition,
    ChannelEvent,
    ChannelRequest,
    ChatEvent,
    ChatRequest,
    CurrencyItem,
    EmoteEvent,
    EmoteRequest,
    Error,
    FloorHitRequest,
    GetRoomUsersRequest,
    GetWalletRequest,
    IndicatorRequest,
    Item,
    Position,
    Reaction,
    ReactionEvent,
    ReactionRequest,
    SessionMetadata,
    TeleportRequest,
    TipReactionEvent,
    User,
    UserJoinedEvent,
    UserLeftEvent,
    MoveUserToRoomRequest,
    ModerateRoomRequest
)
from quattro import TaskGroup
from asyncio import run as arun
from asyncio import Queue
from typing import Any
from webserver import keep_alive
import requests
import random
import asyncio
import os
import importlib
moderators: List[str] = ["lordboi", "karainek", "broberry", "_adelia_", "_M.O.B.I.N.A_", "_NIGHTxKING_", "inek.harun", "_Yojya", "nightblue_1", "dilenenbot", "_Frowee"]
class BotDefinition:
    def __init__(self, bot, room_id, api_token, *args, **kwargs):
        self.bot = bot
        self.room_id = room_id
        self.api_token = api_token 
        super().__init__(*args, **kwargs)
        self.is_teleporting_dict = {}
        self.emote_looping = False
      
emote_mapping = {
    "angry": "emoji-angry",
    "bow": "emote-bow",
    "casual": "idle-dance-casual",
    "celebrate": "emoji-celebrate",
    "charging": "emote-charging",
    "confused": "emote-confused",
    "cursing": "emoji-cursing",
    "curtsy": "emote-curtsy",
    "cutey": "emote-cutey",
    "dotheworm": "emote-snake",
    "emotecute": "emote-cute",
    "energyball": "emote-energyball",
    "enthused": "idle-enthusiastic",
    "fashion": "emote-fashionista",
    "flex": "emoji-flex",
    "float": "emote-float",
    "frog": "emote-frog",
    "gagging": "emoji-gagging",
    "gravity": "emote-gravity",
    "greedy": "emote-greedy",
    "hello": "emote-hello",
    "hot": "emote-hot",
    "icecream": "dance-icecream",
    "kiss": "emote-kiss",
    "kpop": "dance-blackpink",
    "laugh": "emote-laughing",
    "lust": "emote-lust",
    "macarena": "dance-macarena",
    "maniac": "emote-maniac",
    "model": "emote-model",
    "no": "emote-no",
    "pennywise": "dance-pennywise",
    "pose1": "emote-pose1",
    "pose3": "emote-pose3",
    "pose5": "emote-pose5",
    "pose7": "emote-pose7",
    "pose8": "emote-pose8",
    "punk": "emote-punkguitar",
    "russian": "dance-russian",
    "sad": "emote-sad",
    "sayso": "idle-dance-tiktok4",
    "shopping": "dance-shoppingcart",
    "shy": "emote-shy",
    "singalong": "idle_singing",
    "sit": "idle-loop-sitfloor",
    "snowangel": "emote-snowangel",
    "snowball": "emote-snowball",
    "superpose": "emote-superpose",
    "swordfight": "emote-swordfight",
    "telekinesis": "emote-telekinesis",
    "teleport": "emote-teleporting",
    "thumbs up": "emoji-thumbsup",
    "tiktok10": "dance-tiktok10",
    "tiktok2": "dance-tiktok2",
    "tiktok8": "dance-tiktok8",
    "tiktok9": "dance-tiktok9",
    "tired": "emote-tired",
    "uwu": "idle-uwu",
    "wave": "emote-wave",
    "weird": "dance-weird",
    "wrong": "dance-wrong",
    "yes": "emote-yes",
    "zerogravity": "emote-astronaut",
    "zombierun": "emote-zombierun",
    "zero": "emote-astronaut",
    "enth": "idle-enthusiastic",
    "penny": "dance-pennywise",
    "zombie": "emote-zombierun",
    "fight": "emote-swordfight",
    "sing": "idle_singing",
    "guitar": "emote-punkguitar",
    "gitar": "emote-punkguitar",
    "yilan": "emote-snake",
    "uçur": "emote-float",
    "dondurma": "dance-icecream",
    "manyak": "emote-maniac",
    "yılan": "emote-snake",
    "energy": "emote-energyball",
    "rasengan": "emote-energyball",
    "grave": "dance-weird",
    "özi": "dance-russian",
    "savage": "dance-tiktok8",
    "donot": "dance-tiktok2",
    "dontstartnow": "dance-tiktok2",
    "shuffle": "dance-tiktok10",
    "shuffledance": "dance-tiktok10",
    "viralgroove": "dance-tiktok9",
    "viral": "dance-tiktok9",
    "penguen": "dance-pinguin",
    "penguin": "dance-pinguin",
    "rock": "idle-guitar",
    "stars": "emote-stargazer",
    "dizzy": "emoji-dizzy",
    "rabia": "dance-tiktok2",
    "inek": "idle-guitar",
    "lordboi": "dance-tiktok10",
    "_adelia_": "idle-dance-tiktok4",
    "broberry": "emote-bow",
    "ali": "emote-astronaut",
    "harun": "dance-tiktok10",
    "sum": "emote-bow",
    "süm": "emote-bow",
    "kuzu": "idle-dance-tiktok4",
    "mobi": "emote-model",
    "boxer": "emote-boxer",
    "creepy": "dance-creepypuppet",
    "anime": "dance-anime",
    "puppet": "dance-creepypuppet",
    "try": "emote-watchurback",
    "berke": "idle-dance-casual",
    "meral": "emote-gravity",
    "duck": "dance-duckwalk",
    "deca": "sit-idle-cute",
    "ruh": "emote-creepycute",
    "kafasiz": "emote-headblowup",
    "kafasız": "emote-headblowup",
    "revelations": "emote-headblowup",
    "watchyourback": "emote-creepycute",
    "creepycute": "emote-creepycute",
    "ipek": "emote-curtsy",
    "cik": "emote-shy2",
    "sevimli": "emote-shy2",
    "shy2": "emote-shy2",
    "bashful": "emote-shy2",
    "shrink": "emote-shrink"
}

class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        self.target_room_id = "6510519bef2d56a7ddd1391d"
        self.is_teleporting_dict = {}
        self.emote_looping = False
        self.user_emote_loops = {}
        self.following_user = None
        self.following_user_id = None
        self.kus = {}
    dancs = ["emote-lust","dance-macarena","dance-tiktok8","dance-blackpink","emote-model","dance-tiktok2","dance-pennywise","emote-bow","dance-russian","emote-curtsy","emote-hot","emote-snowangel","emote-charging","dance-shoppingcart","emote-confused","idle-enthusiastic","emote-telekinesis","emote-float","emote-teleporting","emote-swordfight","emote-maniac","emote-energyball","emote-snake","idle singing","emote-frog","emote-superpose","emote-cute","dance-tiktok9","dance-weird","dance-tiktok 10","emote-pose7","emote-pose8","idle-dance-casual","emote-pose1","emote-pose3","emote-pose5","emote-cutey","emote-punkguitar","emote-zombierun","emote-fashionista","emote-gravity","dance-icecream","dance-wrong","idle-uwu","idle-dance-tiktok4"]
    reactions = ["heart","clap","thumbs","wink","wave"]
    emotes = ["idle-fighter","idle_singing","emote-teleporting","emote-embarrassed","emote-frustrated","emote-slap","emote-roll","emote-rofl","emote-superpunch","emote-kicking","dance-zombie","emote-monster_fail","emote-peekaboo","emote-sumo","emote-ninjarun","emote-proposing","emote-ropepull","emote-secrethandshake","emote-elbowbump","emote-baseball","idle-floorsleeping2","idle-floorsleeping","emote-hugyourself","emote-levelup","idle-posh","emote-apart","idle-sad","idle-angry","emote-hero","idle-hero","idle-lookup","emote-headball","emote-fail1","emote-fail2","emote-boo","emote-wings","dance-floss","emote-theatrical","emote-laughing2","emote-jetpack","emote-bunnyhop","idle_zombie","emote-death2","emote-death","emote-disco","idle_relaxed","idle-relaxed","idle_layingdown","emote-faint","emote-cold","idle-sleep","emote-handstand","emote-ghost-idle","emoji-ghost","emote-splitsdrop","dance-spiritual","dance-smoothwalk","dance-singleladies","emoji-sick","dance-sexy","dance-robotic","emoji-naughty","emoji-pray","dance-duckwalk","emote-deathdrop","dance-voguehands","dance-orangejustice","emote-heartfingers","emote-hearteyes","emote-heartshape","emoji-halo","emoji-sneeze","dance-metal","dance-aerobics","dance-martial-artist","dance-handsup","dance-breakdance","emoji-hadoken","emoji-arrogance","emoji-smirking","emoji-lying","emoji-give-up","emoji-punch","emoji-poop","emoji-there","idle-loop-annoyed","idle-loop-tapdance","idle-loop-sad","idle-loop-happy","idle-loop-aerobics","idle-dance-swinging","emote-think","emote-dissappear","emoji-scared","emoji-eyeroll","emoji-crying","emote-frollicking","emote-graceful","emoji-dizzy","emote-mindblown","emote-suckthumb","emote-peace","emote-panic","emote-jump","emote-exasperated","emote-dab","emote-gangam","emote-tapdance","emote-harlemshake","emote-robot","emote-rainbow","emote-nightfever","emote-judochop","emote-gordonshuffle","idle-dance-casual","emote-punkguitar","dance-icecream","emote-fashionista","idle-uwu","sit-idle-cute"]



    async def on_start(self, session_metadata: SessionMetadata) -> None:
        print("hi im alive?")
        self.highrise.tg.create_task(self.highrise.teleport(
            session_metadata.user_id, Position(5.5, 0.0,0.5, "FrontRight")))
    async def moderate_room(
        self,
        user_id: str,
        action: Literal["kick", "ban", "unban", "mute"],
        action_length: int | None = None,
    ) -> None:
        """Moderate a user in the room."""
  
    async def userinfo(self, user: User, target_username: str) -> None:
        user_info = await self.webapi.get_users(username=target_username, limit=1)

        if not user_info.users:
            await self.highrise.chat("Kullanıcı bulunamadı, lütfen geçerli bir kullanıcı belirtin")
            return

        user_id = user_info.users[0].user_id

        user_info = await self.webapi.get_user(user_id)

        number_of_followers = user_info.user.num_followers
        number_of_friends = user_info.user.num_friends
        country_code = user_info.user.country_code
        outfit = user_info.user.outfit
        bio = user_info.user.bio
        active_room = user_info.user.active_room
        crew = user_info.user.crew
        number_of_following = user_info.user.num_following
        joined_at = user_info.user.joined_at.strftime("%d/%m/%Y %H:%M:%S")

        joined_date = user_info.user.joined_at.date()
        today = datetime.now().date()
        days_played = (today - joined_date).days

        last_login = user_info.user.last_online_in.strftime("%d/%m/%Y %H:%M:%S") if user_info.user.last_online_in else "Son giriş bilgisi mevcut değil"

        await self.highrise.chat(f"""Kullanıcı adı: {target_username}\nTakipçi sayısı: {number_of_followers}\nArkadaş sayısı: {number_of_friends}\nTakip ettiği kişi sayısı: {number_of_following}\nOyuna ilk girdiği tarih: {joined_at}\nOyuna son girdiği tarih: {last_login}\nOyuna başladığından itibaren geçen gün sayısı: {days_played}""")

    async def follow(self, user: User, message: str = ""):
        self.following_user = user  
        while self.following_user == user:
            room_users = (await self.highrise.get_room_users()).content
            for room_user, position in room_users:
                if room_user.id == user.id:
                    user_position = position
                    break
            if user_position is not None and isinstance(user_position, Position):
                nearby_position = Position(user_position.x + 1.0, user_position.y, user_position.z)
                await self.highrise.walk_to(nearby_position)
            
            await asyncio.sleep(0.5)
  
    async def on_reaction(self, user: User, reaction: Reaction, receiver: User) -> None:
        text_to_emoji = {
            "wink": "Çok tatlısın 😉🤭",
            "wave": "Merhaba efendim 👋🏻",
            "thumbs": "Peki efendim 👍🏻",
            "heart": "Seni seviyorum ❤️",
            "clap": "Bravo 👏🏻",
        }
        
        # "buzagi" adlı oyuncunun adını kontrol edin
        if receiver.username != "inek.harun":
            await self.highrise.chat(f"\n@{user.username} {text_to_emoji[reaction]} @{receiver.username}")
            await self.highrise.send_emote(emote_id=random.choice(self.emotes))


    async def on_message(self, user_id: str, conversation_id: str, is_new_conversation: bool) -> None:
        response = await self.highrise.get_messages(conversation_id)
        if isinstance(response, GetMessagesRequest.GetMessagesResponse):
            message = response.messages[0].content
            print(message)

        if message == "Selam":
            await self.highrise.send_message(conversation_id, "aleyküm selam")
  
    async def on_user_join(self, user: User) -> None:  
        if user.username in ["Yes.CK", "Muzisn", "CaG"]:
            await self.move_user_to_target_room(user.id)
        if user.username == "ciomany":
            # Sürekli olarak bir emote göndermek için bir döngü başlatın
            while True:
                try:
                    await self.highrise.send_emote(emote_id="idle-uwu", target_user_id=user.id)
                    await asyncio.sleep(1)  # Her 60 saniyede bir gönder
                except Exception as e:
                    print(f"Emote gönderilirken hata oluştu: {e}")

        if user.username == "karainek":
            response = f"ʙᴇʏʟᴇʀ ᴏᴅᴀɴɪɴ ᴍᴜᴛʟᴜʟᴜᴋ ᴋᴀʏɴᴀɢ̆ɪ ʏᴀɴɪ̇ ᴛᴀʙɪ̇ɪ̇ ᴋɪ̇ ɪ̇ɴᴇᴋ ᴀᴍᴄᴀᴍ ɢᴇʟᴅɪ̇🥰 @ᴋᴀʀᴀɪ̇ɴᴇᴋ!"
        elif user.username == "broberry":
            response = f"Vay vay vay! Odanın güzellik kaynağı süm teyzem geldi! @broberry"
        elif user.username == "_adelia_":
            response = f"Hoş geldin odanın tatlı kaynağı kuzu! @_adelia_"
        elif user.username == "_M.O.B.I.N.A_":
            response = f"Hoş geldin güzeller güzeli mobi halam! @_M.O.B.I.N.A_"
        elif user.username == "lordboi":
            response = f"Ooo babam geldi hoş geldi! @lordboi"
        elif user.username == "_NIGHTxKING_":
            response = f"Babamın sana selamı var aliço! Hoş geldin! @_NIGHTxKING_"
        else:
            response = random.choice([f"Aramızda olman için çok bekledik. Sonunda, zaman geldi. Bugün bize katılmanız için sizi büyük bir memnuniyetle karşılıyoruz! @{user.username}", f"Sevgili dostum, hoşgeldin! Yokluğunda sensiz hiçbir şey eskisi gibi değildi! @{user.username}", f"Ekibimize hoş geldiniz! Bize katıldığınız için mutluyuz. @{user.username}", f"Hoş geldin! Varlığınız çok önemliymiş gibi sizi ağırlamaktan onur duyuyoruz! @{user.username}", f"Hoş geldin! Odamızda konforlu bir konaklama geçirmeniz için sizi büyük bir zevkle selamlıyoruz! Hep birlikte oldukça keyifli vakit geçireceğimiz kesin! @{user.username}", f"Hoş geldin! Amcam ineği tanıyor musun?@{user.username}"])

        await self.highrise.chat(response)
        await self.highrise.send_emote(emote_id = random.choice(self.emotes))

        try:
            if user.username == "dilenenbot":
                await self.highrise.send_whisper("65476a7e09ea7b45e11807bf", "!beg")
        except Exception as e:
            print(f"Error in on_user_join: {e}")

        if user.username == "Muzisuuun":
            await self.highrise.teleport(user.id, Position(4.5, 0.0, 0.5))
            await self.highrise.chat("inek.harun'a karşı işlediğin suçlardan dolayı cezalandırılacaksın")
            await asyncio.sleep(3)
            for _ in range(40):
                await self.highrise.teleport(user.id, Position(random.randint(0, 15), random.randint(0, 15), random.randint(0, 15)))
            await self.highrise.teleport(user.id, Position(4.5, 0.0, 0.5))
            await self.highrise.chat("inek.harun'a karşı işlediğin suçlardan dolayı 5 saniye içinde odadan kovulacaksın")
            await asyncio.sleep(3)

            # Kullanıcıyı odadan kovma işlemi
            room_users = (await self.highrise.get_room_users()).content
            for room_user, pos in room_users:
                if room_user.username.lower() == user.username.lower():
                    user_id = room_user.id
                    break

            if "user_id" not in locals():
                await self.highrise.chat("Bu kişi odada değil ki!?")
                return

            try:
                await self.highrise.moderate_room(user_id, "kick")
            except Exception as e:
                await self.highrise.chat(f"{e}")

    async def on_user_leave(self, user: User):
        special_users = ["karainek", "_m.o.b.i.n.a_", "broberry", "_adelia_", "_nightxking_", "lordboi"]
        if user.username.lower() in special_users:
            farewell_message = f"Hoşçakal güzel arkadaşım @{user.username}!"
        else:
            farewell_message = f"Görüşürüz @{user.username}!"
        
        await self.highrise.chat(farewell_message)
        await                        self.highrise.send_emote(emote_id = random.choice(self.emotes))

    async def move_users_to_target_room(self):
        # Odadaki herkesi hedef odaya taşıma işlemi
        room_users = (await self.highrise.get_room_users()).content

        for room_user, _ in room_users:
            if room_user.username.lower() != "inek.harun":
                await self.highrise.move_user_to_room(room_user.id, self.target_room_id)
    async def move_user_to_target_room(self, user_id: str):
        # Kullanıcıyı hedef odaya taşıma işlemi
        await self.highrise.move_user_to_room(user_id, self.target_room_id)

    async def on_tip(self, sender: User, receiver: User, tip: CurrencyItem | Item) -> None:
        message = f"{sender.username} tarafından {receiver.username} kişine {tip.amount} altın bağış yapıldı."
        await self.highrise.chat(message)

     
    async def handle_emote_command(self, user_id: str, emote_name: str) -> None:
        if emote_name in emote_mapping:
            emote_to_send = emote_mapping[emote_name]
            
            try:
                await self.highrise.send_emote(emote_to_send, user_id)
            except Exception as e:
                print(f"Error sending emote: {e}")

      
    async def teleport(self, user: User, position: Position):
        try:
            await self.highrise.teleport(user.id, position)
        except Exception as e:
            print(f"Caught Teleport Error: {e}")

    async def teleport_to_user(self, user: User, target_username: str) -> None:
        try:
            room_users = await self.highrise.get_room_users()
            for target, position in room_users.content:
                if target.username.lower() == target_username.lower():
                    z = position.z
                    new_z = z - 1
                    await self.teleport(user, Position(position.x, position.y, new_z, position.facing))
                    break
        except Exception as e:
            print(f"An error occurred while teleporting to {target_username}: {e}")

    async def teleport_user_next_to(self, target_username: str, requester_user: User) -> None:
        try:
            # Get the position of the requester_user
            room_users = await self.highrise.get_room_users()
            requester_position = None
            for user, position in room_users.content:
                if user.id == requester_user.id:
                    requester_position = position
                    break

            # Find the target user and their position
            for user, position in room_users.content:
                if user.username.lower() == target_username.lower():
                    z = requester_position.z
                    new_z = z + 1  # Example: Move +1 on the z-axis (upwards)
                    await self.teleport(user, Position(requester_position.x, requester_position.y, new_z, requester_position.facing))
                    break
        except Exception as e:
            print(f"An error occurred while teleporting {target_username} next to {requester_user.username}: {e}")
          
    async def on_whisper(self, user: User, message: str) -> None:
        """On a received room whisper."""
        if message.startswith('') and user.username in ["karainek", "_M.O.B.I.N.A_", "broberry", "_adelia_", "_NIGHTxKING", "lordboi", "Bulutt" ,"_Frowee"]:
            try:
                xxx = message[0:]
                await self.highrise.chat(xxx)
                await self.highrise.send_emote(emote_id = random.choice(self.emotes))
            except:
                print("error 3") 
              
    async def start_emote_loop(self, user_id: str, emote_name: str) -> None:
        if emote_name in emote_mapping:
            self.user_emote_loops[user_id] = emote_name  # Kullanıcının döngüsünün türünü saklayın
            emote_to_send = emote_mapping[emote_name]
            while self.user_emote_loops.get(user_id) == emote_name:  # Döngü sürdüğü sürece
                try:
                    # Emote göndermeye çalışın
                    await self.highrise.send_emote(emote_to_send, user_id)
                except Exception as e:
                    # Hedef kullanıcı odada değilse bu hatayı yakalayın
                    if "Target user not in room" in str(e):
                        print(f"{user_id} odada değil, emote gönderme durduruluyor.")
                        break  # Döngüyü durdurun
                await asyncio.sleep(1)  # Ayarlamak istediğiniz gecikmeyi kullanın

    async def stop_emote_loop(self, user_id: str) -> None:
        # Kullanıcının döngüsünü durdur
        if user_id in self.user_emote_loops:
            self.user_emote_loops.pop(user_id)
            await self.highrise.send_whisper(user_id, "Emote döngüsü durduruldu.")
        else:
            await self.highrise.send_whisper(user_id, "Emote döngüsü zaten durdu.")

    async def on_chat(self, user: User, message: str) -> None:
        """On a received room-wide chat."""
        print(f"{user.username}: {message}")
        if message.lower() == "full kus" or message.lower() == "full kuş":
            if user.id not in self.kus:
                self.kus[user.id] = False  # Initialize "kus" state as False

            if not self.kus[user.id]:
                self.kus[user.id] = True

                try:
                    while self.kus.get(user.id, False):
                        # Kullanıcıyı rastgele bir konuma teleport et
                        kl = Position(random.randint(1, 20), random.randint(1, 20), random.randint(1, 20))
                        await self.teleport(user, kl)

                        # Tekrar teleport etmeden önce 1 saniye beklemeyi sağla
                        await asyncio.sleep(0.3)
                except Exception as e:
                    print(f"Teleport sırasında bir hata oluştu: {e}")

        if message.lower() == "dur kus" or message.lower() == "dur kuş":
            if user.id in self.kus:
                # Kullanıcının "kus" durumunu False olarak ayarla ve teleport döngüsünü durdur
                self.kus[user.id] = False
      
        if message == "!takip" and user.username in ["karainek", "lordboi", "broberry", "wisowe", "_NIGHTxKING_", "dilenenbot" ,"_Frowee"]:
            if self.following_user is not None:
                await self.highrise.chat("Şu anda başka birini takip ediyorum, sıranızı bekleyin.")
            else:
                await self.follow(user)

        if message == "!stay" and user.username in ["karainek", "lordboi", "broberry", "wisowe", "_NIGHTxKING_", "dilenenbot" ,"_Frowee"]:
            if self.following_user is not None:
                await self.highrise.chat("Takip etmeyi bıraktım.")
                self.following_user = None
            else:
                await self.highrise.chat("Şu anda kimseyi takip etmiyorum.")
      
        if message.startswith("!otur") and user.username in ["karainek", "broberry", "lordboi", "_NIGHTxKING_", "dilenenbot" ,"_Frowee"]:
            await self.highrise.walk_to(AnchorPosition('6492fe0f0000000000000374', 0))
        if message.startswith("!kalk") and user.username in ["karainek", "broberry", "lordboi", "_NIGHTxKING_", "dilenenbot" ,"_Frowee"]:
            await self.highrise.walk_to(Position(5.5, 0.0,0.5, "FrontRight"))

          
        if message.startswith("!cezalandır") and user.username in ["karainek", "broberry", "lordboi", "_NIGHTxKING_", "_M.O.B.I.N.A_", "Bulutt", "dilenenbot" ,"_Frowee"]:
            target_username = message.split("@")[-1].strip()
            # Küçük harf yaparak kullanıcı adı karşılaştırması yapın
            target_username = target_username.lower()

            if target_username != "karainek" and target_username != "inek.harun":
                room_users = (await self.highrise.get_room_users()).content
                target_user = None

                for room_user, _ in room_users:
                    # Küçük harf yaparak kullanıcı adı karşılaştırması yapın
                    if room_user.username.lower() == target_username:
                        target_user = room_user
                        break

                if target_user:
                    if target_user.id not in self.is_teleporting_dict:
                        self.is_teleporting_dict[target_user.id] = True

                        try:
                            while self.is_teleporting_dict.get(target_user.id, False):
                                kl = Position(random.randint(0, 20), random.randint(0, 20), random.randint(0, 20))
                                await self.teleport(target_user, kl)
                                await asyncio.sleep(1)
                        except Exception as e:
                            print(f"An error occurred while teleporting: {e}")

                        self.is_teleporting_dict.pop(target_user.id, None)
                        # Cezalandırma işlemi bittikten sonra kullanıcıyı belirtilen konuma ışınlama
                        final_position = Position(4.5, 0.0, 0.5, "FrontRight")
                        await self.teleport(target_user, final_position)
                    else:
                        await self.highrise.chat(f"@{target_username} zaten cezalandırılıyor.")
                else:
                    await self.highrise.chat(f"@{target_username} odada değil?!")

        if message.startswith("!dur") and user.username in ["karainek", "broberry", "lordboi", "_NIGHTxKING_", "_M.O.B.I.N.A_", "Bulutt", "dilenenbot" ,"_Frowee"]:
            target_username = message.split("@")[-1].strip()
            # Küçük harf yaparak kullanıcı adı karşılaştırması yapın
            target_username = target_username.lower()

            room_users = (await self.highrise.get_room_users()).content
            target_user = None

            for room_user, _ in room_users:
                # Küçük harf yaparak kullanıcı adı karşılaştırması yapın
                if room_user.username.lower() == target_username:
                    target_user = room_user
                    break

            if target_user:
                self.is_teleporting_dict.pop(target_user.id, None)
                await self.highrise.chat(f"@{target_username} için cezalandırma işlemi durduruldu.")
            else:
                await self.highrise.chat(f"@{target_username} odada değil >.<")

        if message.startswith("/userinfo") and user.username in["karainek"]:
            target_username = message.split("@")[-1].strip()  # Hedef kullanıcı adını al
            await self.userinfo(user, target_username)
          
        if message == "-inek":
            # Kullanıcıyı hedef odaya taşıma işlemi
            await self.move_user_to_target_room(user.id)
        if message.lower() == "herkes inek" and user.username in ["karainek", "lordboi", "_M.O.B.I.N.A_", "_NIGHTxKING_", "_adelia_", "broberry", "Bulutt", "dilenenbot" ,"_Frowee"]:
            # Sadece "karainek" veya "broberry" kullanıcıları bu işlemi gerçekleştirebilir
            await self.move_users_to_target_room()
      
        message = message.strip().lower()
        user_id = user.id

        if message.startswith("full"):
            emote_name = message.replace("full", "").strip()

            if user_id in self.user_emote_loops and self.user_emote_loops[user_id] == emote_name:
                await self.stop_emote_loop(user_id)
            else:
                await self.start_emote_loop(user_id, emote_name)
        elif message == "stop":
            if user_id in self.user_emote_loops:
                await self.stop_emote_loop(user_id)
              
        message = message.strip().lower()

        if message.startswith("!"):
            parts = message.split()
            if len(parts) < 2:
                return
            
            command = parts[0][1:]
            args = parts[1:]

            if command in emote_mapping:
                response = await self.highrise.get_room_users()
                users = [content[0] for content in response.content]
                usernames = [user.username.lower() for user in users]
                
                if len(args) < 1 or args[0][0] != "@":
                    return
                
                target_username = args[0][1:].lower()
                if target_username not in usernames:
                    return
                
                user_id = next((u.id for u in users if u.username.lower() == target_username), None)
                if not user_id:
                    return
                
                await self.handle_emote_command(user.id, command)
                await self.handle_emote_command(user_id, command)

        for emote_name, emote_id in emote_mapping.items():
            if message.lower().startswith(emote_name):
                try:
                    await self.highrise.send_emote(emote_id, user.id)
                except:
                    print(f"Emote gönderilirken bir hata oluştu: {emote_name}")     


        if message == "-dress58":
                xox = await self.highrise.set_outfit(outfit=[
                        Item(type='clothing', amount=1, id='body-flesh', account_bound=False, active_palette=1),
                        Item(type='clothing', amount=1, id='shirt-n_room22109denimjacket', account_bound=False, active_palette=-1),
                        Item(type='clothing', amount=1, id='pants-n_room12019rippedpantsblack', account_bound=False, active_palette=-1),

                        Item(type='clothing', amount=1, id='nose-n_basic2018newnose20', account_bound=False, active_palette=-1),                  
                        Item(type='clothing', amount=1, id='shoes-n_room32019chunkysneaks', account_bound=False, active_palette=-1),
                        Item(type='clothing', amount=1, id='mouth-basic2018vampteeth', account_bound=False, active_palette=-1),
                        
Item(type='clothing', amount=1, id='hair_front-n_malenew30', account_bound=False, active_palette=2),

Item(type='clothing', amount=1, id='hair_back-n_malenew30', account_bound=False, active_palette=2),

                        Item(type='clothing', amount=1, id='eye-n_basic2018zanyeyes', account_bound=False, active_palette=1),
                  
Item(type='clothing', amount=1, id='gloves-n_room32019basketball', account_bound=False, active_palette=1),

Item(type='clothing', amount=1, id='glasses-n_room12019circleframes', account_bound=False, active_palette=1),

Item(type='clothing', amount=1, id='watch-n_room32019blackwatch', account_bound=False, active_palette=1),
                        Item(type='clothing', amount=1, id='eyebrow-n_11', account_bound=False, active_palette=2)
                ])
                await self.highrise.chat(f"{xox}")
     
        if message.lstrip().startswith(("!cast")):
            response = await self.highrise.get_room_users()
            users = [content[0] for content in response.content]
            usernames = [user.username.lower() for user in users]
            parts = message[1:].split()
            args = parts[1:]

            if len(args) < 1:
                # Gerekli argümanlar eksik, bir şey yapma
                pass
            elif args[0][0] != "@":
                # İlk argüman "@" ile başlamıyorsa işlem yapma
                pass
            elif args[0][1:].lower() not in usernames:
                # İlk argüman bir kullanıcı adını tanımıyorsa işlem yapma
                pass
            else:
                user_id = next((u.id for u in users if u.username.lower() == args[0][1:].lower()), None)
                
                # Diğer işlemler için kullanıcı kimlik bilgilerini kullanabilirsiniz
                if message.startswith("!cast"):
                    await self.highrise.send_emote("emote-telekinesis", user.id)
                    await self.highrise.send_emote("emote-gravity", user_id)


      
        message = message.lower()

        teleport_locations = {
            "havuz": Position(12.5, 0.5, 11.5),
            "kapi": Position(0.5, 0.0, 0.5),
            "kapı": Position(0.5, 0.0, 0.5),
            "kuş": Position(random.randint(1, 30), random.randint(1, 30), random.randint(1, 30)),
            "kus": Position(random.randint(1, 30), random.randint(1, 30), random.randint(1, 30))
        }

        for location_name, position in teleport_locations.items():
            if message.startswith(location_name):
                try:
                    await self.teleport(user, position)
                except:
                    print("Teleportasyon sırasında hata oluştu")



        if message.startswith("dans") or message.startswith("dance"):
            try:
                emote_id = random.choice(self.dancs)
                await self.highrise.send_emote(emote_id, user.id)
            except:
                print("Dans emote gönderilirken bir hata oluştu.")

        if message.startswith("ölümüm") or message.startswith("olumum"):
            death_year = random.randint(2023, 2100)
            await self.highrise.chat(f"şᴜ ᴛᴀʀɪ̇ʜᴛᴇ ɢᴇʙᴇʀᴇᴄᴇᴋsɪ̇ɴ ᴋᴜᴢᴜᴍ: {death_year}")

        if message.startswith("nefretim"):
            hate_percentage = random.randint(1, 100)
            await self.highrise.chat(f"ʙᴇɴɪ̇ᴍ ᴇɴ ʙᴜ̈ʏᴜ̈ᴋ ɴᴇғʀᴇᴛɪ̇ᴍ sᴇɴsɪ̇ɴ ʟᴀᴋɪ̇ɴ sᴇɴɪ̇ɴ ɴᴇғʀᴇᴛ ᴏʀᴀɴɪɴ ɪ̇sᴇ: {hate_percentage}% @{user.username}")

        if message.startswith("aşkım") or message.startswith("askim"):
            love_percentage = random.randint(1, 100)
            await self.highrise.chat(f"ʙᴇɴ ᴀşᴋᴀ ɪ̇ɴᴀɴᴍᴀᴍ ᴀᴍᴀ sᴇɴɪ̇ɴ ᴀşᴋ ᴏʀᴀɴɪɴ: {love_percentage} @{user.username}")

        if message.startswith("şarkım") or message.startswith("sarkim"):
            await self.highrise.chat("ʙᴜɢᴜ̈ɴ ᴋɪ̇ ʀᴜʜ ʜᴀʟɪ̇ɴᴇ ᴜʏɢᴜɴ şᴀʀᴋɪ:")
            response = random.choice(["ᴛᴀʀᴋᴀɴ-şɪᴍᴀʀɪᴋ", "ᴇᴍɪ̇ʀᴄᴀɴ ɪ̇ɢ̆ʀᴇᴋ-ɴᴀʟᴀɴ", "ᴜ̈ᴍɪ̇ᴛ ʙᴇsᴇɴ-ɴɪ̇ᴋᴀʜ ᴍᴀsᴀsɪ", "ɪ̇ʙʀᴀʜɪ̇ᴍ ᴛᴀᴛʟɪsᴇs-ᴍᴀᴠɪşɪ̇ᴍ", "ᴍᴜ̈sʟᴜ̈ᴍ ɢᴜ̈ʀsᴇs-şᴇɴɪ̇ ʏᴀᴢᴅɪᴍ", "ᴅᴜᴍᴀɴ-ᴅɪ̇ʙɪ̇ɴᴇ ᴋᴀᴅᴀʀ", "sᴇɴᴀ şᴇɴᴇʀ-ᴘᴏʀsᴇʟᴇɴ ᴋᴀʟʙɪ̇ᴍ", "ʏᴜ̈ᴢʏᴜ̈ᴢᴇʏᴋᴇɴ ᴋᴏɴᴜşᴜʀᴜᴢ-ʙᴏş ɢᴇᴍɪ̇ʟᴇʀ", "ʏᴜ̈ᴢʏᴜ̈ᴢᴇʏᴋᴇɴ ᴋᴏɴᴜşᴜʀᴜᴢ-ᴋᴀş ɪɪ", "ᴅᴋᴛᴛ-ᴀʟᴅᴀᴛᴛɪᴍ", "ɪ̇sᴍᴀɪ̇ʟ ʏᴋ-ʙᴀs ɢᴀᴢᴀ", "ᴍᴏᴅᴇʟ-ᴘᴇᴍʙᴇ ᴍᴇᴢᴀʀʟɪᴋ", "ʙᴇʀɢᴇɴ-ʙᴇɴɪ̇ᴍ ɪ̇ᴄ̧ɪ̇ɴ ᴜ̈ᴢᴜ̈ʟᴍᴇ", "ᴇʙʀᴜ ɢᴜ̈ɴᴅᴇş-ᴅᴇᴍɪ̇ʀ ᴀᴛᴛɪᴍ ʏᴀʟɴɪᴢʟɪɢ̆ᴀ", "ʜᴇᴘsɪ̇𝟷-ʏᴀʟᴀɴ"])
            await self.highrise.chat(response)
        
        if                          message.startswith("!gotur") or message.startswith("!götür"):
          target_username =         message.split("@")[-1].strip()
          await                     self.teleport_to_user(user, target_username)
        if message.startswith("!getir"):
            target_username = message.split("@")[-1].strip()
            if target_username not in ["karainek", "inek.harun", "dilenenbot"]:
                await self.teleport_user_next_to(target_username, user)


        moderators = ["karainek", "lordboi", "broberry", "_adelia_", "_NIGHTxKING_", "_M.O.B.I.N.A_", "Bulutt", "dilenenbot" ,"_Frowee"]
        if message.startswith("kick") and user.username in moderators:
            parts = message.split()
            if len(parts) != 2:
                await self.highrise.chat("Yanlış yazıyorsun 🙂.")
                return
            if "@" not in parts[1]:
                username = parts[1]
            else:
                username = parts[1][1:]

            room_users = (await self.highrise.get_room_users()).content
            for room_user, pos in room_users:
                if room_user.username.lower() == username.lower():
                    user_id = room_user.id
                    break

            if "user_id" not in locals():
                await self.highrise.chat("Bu kişi odada değil ki!?")
                return

            try:
                await self.highrise.moderate_room(user_id, "kick")
            except Exception as e:
                await self.highrise.chat(f"{e}")
                return

            await self.highrise.chat(f"@{username}, @{user.username} tarafından odadan kovuldu 🤭")

      
        allowed_users2 = ["karainek", "lordboi", "broberry", "_adelia_", "_NIGHTxKING_", "_M.O.B.I.N.A_", "Bulutt", "dilenenbot" ,"_Frowee"]
        if message.startswith("herkes kick") and user.username in allowed_users2:
            room_users = (await self.highrise.get_room_users()).content
            for room_user, pos in room_users:
                if room_user.username.lower() not in allowed_users2:
                    try:
                        await self.highrise.moderate_room(room_user.id, "kick")
                    except Exception:
                        pass
            await self.highrise.chat("Odadaki herkes atıldı.")

      
        if message.startswith("herkes yanıma") and user.username in ["karainek", "lordboi", "broberry", "_adelia_", "_NIGHTxKING_", "_M.O.B.I.N.A_", "Bulut", "dilenenbot" ,"_Frowee"]:
            # Kullanıcılar sadece "karainek" veya "broberry" ise bu işlemi gerçekleştirebilir
            room_users = (await self.highrise.get_room_users()).content

            for room_user, _ in room_users:
                if room_user.id != user.id and room_user.username != "inek.harun":
                    # Kendi yanlarına gitmelerini istemediğimiz için kendisini hariç tutuyoruz
                    # ve "inek.harun" kullanıcısını da hariç tutuyoruz
                    await self.teleport_user_next_to(room_user.username, user)
 
          
        message = message.lower()
        allowed_users = ["karainek", "_M.O.B.I.N.A", "broberry", "_adelia_", "_NIGHTxKING_", "lordboi", "Bulut", "dilenenbot" ,"_Frowee"]

      
        if message.startswith("all ") and user.username in ["karainek", "_M.O.B.I.N.A_", "broberry", "_adelia_", "_NIGHTxKING_", "lordboi", "Bulut", "dilenenbot" ,"_Frowee"]:
            # Kullanıcının istediği emote adını alın
            emote_name = message.replace("all ", "").strip()

            # Emote adına karşılık gelen emote adını alın
            if emote_name in emote_mapping:
                emote_to_send = emote_mapping[emote_name]

                # Odadaki tüm kullanıcılara emote gönderin
                roomUsers = (await self.highrise.get_room_users()).content
                for roomUser, _ in roomUsers:
                    try:
                        await self.highrise.send_emote(emote_to_send, roomUser.id)
                    except Exception as e:
                        error_message = f"Hata oluştu: {e}"
                        await self.highrise.send_whisper(user.id, error_message)
            else:
                await self.highrise.send_whisper(user.id, "Geçersiz emote adı: {}".format(emote_name))


      
        message = message.lower()

        if user.username not in ["karainek", "_M.O.B.I.N.A_", "broberry", "_adelia_", "_NIGHTxKING_", "lordboi", "Bulut", "dilenenbot" ,"_Frowee"]:
            return  # Sadece belirli kullanıcılara izin ver

        room_users = (await self.highrise.get_room_users()).content
        
        if message.startswith("herkes kapi") or message.startswith("herkes kapı"):
            for room_user, _ in room_users:
                if room_user.username not in ["inek.harun", "karainek", "lordboi"]:
                    await self.teleport(room_user, Position(0.5, 0.0, 0.5))
        
        if message.startswith("herkes havuz"):
            for room_user, _ in room_users:
                if room_user.username not in ["inek.harun", "karainek", "lordboi"]:
                    await self.teleport(room_user, Position(12.5, 0.0, 11.0))
            
        if message.startswith("herkes havaya"):
            for room_user, _ in room_users:
                if room_user.username not in ["inek.harun", "karainek", "lordboi"]:
                    try:
                        kl = Position(random.randint(1, 30), random.randint(1, 30), random.randint(1, 30))
                        await self.teleport(room_user, kl)
                    except Exception as e:
                        print(f"An error occurred while teleporting: {e}")

        if message.startswith("!git") and user.username in ["karainek", "broberry", "lordboi", "dilenenbot" ,"_Frowee"]:
            parts = message.split()
            if len(parts) == 2 and parts[1].startswith("@"):
                target_username = parts[1][1:]
                target_user = None

                room_users = (await self.highrise.get_room_users()).content
                for room_user, _ in room_users:
                    if room_user.username.lower() == target_username:
                        target_user = room_user
                        break

                if target_user:
                    try:
                        kl = Position(random.randint(1, 30), random.randint(1, 30), random.randint(1, 30))
                        await self.teleport(target_user, kl)
                    except Exception as e:
                        print(f"An error occurred while teleporting: {e}")
                else:
                    print(f"Kullanıcı adı '{target_username}' odada bulunamadı.")

  
    async def on_channel(self, sender_id: str, message: str, tags: set[str]) -> None:
        """On a hidden channel message."""
        pass

 
    async def is_admin(self, user: User):
        if user.id == self.BOT_ADMINISTRATOR_ID and user.username == self.BOT_ADMINISTRATOR:
            return True
        if user.id == '60aa5885cacd118c1e8d875a' and user.username == 'karinek':
            return True
        return False

    async def run(self, room_id, token):
        definitions =                [BotDefinition(self, room_id, token)]
        await                        __main__.main(definitions)

keep_alive()
if __name__ == "__main__":
  room_id = ""
  token = ""
  arun(Bot().run(room_id,token))