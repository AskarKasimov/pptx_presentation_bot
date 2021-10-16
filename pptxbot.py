import logging
import pptx
import telebot
import os
from config import SLIDE_TYPES, CONTENT, TOKEN, LOG_FILE, MARKUP

DESIGNS_NUMBER = len(os.listdir("designs")) - 1
TYPES_NUMBER = len(os.listdir("types"))
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)
# inline клавиатура
INLINE_MARKUP = telebot.types.InlineKeyboardMarkup()
INLINE_MARKUP.row(telebot.types.InlineKeyboardButton(text='Назад', callback_data="back " + str(DESIGNS_NUMBER - 1)),
                  telebot.types.InlineKeyboardButton(text='Вперед', callback_data="next 1"))
INLINE_MARKUP.add(telebot.types.InlineKeyboardButton(text='Этот', callback_data="0"))


def contenthelp(message, typ):
    er = "Введите "
    if message.content_type == "photo":
        er = "Зачем мне картинка? Мне нужно получить "
    elif message.content_type == "document":
        er = "Давайте лучше без документов. Пришлите мне "
    elif message.content_type == "voice":
        er = "Очень красивый голос, но мне нужно прислать "
    elif message.content_type == "audio":
        er = "Потом послушаю... Сейчас мне бы лучше "
    elif message.content_type == "sticker":
        er = "Классный стикер, я себе тоже добавил... Но для презентации мне нужно отправить "
    elif message.content_type == "video" or message.content_type == "video_note":
        er = "Потом обязательно посмотрю, а сейчас вам нужно отправить мне "
    elif message.content_type == "location":
        er = "Были там? Красиво, наверное... Но я всё еще жду "
    elif message.content_type == "contact":
        er = "Ваш номерок? Обязательно созвонимся, но а сейчас мне требуется "
    return er + typ


def makepresentation(design, types, naming, title=None, subtitle=None):
    prs = pptx.Presentation(f"designs/{design}.pptx")
    if title:
        slide = prs.slides.add_slide(prs.slide_layouts[0])
        slide.placeholders[0].text = str(title)
        slide.placeholders[1].text = str(subtitle) if subtitle else ""
    for txt in types:
        slide = prs.slides.add_slide(prs.slide_layouts[txt["type"]])
        for i in range(SLIDE_TYPES[txt["type"]]):
            slide.placeholders[i].text = str(txt[f"text{i}"])
    prs.save(naming)


class Bot:
    def __init__(self, bott):
        self.bot = bott
        self.count_slides = 0
        self.count_text = 0
        self.design = 0
        self.helper = ""
        self.types = list()
        self.help_type = 0

    def sendhi(self, message):
        print(str(message.from_user.username), str(message.text))
        self.bot.send_message(message.chat.id,
                              "Привет, я бот, помогающий сделать презентацию в привычном формате "
                              ".pptx прямо в Telegram!")
        bot.send_message(message.chat.id,
                         "Каким будет дизайн вашей презентации?")
        bot.send_photo(message.chat.id, open("designs/demo/0.png", "rb"), f"Дизайн №1", reply_markup=INLINE_MARKUP)

    def getdesign(self, message):
        try:
            if int(message.text) in range(DESIGNS_NUMBER):
                self.design = message.text
                self.bot.send_message(message.chat.id, "Сколько слайдов должно быть в вашей презентации?\n--\n"
                                                       "P.S. Указывайте количество слайдов, не учитывая титульный. "
                                                       "Заполнить титульный слайд можно "
                                                       "будет в конце создания презентации.")

                self.bot.register_next_step_handler(message, self.getcount_slides)
            else:
                raise ValueError("Нет такого номера дизайна.\nВыберете номер, написанный под фото")
        except ValueError as e:
            er = e if str(e)[0] != "i" else "Введите номер дизайна (написано под фото)!"
            print("Bot", er)
            self.bot.reply_to(message, er)
            self.bot.register_next_step_handler(message, self.getdesign)
        except TypeError:
            self.bot.reply_to(message, contenthelp(message, "число"))
            print("Bot", contenthelp(message, "число"))
            self.bot.register_next_step_handler(message, self.getdesign)

    def getcount_slides(self, message):
        print(str(message.from_user.username), str(message.text))
        try:
            if int(message.text) > 0:
                self.count_slides = int(message.text)
                for i in range(TYPES_NUMBER):
                    if i != 6:
                        bot.send_photo(message.chat.id, open(f"types/{str(i)}.png", "rb"), f"Тип слайда №{str(i)}")
                self.bot.send_message(message.chat.id,
                                      "Сейчас нужно будет выбирать типы слайдов и "
                                      "вводить заголовки и тексты, добавлять картинки...\n"
                                      "Итак, тип первого слайда?")
                self.bot.register_next_step_handler(message, self.gettypes)
            elif int(message.text) == 0:
                raise ValueError("Число слайдов не может быть равным нулю!")
            else:
                raise ValueError("Число слайдов не может быть отрицательным!")
        except ValueError as e:
            er = e if str(e)[0] != "i" else "Введите целое число!"
            print("Bot", er)
            self.bot.reply_to(message, er)
            self.bot.register_next_step_handler(message, self.getcount_slides)
        except TypeError:
            self.bot.reply_to(message, contenthelp(message, "число"))
            print("Bot", contenthelp(message, "число"))
            self.bot.register_next_step_handler(message, self.getcount_slides)

    def gettypes(self, message):
        try:
            if int(message.text) in range(TYPES_NUMBER):

                self.help_type = int(message.text)
                self.count_text = SLIDE_TYPES[self.help_type]
                self.types.append({"type": self.help_type})
                self.bot.send_message(message.chat.id, "Введите текст №1 слайда №1")

                self.bot.register_next_step_handler(message, self.getslides)
            else:
                raise ValueError("Нет такого номера дизайна.\nВыберете номер, написанный под фото")
        except ValueError as e:
            er = e if str(e)[0] != "i" else "Введите номер типа слайда (написано под фото)!"
            print("Bot", er)
            self.bot.reply_to(message, er)
            self.bot.register_next_step_handler(message, self.gettypes)
        except TypeError:
            self.bot.reply_to(message, contenthelp(message, "число"))
            print("Bot", contenthelp(message, "число"))
            self.bot.register_next_step_handler(message, self.gettypes)

    def getslides(self, message):
        print(str(message.from_user.username), str(message.text))
        if message.content_type != "text":
            self.bot.reply_to(message, contenthelp(message, "текст"))
            print("Bot", contenthelp(message, "текст"))
            self.bot.register_next_step_handler(message, self.getslides)
        elif message.content_type == "text":
            indexhelp = SLIDE_TYPES[self.help_type] - self.count_text
            self.types[-1][f"text{indexhelp}"] = message.text
            self.count_text -= 1
            if self.count_text == 0:
                self.count_slides -= 1
                if self.count_slides == 0:
                    self.bot.send_message(message.chat.id, "Вам нужен титульный слайд?", reply_markup=MARKUP)
                    self.bot.register_next_step_handler(message, self.title)
                    return
                self.bot.send_message(message.chat.id, "Следующий слайд... Тип?")
                self.bot.register_next_step_handler(message, self.gettypes)
                return
            self.bot.send_message(message.chat.id,
                                  f"А теперь текст №{SLIDE_TYPES[self.help_type] - self.count_text + 1} слайда №{len(self.types)}")
            print("Bot", "А теперь текст слайда")
            self.bot.register_next_step_handler(message, self.getslides)

    def title(self, message):
        if message.text == "Нет, не нужен":
            self.bot.send_message(message.chat.id, "Приготовьтесь, сейчас вылетит презентация...",
                                  reply_markup=telebot.types.ReplyKeyboardRemove())
            logging.info(message.from_user.username + str(self.types))
            makepresentation(self.design, self.types, message.from_user.username + '_presentation.pptx', self.helper,
                             message.text)
            self.bot.send_document(message.chat.id, open(message.from_user.username + '_presentation.pptx', 'rb'))
            os.remove(message.from_user.username + '_presentation.pptx')
        elif message.text == "Да, нужен":
            self.bot.send_message(message.chat.id, "Введите текст заголовка титульного слайда",
                                  reply_markup=telebot.types.ReplyKeyboardRemove())
            self.bot.register_next_step_handler(message, self.gettitle)
        else:
            self.bot.reply_to(message, "Выберете вариант ответа на экранчике под вашей клавиатурой")
            self.bot.register_next_step_handler(message, self.title)

    def gettitle(self, message):
        self.helper = message.text
        self.bot.send_message(message.chat.id, "Вам нужен подзаголовок?", reply_markup=MARKUP)
        self.bot.register_next_step_handler(message, self.getsubs)

    def getsubs(self, message):
        if message.text == "Нет, не нужен":
            self.bot.send_message(message.chat.id, "Приготовьтесь, сейчас вылетит презентация...",
                                  reply_markup=telebot.types.ReplyKeyboardRemove())
            logging.info(message.from_user.username + str(self.types))
            makepresentation(self.design, self.types, message.from_user.username + '_presentation.pptx', self.helper)
            self.bot.send_document(message.chat.id, open(message.from_user.username + '_presentation.pptx', 'rb'))
            os.remove(message.from_user.username + '_presentation.pptx')
        elif message.text == "Да, нужен":
            self.bot.send_message(message.chat.id, "Введите текст подзаголовка титульного слайда",
                                  reply_markup=telebot.types.ReplyKeyboardRemove())
            self.bot.register_next_step_handler(message, self.sending)
        else:
            self.bot.reply_to(message, "Выберете вариант ответа на экранчике под вашей клавиатурой")
            self.bot.register_next_step_handler(message, self.getsubs)

    def sending(self, message):
        self.bot.send_message(message.chat.id, "Приготовьтесь, сейчас вылетит презентация...",
                              reply_markup=telebot.types.ReplyKeyboardRemove())
        logging.info(message.from_user.username + str(self.types))
        makepresentation(self.design, self.types, message.from_user.username + '_presentation.pptx', self.helper,
                         message.text)
        self.bot.send_document(message.chat.id, open(message.from_user.username + '_presentation.pptx', 'rb'))
        os.remove(message.from_user.username + '_presentation.pptx')


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def sendhi(message):
    Bot(bot).sendhi(message)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(call.id)
    if call.data.split()[0] == "next" or call.data.split()[0] == "back":
        mark = telebot.types.InlineKeyboardMarkup()
        if call.data.split()[1] == str(DESIGNS_NUMBER - 1):
            but = telebot.types.InlineKeyboardButton(text='Вперед',
                                                     callback_data="next 0")
        else:
            but = telebot.types.InlineKeyboardButton(text='Вперед',
                                                     callback_data="next " + str(int(call.data.split()[1]) + 1))
        if call.data.split()[1] == "0":
            mark.row(telebot.types.InlineKeyboardButton(text='Назад', callback_data="back " + str(DESIGNS_NUMBER - 1)),
                     but)
        else:
            mark.row(telebot.types.InlineKeyboardButton(text='Назад',
                                                        callback_data="back " + str(int(call.data.split()[1]) - 1)),
                     but)
        mark.add(telebot.types.InlineKeyboardButton(text='Этот', callback_data=call.data.split()[1]))
        with open(f"designs/demo/{call.data.split()[1]}.png", "rb") as file:
            bot.edit_message_media(reply_markup=mark, chat_id=call.message.chat.id, message_id=call.message.message_id,
                                   media=telebot.types.InputMedia(type="photo", media=file))
            bot.edit_message_caption(f"Дизайн №{str(int(call.data.split()[1]) + 1)}", call.message.chat.id, call.message.message_id, reply_markup=mark)
    else:
        bot.edit_message_caption(f"Дизайн вашей презентации (№{str(int(call.data) + 1)}), выбранный вами", call.message.chat.id,
                                 call.message.message_id)
        call.message.text = int(call.data)
        Bot(bot).getdesign(call.message)


@bot.message_handler(content_types=CONTENT)
def index(message):
    bot.send_message(message.chat.id, "Нажмите /start чтобы начать")


bot.polling(none_stop=True)
