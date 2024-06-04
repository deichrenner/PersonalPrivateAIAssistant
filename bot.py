import atexit
import logging
import os
import sys

import ollama
from telethon import events

from config import client, pipe, file_path_for_notes, allowed_client_id
from helpers import Message, store_messages, load_messages

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

user_messages = load_messages(file_path_for_notes)
atexit.register(store_messages, file_path=file_path_for_notes, data=user_messages)


@client.on(events.NewMessage())
async def handle_message(event: events.NewMessage.Event):
    user_id = event.sender_id
    if user_id != allowed_client_id:
        return

    text = event.message.message

    if event.message.voice:
        async with client.action(event.chat_id, "typing"):
            voice_path = await event.message.download_media()
            transcription = pipe(
                voice_path,
                chunk_length_s=30,
                batch_size=24,
                return_timestamps=True,
                generate_kwargs={"language": "german"},
            )
            os.unlink(voice_path)
            text = transcription["text"].strip()
            logger.info(f"Received and transcribed voice message: {text}")
            await event.respond(text)
            user_messages.append(
                Message(message_text=text, message_id=event.message.id, timestamp=event.message.date.isoformat())
            )
        await client.action(event.chat_id, "cancel")

    if text.lower().startswith("command"):
        logger.info(f"Received command: {text}")
        async with client.action(event.chat_id, "typing"):
            try:
                parts = text.split()
                n_context = int(parts[1].strip(" ,.:;"))
                command_text = " ".join(parts[2:])
            except (IndexError, ValueError):
                await event.respond("Invalid command format. Use 'command N <prompt>'.")
                return

            context = None

            if n_context > 0:
                context = "\n".join(message.message_text for message in user_messages[-n_context - 1 : -1])

            prompt = f"Anweisung: {command_text}"
            if context:
                prompt += f"\n\nKontext: {context}"
            logger.info(f"Execute command with context: {prompt}")
            response = ollama.chat(
                model="llama3:8b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant that summarizes, rephrases, corrects errors, "
                        "and much more based on context information.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
            logger.info(f"Received response from llm: {response['message']['content']}")
            await event.respond(response["message"]["content"])
        await client.action(event.chat_id, "cancel")
    else:
        logger.info(f"Received message: {text}")
        user_messages.append(
            Message(message_text=text, message_id=event.message.id, timestamp=event.message.date.isoformat())
        )


if __name__ == "__main__":
    logger.info("Bot is running...")
    client.run_until_disconnected()
