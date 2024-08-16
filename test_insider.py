import pytest

from insider import GameMaster, Player


def test_お題のリストからお題を決定する():
    game_master = GameMaster()
    game_master.start(["ゲーム"])
    assert game_master.target == "ゲーム"


def test_プレイヤーAにマスターロールを割り当てる():
    game_master = GameMaster()
    player_a = Player("A")
    role_master = "master"
    roled_player = game_master.assign_role(player_a, role_master)
    assert roled_player.name == "A"
    assert roled_player.role == "master"


def test_市民のプレイヤーにロールを通知するメッセージを作成する():
    game_master = GameMaster()
    player_a = Player("A")
    master_player_a = game_master.assign_role(player_a, "master")
    message = game_master.make_message(master_player_a)
    assert message == "Your role is 'master'"


