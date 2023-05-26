import subprocess
import threading
import time
import discord
import os
from discord import app_commands
import openai
import asyncio
from src import log

logger = log.setup_logger(__name__)

isPrivate = False


async def audio_to_text(interaction):
    audio_file = open("./downloads/downloaded.m4a", "rb")
    transcript = openai.Audio.transcribe(
        "whisper-1",
        audio_file,
    )
    await interaction.response.send_message("```" + transcript.text + "```")


def download_twitter_space(process, interaction):
    stdout, stderr = process.communicate()  # This will block until process completes
    logger.info(f"Download completed")
    # print("Subprocess completed. Return code:", process.returncode)
    print("Output:", stdout.decode())
    print("Errors:", stderr.decode())
    asyncio.run(audio_to_text(interaction))


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

        try:
            timestamp = time.time()
            os.environ["PATH"] += os.pathsep + os.getenv("FFMPEG_BIN_PATH")
            download_process = subprocess.Popen(
                ["twspace_dl ", "-i", message, "-o", "./downloads/downloaded"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            # Start a new thread to monitor the subprocess
            monitor_thread = threading.Thread(
                target=download_twitter_space, args=(download_process, interaction)
            )
            monitor_thread.start()
        except Exception as e:
            print(e)

    TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    client.run(TOKEN)
