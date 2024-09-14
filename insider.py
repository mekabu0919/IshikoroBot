import random

from discord import User


class Player:
    def __init__(self, user: User) -> None:
        self.user = user
        self.role = None
        self.target = None

    def assign_role(self, role: str):
        self.role = role
        return self


class GameMaster:
    def __init__(self) -> None:
        self.players = []

    def add(self, *users: User):
        for user in users:
            player = Player(user)
            self.players.append(player)

    def select_target(self, targets: list[str]):
        self.target = random.choice(targets)

    def shuffle_roles(self):
        random.shuffle(self.players)
        self.players[0].assign_role("master")
        self.players[1].assign_role("インサイダー")
        for player in self.players[2:]:
            player.assign_role("市民")
    
    def make_message(self, player: Player):
        if player.role == "市民":
            return f"Your role is '{player.role}'"
        else:
            return f"Your role is '{player.role}'. The target is '{self.target}'"
