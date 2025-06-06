
# 📦 TsushimaRuBot — Telegram Bot

Бот на Python для управления сообществом Tsushima.ru в Telegram.  
Работает на `aiogram`, с базой данных SQLite и переменными окружения через `.env`.

---

## 🔧 Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/swiezdo/TsushimaRuBot.git
cd TsushimaRuBot
```

---

### 2. Создание виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

---

### 4. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```bash
nano .env
```

Пример содержимого `.env`:

```env
BOT_TOKEN=ваш_токен_бота
```

---

### 5. Подготовка базы данных

Создайте файл базы данных `users.db`, если его нет:

```bash
sqlite3 users.db ".databases"
```

Или используйте существующую базу.

---

## 🚀 Запуск через systemd (службы)

Настроим автоматический запуск бота и панели управления базой через systemd.

---

### 6. Служба для бота

Создайте файл юнита:

```bash
sudo nano /etc/systemd/system/tsushimarubot.service
```

Пример содержимого:

```ini
[Unit]
Description=Telegram Bot TsushimaRuBot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/TsushimaRuBot
ExecStart=/home/ubuntu/TsushimaRuBot/venv/bin/python3 /home/ubuntu/TsushimaRuBot/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Активируйте службу:

```bash
sudo systemctl daemon-reload
sudo systemctl enable tsushimarubot.service
sudo systemctl start tsushimarubot.service
```

Проверка статуса:

```bash
sudo systemctl status tsushimarubot.service
```

---

### 7. Служба для SQLite Web

Создание службы:

```bash
sudo nano /etc/systemd/system/sqliteweb.service
```

Пример содержимого:

```ini
[Unit]
Description=SQLite Web Interface
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/TsushimaRuBot
ExecStart=/home/ubuntu/TsushimaRuBot/venv/bin/sqlite_web --host 0.0.0.0 --port 8080 users.db
Restart=always

[Install]
WantedBy=multi-user.target
```

Активируйте службу:

```bash
sudo systemctl daemon-reload
sudo systemctl enable sqliteweb.service
sudo systemctl start sqliteweb.service
```

Веб-интерфейс будет доступен по адресу:

```
http://<ваш-IP>:8080
```

---

## 🛠️ Полезные команды

- Перезапуск бота:

```bash
sudo systemctl restart tsushimarubot.service
```

- Логи бота:

```bash
journalctl -u tsushimarubot.service -f
```

- Остановка бота:

```bash
sudo systemctl stop tsushimarubot.service
```

---

## 📝 .gitignore (рекомендуемый)

Создайте файл `.gitignore` в корне проекта со следующим содержимым:

```gitignore
# Python кеш
__pycache__/
**/__pycache__/

# Виртуальное окружение
venv/

# Переменные окружения
.env

# База данных пользователей
users.db

# Системные файлы
*.pyc
*.pyo
*.pyd

# IDE и редакторы
.vscode/
.idea/
*.swp
```

---

## ⚠️ Важно

- Никогда не публикуйте `.env` и `users.db` в публичных репозиториях.
- Для безопасности рекомендуется использовать отдельного пользователя без привилегий для запуска служб.

---

# ✅ Готово!

Теперь бот будет автоматически запускаться при старте системы и работать в фоне.  
Веб-панель для управления базой также будет доступна при необходимости.

---

## 🚀 Требования к окружению

- Python 3.8+
- SQLite 3
- `git`, `systemd` установлены на сервере.

---

## 📦 Требуемые зависимости (`requirements.txt`)

```txt
aiogram==3.18.0
aiosqlite==0.19.0
sqlite-web==0.6.4
python-dotenv==1.1.0
```
