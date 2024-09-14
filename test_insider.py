from unittest.mock import MagicMock
import pytest
from discord import User
from insider import GameMaster, Player


@pytest.fixture
def game_master():
    def mock_user(id: int, name: str):
        user = MagicMock(spec=User)
        user.id = id
        user.name = name
        return user
    gamemaster = GameMaster()
    users = [mock_user(id, name) for id, name in zip([0, 1, 2, 3], "ABCD")]
    gamemaster.add(*users)
    return gamemaster


def test_複数のユーザーを入力として受け取りプレイヤーに登録する(game_master):
    assert game_master.players[0].user.id == 0
    assert game_master.players[1].user.id == 1


def test_お題のリストからお題を決定する(game_master):
    game_master.select_target(["ゲーム"])
    assert game_master.target == "ゲーム"


def test_プレイヤーAにマスターロールを割り当てる(game_master):
    roled_player = game_master.players[0].assign_role("master")
    assert roled_player.user.id == 0
    assert roled_player.role == "master"


def test_市民のプレイヤーにロールを通知するメッセージを作成する(game_master):
    villager_player = game_master.players[0].assign_role("市民")
    message = game_master.make_message(villager_player)
    assert message == "Your role is '市民'"


def test_市民以外のプレイヤーにロールとお題を通知するメッセージを作成する(game_master):
    game_master.select_target(["ゲーム"])
    insider_playaer = game_master.players[0].assign_role("インサイダー")
    message = game_master.make_message(insider_playaer)
    assert message == "Your role is 'インサイダー'. The target is 'ゲーム'"


def test_プレイヤーリストを並び替えてmasterインサイダー市民を割り当てる(game_master):
    game_master.shuffle_roles()
    assert game_master.players[0].role == "master"
    assert game_master.players[1].role == "インサイダー"
    assert game_master.players[2].role == "市民"
