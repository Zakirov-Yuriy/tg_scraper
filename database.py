# логика базы данных

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import UniqueConstraint

import datetime

# Создаём подключение к SQLite базе (файл messages.db)
engine = create_engine("sqlite:///messages.db", echo=False)

# Базовый класс для моделей
Base = declarative_base()

# Класс, описывающий таблицу сообщений
class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    group_name = Column(String)
    sender_id = Column(String)
    text = Column(String)
    date = Column(DateTime)
    media_path = Column(String)

    __table_args__ = (
        UniqueConstraint('group_name', 'sender_id', 'text', 'date', name='uix_1'),
    )


# Создание таблицы (если её ещё нет)
Base.metadata.create_all(engine)

# Создаём сессию — это то, через что мы работаем с БД
Session = sessionmaker(bind=engine)
session = Session()

# Функция для сохранения нового сообщения
def save_message(group_name, sender_id, text, date, media_path=None):
    # Проверка на дубликаты
    existing = session.query(Message).filter_by(
        group_name=group_name,
        sender_id=sender_id,
        text=text,
        date=date
    ).first()

    if existing:
        print("⛔️ Сообщение уже существует, пропускаем.")
        return

    # Если не существует — добавляем
    message = Message(
        group_name=group_name,
        sender_id=sender_id,
        text=text,
        date=date,
        media_path=media_path
    )
    session.add(message)
    session.commit()
    print("✅ Сообщение добавлено.")

