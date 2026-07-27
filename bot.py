import os
import random
from pathlib import Path

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from config import TOKEN, PHOTOS_FOLDER, VOICE_FILE, JOKES

# === ИНИЦИАЛИЗАЦИЯ ===
bot = telebot.TeleBot(TOKEN)

# === ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ===

def get_all_photos():
    """Возвращает список путей ко всем фото в папке"""
    folder = Path(PHOTOS_FOLDER)
    if not folder.exists():
        folder.mkdir()
    return [f for f in folder.iterdir() if f.suffix.lower() in ('.jpg', '.jpeg', '.png', '.gif')]

def main_keyboard():
    """Клавиатура с двумя основными кнопками"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton("📸 Фото"), KeyboardButton("🎲 Сюрприз"))
    return kb

# === ОБРАБОТЧИКИ ===

@bot.message_handler(commands=['start'])
def start(message):
    # 1. Текстовое признание
    love_text = (
        "❤️ Прр, моя любимая Камилла! ❤️\n\n"
        "Я люблю тебя сипса, я оч скучаю по тебе\n"
        "Я надеюсь, что эти два года станут для нас только началом!!"
    )
    bot.send_message(message.chat.id, love_text, reply_markup=main_keyboard())

    # 2. Голосовое сообщение (если файл существует)
    voice_path = Path(VOICE_FILE)
    if voice_path.exists():
        with open(voice_path, 'rb') as f:
            bot.send_voice(message.chat.id, f)
    else:
        bot.send_message(message.chat.id, "😅 Бияс, забудь загрузить voice.mp3! Положи его в папку с ботом.")

@bot.message_handler(commands=['photo'])
def cmd_photo(message):
    send_random_photo(message)

@bot.message_handler(commands=['surprise'])
def cmd_surprise(message):
    send_surprise(message)

@bot.message_handler(func=lambda msg: msg.text == "📸 Фото")
def button_photo(message):
    send_random_photo(message)

@bot.message_handler(func=lambda msg: msg.text == "🎲 Сюрприз")
def button_surprise(message):
    send_surprise(message)

# === ЛОГИКА ОТПРАВКИ ===

def send_random_photo(message):
    photos = get_all_photos()
    if not photos:
        bot.send_message(message.chat.id, "😅 Фоток пока нет! Бияс, добавь их в папку photos/")
        return

    chosen = random.choice(photos)
    with open(chosen, 'rb') as photo:
        bot.send_photo(
            message.chat.id,
            photo,
            caption="📸 Вот наше фото! ❤️"
        )

def send_surprise(message):
    # 50/50 – фото или шутка
    if random.choice([True, False]):
        send_random_photo(message)
    else:
        joke = random.choice(JOKES)
        bot.send_message(message.chat.id, joke)

# === ЗАПУСК ===

if __name__ == "__main__":
    print("🤖 Бот запущен! Нажми Ctrl+C для остановки")
    print(f"📸 Фото в папке: {len(get_all_photos())}")
    print(f"😂 Сгенерировано шуток: {len(JOKES)}")
    bot.infinity_polling()