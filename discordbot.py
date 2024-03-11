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

from litellm import completion
import os

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    await tree.sync(guild=discord.Object(id=GUILD_ID))

def message_sent(message_to_reply):
    system_message = {"role": "system", "content": "あなたは修行中のAIアシスタントです。あなたの名前はいしころもちです。", "name": "師匠"}
    user_message = {"role": "user", "content": message_to_reply.content, "name": message_to_reply.author.name}
    return [system_message, user_message]

@client.event
async def on_message(message):
    if message.mentions and client.user in message.mentions:
        if message.author == client.user:
            return
        # parts = message.content.split(' ', 1)
        # arguments = ' '.join(parts)
        response = completion(
        model="gemini/gemini-pro", 
            messages=message_sent(message))
        await message.reply(response['choices'][0]['message']['content'])

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


# Botの起動とDiscordサーバーへの接続
keep_alive()
client.run(TOKEN)
