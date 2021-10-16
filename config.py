# [типы слайдов от 0 до 7]: [количество текстовых контейнеров]
SLIDE_TYPES = {
    0: 2,
    1: 2,
    2: 2,
    3: 3,
    4: 5,
    5: 1,
    6: 4,
    7: 3
}

# контент который воспринимается ботом
CONTENT = ["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact"]

# токен бота
TOKEN = "1409542686:AAHrny9RYqsRqZ7WCaROOXk9bshxJsBNS2Q"

# лог-файл
LOG_FILE = "logs.log"

# клавиатура
import telebot
MARKUP = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add(telebot.types.KeyboardButton("Да, нужен")).add(telebot.types.KeyboardButton("Нет, не нужен"))