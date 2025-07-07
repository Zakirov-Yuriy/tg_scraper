from telethon import TelegramClient, events
from config import api_id, api_hash, group_usernames
from database import save_message
from collections import defaultdict
import os
from datetime import datetime

client = TelegramClient("tg_listener_session", api_id, api_hash)

# 📁 Функция для сохранения одного фото и возвращения пути к файлу
async def save_photo(msg):
    media_dir = "static/media"
    os.makedirs(media_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"{timestamp}_{msg.id}.jpg"
    full_path = os.path.join(media_dir, filename)

    await msg.download_media(file=full_path)

    # 🔥 сохраняем только относительный путь — media/имя.jpg
    return os.path.join("media", filename)


# Функция для сохранения всех фото из списка сообщений (альбома)
async def save_all_photos(msgs):
    media_paths = []
    for msg in msgs:
        if msg.photo:
            path = await save_photo(msg)
            media_paths.append(path)
    return ",".join(media_paths) if media_paths else None

# Парсим историю сообщений из групп
async def parse_history():
    for username in group_usernames:
        print(f"📥 Загружаем историю из {username}")
        grouped_messages = defaultdict(list)

        async for message in client.iter_messages(username, reverse=True):
            text = message.text or "[Без текста]"
            date = message.date
            sender_id = message.sender_id
            group_name = username

            if message.grouped_id:
                grouped_messages[message.grouped_id].append(message)
            else:
                if message.photo:
                    media_path = await save_all_photos([message])
                    save_message(group_name, sender_id, text, date, media_path)
                else:
                    save_message(group_name, sender_id, text, date)

        # Обрабатываем альбомы
        for group_id, messages in grouped_messages.items():
            media_path = await save_all_photos(messages)
            text = messages[0].text or "[Медиагруппа]"
            date = messages[0].date
            sender_id = messages[0].sender_id
            save_message(group_name=username, sender_id=sender_id, text=text, date=date, media_path=media_path)

# Обработчик новых сообщений в реальном времени
@client.on(events.NewMessage(chats=group_usernames))
async def handler(event):
    msg = event.message
    text = msg.text or "[Без текста]"
    date = msg.date
    group_name = event.chat.username if event.chat else "unknown"
    sender_id = msg.sender_id

    if hasattr(msg, 'grouped_id') and msg.grouped_id:
        album_msgs = await client.get_messages(event.chat_id, limit=20)
        album_photos = [m for m in album_msgs if m.grouped_id == msg.grouped_id and m.photo]
        media_path = await save_all_photos(album_photos)
        save_message(group_name, sender_id, text, date, media_path)
    elif msg.photo:
        media_path = await save_all_photos([msg])
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
