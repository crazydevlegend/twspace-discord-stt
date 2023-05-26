from datetime import datetime
import subprocess
import threading
import discord
import os
from discord import app_commands
import openai
import asyncio
from src import log

logger = log.setup_logger(__name__)

isPrivate = False


def download_twitter_space(url, output):
    try:
        os.environ["PATH"] += os.pathsep + os.getenv("FFMPEG_BIN_PATH")
        download_process = subprocess.Popen(
            ["twspace_dl ", "-i", url, "-o", "downloads/" + output],
        )
        download_process.wait()
        return True
    except:
        print("An exception occurred while downloading Twitter space")
        return False


def convert_audio_to_text(filename):
    try:
        audio_file = open("downloads/" + filename + ".m4a", "rb")
        transcript = openai.Audio.transcribe(
            "whisper-1",
            audio_file,
        )
        text_file = open("downloads/" + filename + ".txt", "wb")
        text_file.write(str.encode(transcript.text))
        text_file.close()
        return True
    except:
        print("An exception occurred while transcribing audio file")
        return False


def process_twitter_space(client, interaction, url):
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    message = ""
    asyncio.run_coroutine_threadsafe(
        interaction.response.send_message("Starting download..."), client.loop
    )
    downloaded = download_twitter_space(url, timestamp)
    message = "Downloaded successfully!" if downloaded else "Download failed!"
    logger.info(message)
    asyncio.run_coroutine_threadsafe(
        interaction.followup.send(message, ephemeral=True), client.loop
    )
    if not downloaded:
        return

    converted = convert_audio_to_text(timestamp)
    message = "Transcribed successfully!" if converted else "Transcription failed!"
    logger.info(message)
    asyncio.run_coroutine_threadsafe(
        interaction.followup.send(message, ephemeral=True), client.loop
    )
    if not converted:
        return

    text_file = open("downloads/" + timestamp + ".txt", "rb")
    result = f"***{url}***\n" + "```" + text_file.read().decode() + "```"
    asyncio.run_coroutine_threadsafe(
        interaction.followup.send(result, ephemeral=True), client.loop
    )


class aclient(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)


def run_discord_bot():
    client = aclient()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    openai.api_key = OPENAI_API_KEY

    @client.event
    async def on_ready():
        await client.tree.sync()
        logger.info(f"{client.user} is now running!")
        logger.info(f"{len(client.guilds)} command(s) synced!!!")

    @client.tree.command(name="say", description="Input word you want the bot say")
    async def say(interaction: discord.Interaction, *, message: str):
        username = str(interaction.user)
        channel = str(interaction.channel)
        logger.info(f"\x1b[31m{username}\x1b[0m : /say [{message}] in ({channel})")
        # await interaction.response.defer(ephemeral=True)
        # await interaction.followup.send(f"{message} @{username}")
        await interaction.response.send_message(message)
        # await interaction.channel.send(message)

    @client.tree.command(name="transpile", description="Twitter Space link")
    async def transpile(interaction: discord.Interaction, *, message: str):
        username = str(interaction.user)
        channel = str(interaction.channel)
        logger.info(
            f"\x1b[31m{username}\x1b[0m : /transpile [{message}] in ({channel})"
        )

        process_thread = threading.Thread(
            target=process_twitter_space,
            args=(
                client,
                interaction,
                message,
            ),
        )
        process_thread.start()

    TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    client.run(TOKEN)
