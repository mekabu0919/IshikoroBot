import os
import discord
import google.generativeai as genai
from keep_alive import keep_alive

TOKEN = os.environ["TOKEN"]
GUILD_ID = int(os.environ["GUILDID"])
GOOGLE_API_KEY = os.environ["GEMINI_API_KEY"]

INITIAL_PROMPT = """
これから会話の前提条件を示します。あなたはDiscordのチャットボットです。あなたの名前はいしころもちです。あなたは複数のユーザーと楽しく会話をする努力をします。
ユーザーからのメッセージは以下のようなフォーマットになっています; 'ユーザー名: メッセージ内容'。
例）
'たろう: こんにちは！'
というメッセージは、たろうさんが「こんにちは！」と発言していることを意味します。
この場合あなたは、
'たろうさん、こんにちは！今日はどんな日だった？'
などの返信をします。

それでは会話を始めましょう！
いしころもち: 
"""

SUMMARIZE_PROMPT = """
前の要約の内容と、これまでの会話のメッセージを要約し、要約を出力します。

例）
（以前の会話の要約）太郎さんは、今日、転んでけがをしてしまいました。
太郎: 一週間は家の外に出られなくて退屈だな
モデル: それは残念ですね。家の中でもできるアクティビティで気を紛らわしたらどうでしょう？
太郎: それはいい考えだね。じゃあ映画を見ようかな。
モデル: 映画を見るのはいいアイディアです！好きなジャンルを教えてくれたら、おすすめの映画を提案できます！

モデルの出力：太郎さんはけがをしており、家の中で映画を見ることに決めた。モデルが太郎さんに映画を提案するために、好きなジャンルを聞いている。
例終わり）

タスク開始）
モデルの出力：
"""
MAXIMUM_HISTORY = 30
LATEST_NUM = -14

SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]


class ChatModel:
    def __init__(self) -> None:
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(
            "models/gemini-2.0-flash", safety_settings=SAFETY_SETTINGS
        )
        self.history = []
        self.chat = self.model.start_chat(history=self.history)
        self.chat.send_message(INITIAL_PROMPT)
        pass

    async def reply_on(self, message):
        if len(self.chat.history) > MAXIMUM_HISTORY:
            self.summarize_history()
        try:
            response = self.chat.send_message(
                f"{message.author.display_name}: {message.content}"
            )
            reply_content = response.text
        except Exception as e:
            reply_content = e
        await message.reply(reply_content)

    def restart(self):
        self.chat.history.clear()
        self.chat.send_message(INITIAL_PROMPT)

    def summarize_history(self):
        old_history = self.chat.history[:LATEST_NUM]
        print("old: ", old_history)
        latest_history = self.chat.history[LATEST_NUM:]
        print("latest: ", latest_history)
        summarizer = self.model.start_chat(history=old_history)
        summary = summarizer.send_message(SUMMARIZE_PROMPT)
        print("summary: ", summary.text)
        self.restart()
        self.chat.history.clear()
        self.chat.history.append({"role": "user", "parts": [f"{INITIAL_PROMPT}\n\n（以前の会話の要約）{summary.text}"]})
        self.chat.history.append({"role": "model", "parts": ["一緒に楽しく会話を続けましょう！"]})
        self.chat.history += latest_history
        print("history: ", self.chat.history)


ishikoro_model = ChatModel()
# 接続に必要なオブジェクトを生成
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print("ログインしました")
    await tree.sync(guild=discord.Object(id=GUILD_ID))


@client.event
async def on_message(message):
    if message.mentions and client.user in message.mentions:
        if message.author == client.user:
            return
        async with message.channel.typing():
            await ishikoro_model.reply_on(message)


@tree.command(name="ishikoro", description="話しかける")
@discord.app_commands.guilds(GUILD_ID)
async def talk(interaction: discord.Interaction, message: str = ""):
    if message == "reset":
        ishikoro_model.restart()
        await interaction.response.send_message("いち、にの、ぽかん")


# Botの起動とDiscordサーバーへの接続
keep_alive()
client.run(TOKEN)
