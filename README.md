# Telegram Text Helper Bot

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](#)  
[![License](https://img.shields.io/badge/license-MIT-green.svg)](#)

**Telegram-бот для генерации текстов по мебели на заказ**

Бот использует OpenAI GPT для создания информативных и привлекательных постов и статей о кухнях, шкафах и другой мебели на заказ. Поддерживает хранение контекста, команды управления и простой деплой на VPS.

---

## 📋 Содержание

- [🚀 Возможности](#-возможности)
- [⚙️ Требования](#️-требования)
- [⚡ Установка и настройка](#-установка-и-настройка)
- [🔧 Конфигурация](#-конфигурация)
- [▶️ Использование](#️-использование)
- [☁️ Деплой на VPS](#️-деплой-на-vps)
  - [Systemd](#systemd)
  - [tmux](#tmux)
- [🛠️ Настройка и доработка](#️-настройка-и-доработка)
- [📝 Лицензия](#-лицензия)

---

## 🚀 Возможности

- Генерация текста по заданной теме (кухни, шкафы и т.д.)  
- Хранение истории диалога (контекст между сообщениями)  
- Команды управления:  
  - `/start` — приветствие и инструкции  
  - `/clear` — сброс истории диалога  
- Настраиваемый системный промпт  
- Лёгкий деплой через systemd или `tmux`

## ⚙️ Требования

- Python **3.10** или выше  
- Библиотеки Python:
  - `pyTelegramBotAPI`
  - `openai`
  - `python-dotenv`
- Доступ в интернет  
- Telegram Bot Token  
- OpenAI API Key

## ⚡ Установка и настройка

1. **Клонирование репозитория**
    ```bash
    git clone https://github.com/SergeyTatarintcev/telegram_text_helper_bot.git
    cd telegram_text_helper_bot
    ```
2. **Создание виртуального окружения**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate   # Linux/macOS
    .\.venv\Scripts\activate    # Windows PowerShell
    ```
3. **Установка зависимостей**
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

## 🔧 Конфигурация

Создайте файл `.env` в корне проекта (рядом с `bot.py`) без комментариев:

```dotenv
TELEGRAM_TOKEN=ваш_токен_телеграм
OPENAI_API_KEY=ваш_ключ_openai
AGENT_SYSTEM_PROMPT=Ваш системный промпт, например:
"Ты — экспертный копирайтер по мебели на заказ. Пиши качественные тексты про кухни, шкафы и другую мебель."


 **Обязательно проверьте:** `.env` должен содержать только пары `KEY=value`

## ▶️ Использование

1. Запустите бота локально:
    ```bash
    python bot.py
    ```
2. В Telegram отправьте своему боту:
    - `/start` — начать диалог  
    - Тему текста — например, «кухня в стиле хай-тек»  
3. Получите сгенерированный текст.  
4. Используйте `/clear` для сброса контекста.

## ☁️ Деплой на VPS

### Systemd

1. Скопируйте репозиторий на сервер или клонируйте:
    ```bash
    git clone https://github.com/SergeyTatarintcev/telegram_text_helper_bot.git
    cd telegram_text_helper_bot
    ```
2. Создайте виртуальное окружение и установите зависимости, как в разделе выше.  
3. Создайте файл сервиса `/etc/systemd/system/telegram_bot.service`:
    ```ini
    [Unit]
    Description=Telegram Text Helper Bot
    After=network.target

    [Service]
    Type=simple
    User=ваш_пользователь
    WorkingDirectory=/home/ваш_пользователь/telegram_text_helper_bot
    ExecStart=/home/ваш_пользователь/telegram_text_helper_bot/.venv/bin/python bot.py
    Restart=on-failure
    RestartSec=5
    EnvironmentFile=/home/ваш_пользователь/telegram_text_helper_bot/.env

    [Install]
    WantedBy=multi-user.target
    ```
4. Перезагрузите `systemd` и запустите сервис:
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable telegram_bot.service
    sudo systemctl start telegram_bot.service
    sudo systemctl status telegram_bot.service
    ```

### tmux

1. Установите `tmux` (если ещё не установлен):
    ```bash
    sudo apt install tmux -y
    ```
2. Запустите новую сессию и бот:
    ```bash
    tmux new -s telegram_bot
    source .venv/bin/activate
    python bot.py
    ```
3. Отключитесь от сессии, не останавливая бот: `Ctrl+B`, затем `D`.  
4. Вернуться к сессии: `tmux attach -t telegram_bot`.

## 🛠️ Настройка и доработка

- **Системный промпт** (`AGENT_SYSTEM_PROMPT`) можно изменять в `.env`.  
- **Параметры OpenAI** (`temperature`, `max_tokens`) настраиваются в `bot.py`.  
- Для долговременного хранения контекста рассмотрите подключение SQLite или JSON-файла.

## 📝 Лицензия

Проект распространяется под лицензией **MIT**.

---

Автор: SergeyTatarintcev