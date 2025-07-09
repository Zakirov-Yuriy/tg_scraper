from telethon import TelegramClient, events
from config import api_id, api_hash, group_usernames
from database import save_message
from collections import defaultdict
import os
from datetime import datetime

client = TelegramClient("tg_listener_session", api_id, api_hash)


def normalize_group_name(name: str) -> str:
    if not name:
        return "unknown"
    return name.lstrip('@').strip()


# Универсальная функция для сохранения одного медиафайла (фото, видео, аудио и т.д.) и возврата пути
async def save_media(msg):
    media_dir = "static/media"
    os.makedirs(media_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    # Определяем расширение файла по типу медиа
    if msg.photo:
        ext = "jpg"
    elif msg.video:
        ext = "mp4"
    elif msg.voice:
        ext = "ogg"
    elif msg.audio:
        ext = "mp3"
    else:
        ext = "bin"  # для прочих типов

    filename = f"{timestamp}_{msg.id}.{ext}"
    full_path = os.path.join(media_dir, filename)

    await msg.download_media(file=full_path)

    # Возвращаем относительный путь для сохранения в базе
    return os.path.join("media", filename)


# Функция для сохранения всех медиа из списка сообщений (например, альбом)
async def save_all_media(msgs):
    media_paths = []
    for msg in msgs:
        # Проверяем есть ли у сообщения медиа
        if msg.photo or msg.video or msg.voice or msg.audio:
            path = await save_media(msg)
            media_paths.append(path)
    return ",".join(media_paths) if media_paths else None


# Парсим историю сообщений из групп
async def parse_history():
    for username in group_usernames:
        group_name = normalize_group_name(username)
        print(f"📥 Загружаем историю из {group_name}")
        grouped_messages = defaultdict(list)

        async for message in client.iter_messages(username, reverse=True):
            text = message.text or "[Без текста]"
            date = message.date
            sender_id = message.sender_id

            if message.grouped_id:
                grouped_messages[message.grouped_id].append(message)
            else:
                if message.photo or message.video or message.voice or message.audio:
                    media_path = await save_all_media([message])
                    save_message(group_name, sender_id, text, date, media_path)
                else:
                    save_message(group_name, sender_id, text, date)

        # Обрабатываем альбомы (группы сообщений с media)
        for group_id, messages in grouped_messages.items():
            media_path = await save_all_media(messages)
            text = messages[0].text or "[Медиагруппа]"
            date = messages[0].date
            sender_id = messages[0].sender_id
            save_message(group_name, sender_id, text, date, media_path)


# Обработчик новых сообщений в реальном времени
@client.on(events.NewMessage(chats=group_usernames))
async def handler(event):
    msg = event.message
    text = msg.text or "[Без текста]"
    date = msg.date
    group_name = normalize_group_name(event.chat.username if event.chat else "unknown")
    sender_id = msg.sender_id

    if hasattr(msg, 'grouped_id') and msg.grouped_id:
        album_msgs = await client.get_messages(event.chat_id, limit=20)
        album_media = [m for m in album_msgs if m.grouped_id == msg.grouped_id and (m.photo or m.video or m.voice or m.audio)]
        media_path = await save_all_media(album_media)
        save_message(group_name, sender_id, text, date, media_path)
    elif msg.photo or msg.video or msg.voice or msg.audio:
        media_path = await save_all_media([msg])
        save_message(group_name, sender_id, text, date, media_path)
    else:
        save_message(group_name, sender_id, text, date)

    print(f"📩 Получено: [{date}] {group_name}: {text}")


# Основная точка входа
async def main():
    print("📥 Сначала парсим историю...")
    await parse_history()
    print("✅ История загружена. Ждём новые сообщения...")
    await client.run_until_disconnected()


with client:
    client.loop.run_until_complete(main())
