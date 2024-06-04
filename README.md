# Personal Private Telegram AI Assistant

This is the code repository which accompanies the article "How I built a personal Telegram AI Assistant in an Afternoon"
on medium. Find the article [here](https://medium.com/@k.hueck).

## Run the Bot

Clone the project

```bash
  git clone https://github.com/deichrenner/PersonalPrivateAIAssistant.git
```

Create a virtual environment

```bash
  python3 -m venv .venv
```

Activate the virtual environment

```bash
  source .venv/bin/activate
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Install ollama 

```bash 
  curl https://ollama.ai/install.sh | sh 
  ollama serve
```

Get the Telegram API token from the @BotFather and the API hash from the Telegram online center 
(see medium article for details) and add it to the .env file.

Start the Telegram bot

```bash
  python bot.py
```

  
## Environment Variables

To run this project, you will need to add the required environment variables to the .env file. Copy the contents of the 
.env.example file and add the required API keys and tokens.