## 🛠️ Используемые технологии

| Frontend | Backend | Database | Infra / Tooling |
|---|---|---|---|
| ![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black) ![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white) ![Vite](https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=white) ![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?logo=tailwindcss&logoColor=white) | ![Node.js](https://img.shields.io/badge/Node.js-339933?logo=node.js&logoColor=white) ![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white) ![Fastify](https://img.shields.io/badge/Fastify-000000?logo=fastify&logoColor=white) ![Prisma](https://img.shields.io/badge/Prisma-2D3748?logo=prisma&logoColor=white) | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white) | ![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white) ![Vite](https://img.shields.io/badge/Vite_Config-646CFF?logo=vite&logoColor=white) ![TSConfig](https://img.shields.io/badge/tsconfig-3178C6?logo=typescript&logoColor=white) ![Tailwind Config](https://img.shields.io/badge/tailwind.config.js-06B6D4?logo=tailwindcss&logoColor=white) |


# Telegram Scraper + Admin Panel

A Telegram group message scraper that saves data to a database and displays it in a web interface.

## 🚀 Features

- Scrapes message history from specified Telegram groups  
- Automatically tracks new incoming messages  
- Saves text, date, author, and **photos**  
- Displays data in an admin panel built with Flask  
- Allows downloading images  

## 🛠️ Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/tg_scraper.git
cd tg_scraper
(Optional) Create and activate a virtual environment:

bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/macOS
Install dependencies:

bash
pip install -r requirements.txt
⚙️ Configuration
Create a config.py file:

python
api_id = YOUR_API_ID
api_hash = "YOUR_API_HASH"
group_usernames = ["@group_name"]
You can get your api_id and api_hash at https://my.telegram.org.

▶️ Running
First, run the scraper:

bash
python listener.py
It will first load the message history, then start live monitoring new messages.

To launch the web interface:

bash
python admin_panel.py
The admin panel will be available at: http://127.0.0.1:5000

🖼️ Admin Panel Preview
![Admin panel screenshot](images/screenshot.png)


📁 Project Structure

tg_scraper/
├── listener.py          # main scraper script
├── admin_panel.py       # Flask web interface
├── config.py            # API settings and group list
├── database.py          # database handling
├── messages.db          # SQLite database file
├── requirements.txt     # dependencies
├── templates/
│   └── messages.html    # web interface template
└── static/
    └── media/           # saved images



# Telegram Scraper + Admin Panel

Парсер сообщений из Telegram-групп с сохранением в базу данных и отображением в веб-интерфейсе.

## 🚀 Возможности

- Парсит историю сообщений из указанных Telegram-групп
- Автоматически отслеживает новые сообщения
- Сохраняет текст, дату, автора и **фото**
- Отображает данные в админ-панели на Flask
- Позволяет скачивать изображения

## 🛠️ Установка

1. Клонируй репозиторий:

```bash
git clone https://github.com/your-username/tg_scraper.git
cd tg_scraper
```

2. Создай и активируй виртуальное окружение (опционально):

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/macOS
```

3. Установи зависимости:

```bash
pip install -r requirements.txt
```

## ⚙️ Конфигурация

Создай файл `config.py`:

```python
api_id = YOUR_API_ID
api_hash = "YOUR_API_HASH"
group_usernames = ["@название_группы"]
```

Получить `api_id` и `api_hash` можно на сайте https://my.telegram.org.

## ▶️ Запуск

Сначала запусти парсер:

```bash
python listener.py
```

Сначала загрузится история сообщений, затем будет вестись live-мониторинг новых.

Чтобы запустить веб-интерфейс:

```bash
python admin_panel.py
```

Панель будет доступна по адресу: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 🖼️ Пример админ-панели

![Скриншот админ-панели](images/screenshot.png)

## 📁 Структура проекта

```
tg_scraper/
├── listener.py          # основной парсер
├── admin_panel.py       # Flask интерфейс
├── config.py            # настройки API и список групп
├── database.py          # работа с базой данных
├── messages.db          # SQLite база данных
├── requirements.txt     # зависимости
├── templates/
│   └── messages.html    # шаблон для веб-интерфейса
└── static/
    └── media/           # сохранённые изображения
```

