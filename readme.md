# Discord Twitter Space Bot

This repository contains a Discord bot that can download and transcribe Twitter Spaces.

## Features

- **Download Twitter Spaces**: Given a Twitter Space link, the bot can download the audio from the space.
- **Transcribe Audio**: After downloading a Twitter Space, the bot can transcribe the audio into text.
- **Asynchronous Processing**: The bot can handle multiple requests simultaneously.

## Installation

1. Clone this repository.

```bash
git clone https://github.com/crazydevlegend/twspace-discord-stt.git
```

2. Install the required Python packages.

```bash
pip install -r requirements.txt
```

3. Copy `.env.dev` to `.env` and set up the necessary environment variables.

```bash
# The token for your Discord bot
DISCORD_BOT_TOKEN=your-discord-bot-token
# OpenAI API key to use Whisper API
OPENAI_API_KEY="your-openai-api-key"
# (Optional) The path to the ffmpeg executable, if it's not in the PATH
FFMPEG_PATH="/path/to/ffmpeg"
```

## Usage

To start the bot, run the main script:

```bash
python main.py
```

In Discord, you can use the following commands:

- `/say <message>`: The bot will repeat whatever message you input.
- `/transpile <Twitter Space link>`: The bot will download the audio from the given Twitter Space, transcribe it into text, and send a message with the transcription when it's done.
