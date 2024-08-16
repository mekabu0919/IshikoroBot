import random


class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.role = None
        self.target = None


class GameMaster:
    def __init__(self) -> None:
        pass

    def start(self, targets: list[str]):
        self.target = random.choice(targets)

    def assign_role(self, player: Player, role: str):
        roled_player = player
        roled_player.role = role
        return roled_player
    
    def make_message(self, player: Player):
        return f"Your role is '{player.role}'"
