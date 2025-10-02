# WebApp Telegram Django

This is a minimal skeleton project for a Telegram WebApp integrated with Django. The project demonstrates how to:

- Create a simple WebApp interface.
- Use Telegram WebApp `ThemeParams` for native theming.

## Features

- Django Backend: Utilizes Django framework for building the web application backend.
- Python Telegram Bot: Integrates Python Telegram Bot library for interacting with the Telegram API.
- Uses PostgreSQL as the database backend for storing bot data.
- Uses Django Daisy for the admin interface, providing a modern and customizable UI
- Theme-aware colors using Telegram's CSS variables.
- Basic main page structure with a section for content.
- Ready for expansion with API requests and additional WebApp functionality.

## Installation & Setup

1. **Clone the repository:**

```bash
git clone https://github.com/sibeardev/webapp_telegram_django.git
cd webapp_telegram_django
```

2. **Set environment variables:**

Create a `.env` file in the project root with your Telegram bot token and Django secret key:

```env
# === Django settings ===
DJANGO__SECRET_KEY="super_secret_key"
DJANGO__ALLOWED_HOSTS=["127.0.0.1","localhost"]
DJANGO__CSRF_TRUSTED_ORIGINS=["https://localhost"]

# === Database settings ===
POSTGRES__USER=user
POSTGRES__PASSWORD=password
POSTGRES__DB=db

# === Telegram bot ===
TELEGRAM__TOKEN=You can obtain a bot token from @BotFather in Telegram.
TELEGRAM__ADMINS=[308382881]

# === External URL ===
EXTERNAL_URL=https://example.com
```

> Note: For testing purposes, you can use [ngrok](https://ngrok.com/docs/getting-started/) to expose your local server to the internet. After installing ngrok, run ngrok http 8000 in a separate terminal window. Then, insert the ngrok URL generated for your server as the value for the EXTERNAL_URL variable in your .env file.

3. Build and start the project with Docker:

```bash
docker-compose up --build
```

> Note: When the container starts, Django migrations are automatically applied, static files are collected, and a superuser is created with login `admin` and password `admin`.

Open the bot in Telegram and press the Start button.

---

**License:** This project is licensed under the MIT License.
