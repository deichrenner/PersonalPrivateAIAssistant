import os
from pathlib import Path

import dotenv
import torch
from telethon import TelegramClient
from transformers import pipeline
from transformers.utils import is_flash_attn_2_available

dotenv.load_dotenv()

api_id = int(os.getenv("API_ID", 0))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
allowed_client_id = int(os.getenv("ALLOWED_CLIENT_ID", 0))

client = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)
pipe = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-large-v3",
    torch_dtype=torch.float16,
    device="mps",
    model_kwargs=(
        {"attn_implementation": "flash_attention_2"} if is_flash_attn_2_available() else {"attn_implementation": "sdpa"}
    ),
)

file_path_for_notes = Path(__file__).parent / "notes.txt"
