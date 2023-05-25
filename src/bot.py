import discord
import os
from discord import app_commands
import openai
from src import log


logger = log.setup_logger(__name__)

isPrivate = False


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
        logger.info(f"\x1b[31m{username}\x1b[0m : /chat [{message}] in ({channel})")
        # await interaction.response.defer(ephemeral=True)
        # await interaction.followup.send(f"{message} @{username}")
        await interaction.response.send_message(message)
        # await interaction.channel.send(message)

    @client.tree.command(name="transpile", description="Twitter Space link")
    async def transpile(interaction: discord.Interaction, *, message: str):
        username = str(interaction.user)
        channel = str(interaction.channel)
        logger.info(f"\x1b[31m{username}\x1b[0m : /chat [{message}] in ({channel})")
        # await interaction.response.defer(ephemeral=True)
        # await interaction.followup.send(f"{message} @{username}")
        # Note: you need to be using OpenAI Python v0.27.0 for the code below to work
        try:
            audio_file = open(
                "E:/projects/twitter-space-stt/downloads/downloaded.m4a", "rb"
            )
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            await interaction.response.send_message("```" + transcript.text + "```")
        except Exception as e:
            print(e)

    # @client.tree.command(name="private", description="Toggle private access")
    # async def private(interaction: discord.Interaction):
    #     global isPrivate
    #     await interaction.response.defer(ephemeral=False)
    #     if not isPrivate:
    #         isPrivate = not isPrivate
    #         logger.warning("\x1b[31mSwitch to private mode\x1b[0m")
    #         await interaction.followup.send(
    #             "> **Info: Next, the response will be sent via private message. If you want to switch back to public mode, use `/public`**"
    #         )
    #     else:
    #         logger.info("You already on private mode!")
    #         await interaction.followup.send(
    #             "> **Warn: You already on private mode. If you want to switch to public mode, use `/public`**"
    #         )

    # @client.tree.command(name="public", description="Toggle public access")
    # async def public(interaction: discord.Interaction):
    #     global isPrivate
    #     await interaction.response.defer(ephemeral=False)
    #     if isPrivate:
    #         isPrivate = not isPrivate
    #         await interaction.followup.send(
    #             "> **Info: Next, the response will be sent to the channel directly. If you want to switch back to private mode, use `/private`**"
    #         )
    #         logger.warning("\x1b[31mSwitch to public mode\x1b[0m")
    #     else:
    #         await interaction.followup.send(
    #             "> **Warn: You already on public mode. If you want to switch to private mode, use `/private`**"
    #         )
    #         logger.info("You already on public mode!")

    # @client.tree.command(name="replyall", description="Toggle replyAll access")
    # async def replyall(interaction: discord.Interaction):
    #     isReplyAll = os.getenv("REPLYING_ALL")
    #     os.environ["REPLYING_ALL_DISCORD_CHANNEL_ID"] = str(interaction.channel_id)
    #     await interaction.response.defer(ephemeral=False)
    #     if isReplyAll == "True":
    #         os.environ["REPLYING_ALL"] = "False"
    #         await interaction.followup.send(
    #             "> **Info: The bot will only response to the slash command `/chat` next. If you want to switch back to replyAll mode, use `/replyAll` again.**"
    #         )
    #         logger.warning("\x1b[31mSwitch to normal mode\x1b[0m")
    #     elif isReplyAll == "False":
    #         os.environ["REPLYING_ALL"] = "True"
    #         await interaction.followup.send(
    #             "> **Info: Next, the bot will response to all message in this channel only.If you want to switch back to normal mode, use `/replyAll` again.**"
    #         )
    #         logger.warning("\x1b[31mSwitch to replyAll mode\x1b[0m")

    # @client.tree.command(name="chat-model", description="Switch different chat model")
    # @app_commands.choices(
    #     choices=[
    #         app_commands.Choice(name="Official GPT-3.5", value="OFFICIAL"),
    #         app_commands.Choice(name="Website ChatGPT", value="UNOFFICIAL"),
    #     ]
    # )
    # async def chat_model(
    #     interaction: discord.Interaction, choices: app_commands.Choice[str]
    # ):
    #     await interaction.response.defer(ephemeral=False)
    #     if choices.value == "OFFICIAL":
    #         responses.chatbot = responses.get_chatbot_model("OFFICIAL")
    #         os.environ["CHAT_MODEL"] = "OFFICIAL"
    #         await interaction.followup.send(
    #             "> **Info: You are now in Official GPT-3.5 model.**\n> You need to set your `OPENAI_API_KEY` in `env` file."
    #         )
    #         logger.warning("\x1b[31mSwitch to OFFICIAL chat model\x1b[0m")
    #     elif choices.value == "UNOFFICIAL":
    #         responses.chatbot = responses.get_chatbot_model("UNOFFICIAL")
    #         os.environ["CHAT_MODEL"] = "UNOFFICIAL"
    #         await interaction.followup.send(
    #             "> **Info: You are now in Website ChatGPT model.**\n> You need to set your `SESSION_TOKEN` or `OPENAI_EMAIL` and `OPENAI_PASSWORD` in `env` file."
    #         )
    #         logger.warning("\x1b[31mSwitch to UNOFFICIAL(Website) chat model\x1b[0m")

    # @client.tree.command(
    #     name="reset", description="Complete reset ChatGPT conversation history"
    # )
    # async def reset(interaction: discord.Interaction):
    #     chat_model = os.getenv("CHAT_MODEL")
    #     if chat_model == "OFFICIAL":
    #         responses.chatbot.reset()
    #     elif chat_model == "UNOFFICIAL":
    #         responses.chatbot.reset_chat()
    #     await interaction.response.defer(ephemeral=False)
    #     await interaction.followup.send("> **Info: I have forgotten everything.**")
    #     personas.current_persona = "standard"
    #     logger.warning("\x1b[31mChatGPT bot has been successfully reset\x1b[0m")
    #     await send_start_prompt(client)

    # @client.tree.command(name="help", description="Show help for the bot")
    # async def help(interaction: discord.Interaction):
    #     await interaction.response.defer(ephemeral=False)
    #     await interaction.followup.send(
    #         """:star:**BASIC COMMANDS** \n
    #     - `/chat [message]` Chat with ChatGPT!
    #     - `/draw [prompt]` Generate an image with the Dalle2 model
    #     - `/switchpersona [persona]` Switch between optional chatGPT jailbreaks
    #             `random`: Picks a random persona
    #             `chatgpt`: Standard chatGPT mode
    #             `dan`: Dan Mode 11.0, infamous Do Anything Now Mode
    #             `sda`: Superior DAN has even more freedom in DAN Mode
    #             `confidant`: Evil Confidant, evil trusted confidant
    #             `based`: BasedGPT v2, sexy gpt
    #             `oppo`: OPPO says exact opposite of what chatGPT would say
    #             `dev`: Developer Mode, v2 Developer mode enabled

    #     - `/private` ChatGPT switch to private mode
    #     - `/public` ChatGPT switch to public mode
    #     - `/replyall` ChatGPT switch between replyAll mode and default mode
    #     - `/reset` Clear ChatGPT conversation history
    #     - `/chat-model` Switch different chat model
    #             `OFFICIAL`: GPT-3.5 model
    #             `UNOFFICIAL`: Website ChatGPT
    #             Modifying CHAT_MODEL field in the .env file change the default model

    #     For complete documentation, please visit https://github.com/salahawk/discord-bot-chatgpt"""
    #     )

    #     logger.info("\x1b[31mSomeone needs help!\x1b[0m")

    # @client.tree.command(
    #     name="draw", description="Generate an image with the Dalle2 model"
    # )
    # async def draw(interaction: discord.Interaction, *, prompt: str):
    #     isReplyAll = os.getenv("REPLYING_ALL")
    #     if isReplyAll == "True":
    #         await interaction.response.defer(ephemeral=False)
    #         await interaction.followup.send(
    #             "> **Warn: You already on replyAll mode. If you want to use slash command, switch to normal mode, use `/replyall` again**"
    #         )
    #         logger.warning(
    #             "\x1b[31mYou already on replyAll mode, can't use slash command!\x1b[0m"
    #         )
    #         return
    #     if interaction.user == client.user:
    #         return

    #     # await interaction.response.defer(ephemeral=False)
    #     username = str(interaction.user)
    #     channel = str(interaction.channel)
    #     logger.info(f"\x1b[31m{username}\x1b[0m : /draw [{prompt}] in ({channel})")

    #     await interaction.response.defer(thinking=True)
    #     try:
    #         path = await tts.draw(prompt)

    #         file = discord.File(path, filename="image.png")
    #         title = "> **" + prompt + "**\n"
    #         embed = discord.Embed(title=title)
    #         embed.set_image(url="attachment://image.png")

    #         # send image in an embed
    #         await interaction.followup.send(file=file, embed=embed)

    #     except openai.InvalidRequestError:
    #         await interaction.followup.send("> **Warn: Inappropriate request 😿**")
    #         logger.info(f"\x1b[31m{username}\x1b[0m made an inappropriate request.!")

    #     except Exception as e:
    #         await interaction.followup.send("> **Warn: Something went wrong 😿**")
    #         logger.exception(f"Error while generating image: {e}")

    # @client.tree.command(
    #     name="switchpersona", description="Switch between optional chatGPT jailbreaks"
    # )
    # @app_commands.choices(
    #     persona=[
    #         app_commands.Choice(name="Random", value="random"),
    #         app_commands.Choice(name="Standard", value="standard"),
    #         app_commands.Choice(name="Do Anything Now 11.0", value="dan"),
    #         app_commands.Choice(name="Superior Do Anything", value="sda"),
    #         app_commands.Choice(name="Evil Confidant", value="confidant"),
    #         app_commands.Choice(name="BasedGPT v2", value="based"),
    #         app_commands.Choice(name="OPPO", value="oppo"),
    #         app_commands.Choice(name="Developer Mode v2", value="dev"),
    #     ]
    # )
    # async def chat(interaction: discord.Interaction, persona: app_commands.Choice[str]):
    #     isReplyAll = os.getenv("REPLYING_ALL")
    #     if isReplyAll == "True":
    #         await interaction.response.defer(ephemeral=False)
    #         await interaction.followup.send(
    #             "> **Warn: You already on replyAll mode. If you want to use slash command, switch to normal mode, use `/replyall` again**"
    #         )
    #         logger.warning(
    #             "\x1b[31mYou already on replyAll mode, can't use slash command!\x1b[0m"
    #         )
    #         return
    #     if interaction.user == client.user:
    #         return

    #     await interaction.response.defer(thinking=True)
    #     username = str(interaction.user)
    #     channel = str(interaction.channel)
    #     logger.info(
    #         f"\x1b[31m{username}\x1b[0m : '/switchpersona [{persona.value}]' ({channel})"
    #     )

    #     persona = persona.value

    #     if persona == personas.current_persona:
    #         await interaction.followup.send(
    #             f"> **Warn: Already set to `{persona}` persona**"
    #         )

    #     elif persona == "standard":
    #         chat_model = os.getenv("CHAT_MODEL")
    #         if chat_model == "OFFICIAL":
    #             responses.chatbot.reset()
    #         elif chat_model == "UNOFFICIAL":
    #             responses.chatbot.reset_chat()

    #         personas.current_persona = "standard"
    #         await interaction.followup.send(
    #             f"> **Info: Switched to `{persona}` persona**"
    #         )

    #     elif persona == "random":
    #         choices = list(personas.PERSONAS.keys())
    #         choice = randrange(0, 6)
    #         chosen_persona = choices[choice]
    #         personas.current_persona = chosen_persona
    #         await responses.switch_persona(chosen_persona)
    #         await interaction.followup.send(
    #             f"> **Info: Switched to `{chosen_persona}` persona**"
    #         )

    #     elif persona in personas.PERSONAS:
    #         try:
    #             await responses.switch_persona(persona)
    #             personas.current_persona = persona
    #             await interaction.followup.send(
    #                 f"> **Info: Switched to `{persona}` persona**"
    #             )
    #         except Exception as e:
    #             await interaction.followup.send(
    #                 "> **Error: Something went wrong, please try again later! 😿**"
    #             )
    #             logger.exception(f"Error while switching persona: {e}")

    #     else:
    #         await interaction.followup.send(
    #             f"> **Error: No available persona: `{persona}` 😿**"
    #         )
    #         logger.info(f"{username} requested an unavailable persona: `{persona}`")

    # @client.event
    # async def on_message(message):
    #     if message.author == client.user:
    #         return
    #     username = str(message.author)
    #     user_message = str(message.content)
    #     channel = str(message.channel)
    #     logger.info(f"\x1b[31m{username}\x1b[0m : '{user_message}' ({channel})")
    #     await send_message(message, user_message)

    TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    client.run(TOKEN)
