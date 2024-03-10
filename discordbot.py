# インストールした discord.py を読み込む
import os
import discord
from keep_alive import keep_alive
# 自分のBotのアクセストークンに置き換えてください
TOKEN = os.environ["TOKEN"]
GUILD_ID = int(os.environ["GUILDID"])
# 接続に必要なオブジェクトを生成
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    await tree.sync(guild=discord.Object(id=GUILD_ID))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

@tree.command(name="ishikoro", description="話しかける")
@discord.app_commands.guilds(GUILD_ID)
async def talk(interaction: discord.Interaction, message: str = ""):
    if message == "":
        await interaction.response.send_message("何？")
        return
    if message in ["いぬ", "犬", "inu", "イヌ"]:
        await interaction.response.send_message("わおん")
        return
    if message in ["ねこ", "neko", "猫", "ネコ"]:
        await interaction.response.send_message("にゃーん")
        return
    await interaction.response.send_message("よくわかんねぇな")

# Botの起動とDiscordサーバーへの接続
keep_alive()
client.run(TOKEN)
