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
        self.active_games = {}  # Store active games



    async def on_chat(self, user: User, message: str, whisper: bool = False) -> None:
        
        # Handle both whisper and public chat commands
        await self.handle_game_action(user, message)

        if message.lower().startswith("!invite @"):
            target_username = message.split("@")[1].strip()

            # Odadaki kullanıcıları al
            response = await self.highrise.get_room_users()
            users = [content[0] for content in response.content]  # Kullanıcı objelerini ayıkla
            usernames = [user.username.lower() for user in users]

            # Kullanıcıyı kontrol et
            if target_username.lower() not in usernames:
                return  # Hedef kullanıcı odada değilse çık

            # Kullanıcı ID'sini al
            user_id = next((u.id for u in users if u.username.lower() == target_username.lower()), None)
            if not user_id:
                return  # Kullanıcı ID'si bulunamadıysa çık

            # Daveti gönder
            await self.send_invitation(user, next((u for u in users if u.username.lower() == target_username.lower()), None))
            await self.handle_game_action(user, message)
    
    async def send_invitation(self, requester: User, target_user: User):
        """Send an invitation to another player to play XOX."""
        if requester.username in self.active_games or target_user.username in self.active_games:
            await self.highrise.send_whisper(requester.id, "Either you or the target user is already in a game.")
            return

        # Whisper to the target user
        await self.highrise.send_whisper(
            target_user.id,
            f"Do you want to accept @{requester.username}'s invite? Yes or no (y/n)"
        )

        print(f"Invitation sent from {requester.username} to {target_user.username}")

        # Store the invitation context under both users
        self.active_games[requester.username] = {
            "state": "waiting_acceptance",
            "opponent": target_user,
            "requester": requester,
            "board": None
        }

        self.active_games[target_user.username] = self.active_games[requester.username]

    async def handle_game_action(self, user: User, message: str):
        """Handle game actions such as move acceptance or actual gameplay."""
        game = next(
            (g for g in self.active_games.values() if g["requester"].username == user.username or g["opponent"].username == user.username),
            None
        )

        if game:
            print(f"Handling action for {user.username}, message: {message}, game state: {game['state']}")

            # If the game state is waiting for acceptance
            if game["state"] == "waiting_acceptance" and user.username == game["opponent"].username:
                print(f"Detected invitation response from {user.username}: {message}")
                if message.lower() == "y":
                    await self.start_game(game["requester"], game["opponent"])
                elif message.lower() == "n":
                    await self.highrise.send_whisper(game["requester"].id, f"@{user.username} declined your invite.")
                    del self.active_games[game["requester"].username]
                    del self.active_games[game["opponent"].username]
                return

            # Handle actual gameplay
            elif game["state"] == "playing":
                await self.process_move(user, message)

    async def start_game(self, player1: User, player2: User):
        """Start the XOX game, assign symbols, and initialize the game board."""
        print(f"Starting game between {player1.username} and {player2.username}")
        players = [player1, player2]
        random.shuffle(players)
        player_x, player_o = players

        game_data = {
            "state": "playing",
            "players": {player_x.username: "X", player_o.username: "O"},
            "turn": player_x.username,  # X starts the game
            "board": [" "] * 9,
            "start_time": time.time(),
            "move_timeout": 30,
        }

        self.active_games[player1.username] = game_data
        self.active_games[player2.username] = game_data

        await self.highrise.send_whisper(player1.id, f"Game started! You are {'X' if player_x.username == player1.username else 'O'}")
        await self.highrise.send_whisper(player2.id, f"Game started! You are {'X' if player_x.username == player2.username else 'O'}")

        await self.display_board(player1, player2, game_data)

        # Start the first turn timeout
        await self.start_turn_timeout(player_x, player_o, game_data)

    async def start_turn_timeout(self, player_x: User, player_o: User, game_data):
        """Handle turn timeouts. If no move is made within 30 seconds, the game ends."""
        while game_data["state"] == "playing":
            current_player = game_data["turn"]
            print(f"Waiting for move from {current_player}")
            await asyncio.sleep(game_data["move_timeout"])

            # Check if a move was made
            if game_data["turn"] == current_player:
                loser = player_x if current_player == player_x.username else player_o
                winner = player_o if loser == player_x else player_x

                print(f"Timeout! {loser.username} took too long.")
                await self.end_game(winner, loser, game_data, timeout=True)
                break

    async def process_move(self, player: User, message: str):
        """Process the move from the player and update the board."""
        game_data = self.active_games[player.username]
        symbol = game_data["players"][player.username]

        print(f"Processing move from {player.username}, message: {message}")

        # Ensure it's the player's turn
        if game_data["turn"] != player.username:
            await self.highrise.send_whisper(player.id, "It's not your turn!")
            print(f"{player.username} tried to move out of turn.")
            return

        # Validate move (ensure message is a number between 1 and 9)
        try:
            move = int(message.strip())
            if move < 1 or move > 9 or game_data["board"][move - 1] != " ":
                await self.highrise.send_whisper(player.id, "Invalid move. Try again.")
                print(f"{player.username} made an invalid move: {move}")
                return
        except ValueError:
            await self.highrise.send_whisper(player.id, "Please enter a number between 1 and 9.")
            print(f"{player.username} sent invalid input: {message}")
            return

        # Make the move
        game_data["board"][move - 1] = symbol

        # Switch turns
        next_turn = [p for p in game_data["players"] if p != player.username][0]
        game_data["turn"] = next_turn

        # Display updated board
        opponent = [p for p in game_data["players"] if p != player.username][0]
        await self.display_board(player, opponent, game_data)

        # Check for win or draw
        winner = self.check_winner(game_data["board"])
        if winner:
            winner_user = player if symbol == winner else opponent
            loser_user = opponent if winner_user == player else player
            await self.end_game(winner_user, loser_user, game_data)
        elif " " not in game_data["board"]:
            await self.end_game(None, None, game_data)  # Draw

    async def display_board(self, player1: User, player2: User, game_data):
        """Send the current board to both players."""
        board = game_data["board"]
        formatted_board = (
            f"{board[0]} | {board[1]} | {board[2]}\n"
            "---------\n"
            f"{board[3]} | {board[4]} | {board[5]}\n"
            "---------\n"
            f"{board[6]} | {board[7]} | {board[8]}"
        )
        await self.highrise.send_whisper(player1.id, formatted_board)
        await self.highrise.send_whisper(player2.id, formatted_board)
        print(f"Current board:\n{formatted_board}")

    def check_winner(self, board):
        """Check if there's a winner."""
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        for a, b, c in win_conditions:
            if board[a] == board[b] == board[c] and board[a] != " ":
                print(f"We have a winner: {board[a]}")
                return board[a]  # Return the winning symbol ('X' or 'O')
        return None

    async def end_game(self, winner, loser, game_data, timeout=False):
        """End the game, announce the winner and clean up."""
        if timeout:
            await self.highrise.chat(f"Game over! @{loser.username} took too long to move. @{winner.username} wins!")
            print(f"Game over due to timeout. {winner.username} wins!")
        elif winner:
            await self.highrise.chat(f"@{winner.username} has won against @{loser.username} in the XOX game and gained 5 points!")
            print(f"Game over. {winner.username} wins against {loser.username}!")
        else:
            await self.highrise.chat("It's a draw!")
            print("Game ended in a draw.")

        # Clean up active games
        for player in game_data["players"]:
            del self.active_games[player]


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
    room_id = "66b1c0a5ad7e47679341f7bb"  # Replace with your room ID
    bot_token = "b801e2dc0eba9ed0079a3f891867d6552a86313929ef5bc4bc016127fed1fe9f"  # Replace with your bot token
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