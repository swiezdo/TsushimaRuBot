from dotenv import load_dotenv
import os

# Загружаем переменные из .env файла
load_dotenv()

# Токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Проверка на наличие токена (очень рекомендую)
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден в .env файле!")

# Путь к базе данных
DATABASE = "users.db"

# Ссылка на группу
GROUP_LINK = "https://t.me/+ZFiVYVrz-PEzYjBi"
