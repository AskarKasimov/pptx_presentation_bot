import pptx
import telebot
import os

CONTENT = ["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact"]
def hi():
    pass

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
    prs = pptx.Presentation(f"designes/{design}.pptx")
    if title:
        slide = prs.slides.add_slide(prs.slide_layouts[0])
        slide.shapes.title.text = str(title)
        slide.placeholders[1].text = str(subtitle) if subtitle else ""
    for txt in types:
        slide = prs.slides.add_slide(prs.slide_layouts[int(txt["type"])])
        slide.shapes.title.text = str(txt["text1"])
        slide.placeholders[1].text = str(txt["text2"])
    prs.save(naming + '_presentation.pptx')


class Bot:
    def __init__(self, bott):
        self.bot = bott
        self.count = 0
        self.design = ""
        self.helper = ""
        self.types = list()
        self.help_type = 0

    def sendhi(self, message):
        print(str(message.from_user.first_name), str(message.text))
        self.bot.send_message(message.chat.id,
                              "Привет, я бот, помогающий сделать презентацию в привычном формате "
                              ".pptx прямо в Telegram!")

        for i in range(11):
            bot.send_photo(message.chat.id, open(f"designes/demo/{str(i)}.png", "rb"), f"Дизайн №{str(i)}")
        bot.send_message(message.chat.id,
                         "Каким будет дизайн вашей презентации?\n--\nP.S. Напишите мне номер понравившегося варианта")
        self.bot.register_next_step_handler(message, self.getdesign)

    def getdesign(self, message):
        try:
            if int(message.text) >= 0:
                self.design = message.text
                self.bot.send_message(message.chat.id, "Сколько слайдов должно быть в вашей презентации?\n--\n"
                                                       "P.S. Указывайте количество слайдов, не учитывая титульный. "
                                                       "Заполнить титульный слайд можно "
                                                       "будет в конце создания презентации.")

                self.bot.register_next_step_handler(message, self.getcount)
            else:
                raise ValueError("Номер дизайна не может быть отрицательным!")
        except ValueError as e:
            er = e if str(e)[0] != "i" else "Введите номер дизайна (написано под фото)!"
            print("Bot", er)
            self.bot.reply_to(message, er)
            self.bot.register_next_step_handler(message, self.getdesign)
        except TypeError:
            self.bot.reply_to(message, contenthelp(message, "число"))
            print("Bot", contenthelp(message, "число"))
            self.bot.register_next_step_handler(message, self.getdesign)

    def getcount(self, message):
        print(str(message.from_user.first_name), str(message.text))
        try:
            if int(message.text) > 0:
                self.count = int(message.text)
                for i in range(8):
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
            self.bot.register_next_step_handler(message, self.getcount)
        except TypeError:
            self.bot.reply_to(message, contenthelp(message, "число"))
            print("Bot", contenthelp(message, "число"))
            self.bot.register_next_step_handler(message, self.getcount)

    def gettypes(self, message):
        try:
            if int(message.text) >= 0:
                self.help_type = int(message.text)
                self.bot.send_message(message.chat.id, "Введите текст слайда")

                self.bot.register_next_step_handler(message, self.getslides)
            else:
                raise ValueError("Номер типа слайда не может быть отрицательным!")
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
        print(str(message.from_user.first_name), str(message.text))
        if message.content_type != "text":
            self.bot.reply_to(message, contenthelp(message, "текст"))
            print("Bot", contenthelp(message, "текст"))
            self.bot.register_next_step_handler(message, self.getslides)
        elif message.content_type == "text":
            self.count -= 1
            self.helper = message.text
            self.bot.send_message(message.chat.id, "А теперь подтекст слайда")
            print("Bot", "А теперь текст слайда")
            self.bot.register_next_step_handler(message, self.gettxt)

    def gettxt(self, message):
        print(str(message.from_user.first_name), str(message.text))
        if message.content_type != "text":
            self.bot.reply_to(message, contenthelp(message, "текст"))
            print("Bot", contenthelp(message, "текст"))
            self.bot.register_next_step_handler(message, self.gettxt)
        elif message.content_type == "text":
            self.types.append({"type": self.help_type, "text1": self.helper, "text2": message.text})
            if self.count != 0:
                self.bot.send_message(message.chat.id, "Следующий слайд... Тип?")
                print("Bot", "Следующий слайд... Заголовок?")
                self.bot.register_next_step_handler(message, self.gettypes)
            else:
                markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                markup.row(telebot.types.KeyboardButton("Да, нужен"))
                markup.row(telebot.types.KeyboardButton("Нет, не нужен"))

                self.bot.send_message(message.chat.id, "Вам нужен титульный слайд?", reply_markup=markup)
                self.bot.register_next_step_handler(message, self.title)

    def title(self, message):
        if message.text == "Нет, не нужен":
            self.bot.send_message(message.chat.id, "Приготовьтесь, сейчас вылетит презентация...", reply_markup=telebot.types.ReplyKeyboardRemove())
            print(self.types)
            makepresentation(self.design, message.from_user.first_name + '_presentation.pptx', self.helper, message.text)
            self.bot.send_document(message.chat.id, open(message.from_user.first_name + '_presentation.pptx', 'rb'))
            os.remove(message.from_user.first_name + '_presentation.pptx')
        elif message.text == "Да, нужен":
            self.bot.send_message(message.chat.id, "Введите текст заголовка титульного слайда", reply_markup=telebot.types.ReplyKeyboardRemove())
            self.bot.register_next_step_handler(message, self.gettitle)
        else:
            self.bot.reply_to(message, "Выберете вариант ответа на экранчике под вашей клавиатурой")
            self.bot.register_next_step_handler(message, self.title)

    def gettitle(self, message):
        self.helper = message.text
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.row(telebot.types.KeyboardButton("Да, нужен"))
        markup.row(telebot.types.KeyboardButton("Нет, не нужен"))
        self.bot.send_message(message.chat.id, "Вам нужен подзаголовок?", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.getsubs)

    def getsubs(self, message):
        if message.text == "Нет, не нужен":
            self.bot.send_message(message.chat.id, "Приготовьтесь, сейчас вылетит презентация...", reply_markup=telebot.types.ReplyKeyboardRemove())
            print(self.types)
            makepresentation(self.design, message.from_user.first_name + '_presentation.pptx', self.helper, message.text)
            self.bot.send_document(message.chat.id, open(message.from_user.first_name + '_presentation.pptx', 'rb'))
            os.remove(message.from_user.first_name + '_presentation.pptx')
        elif message.text == "Да, нужен":
            self.bot.send_message(message.chat.id, "Введите текст подзаголовка титульного слайда", reply_markup=telebot.types.ReplyKeyboardRemove())
            self.bot.register_next_step_handler(message, self.sending)
        else:
            self.bot.reply_to(message, "Выберете вариант ответа на экранчике под вашей клавиатурой")
            self.bot.register_next_step_handler(message, self.getsubs)

    def sending(self, message):
        self.bot.send_message(message.chat.id, "Приготовьтесь, сейчас вылетит презентация...",
                              reply_markup=telebot.types.ReplyKeyboardRemove())
        print(self.types)
        makepresentation(self.design, message.from_user.first_name + '_presentation.pptx', self.helper, message.text)
        self.bot.send_document(message.chat.id, open(message.from_user.first_name + '_presentation.pptx', 'rb'))
        os.remove(message.from_user.first_name + '_presentation.pptx')


bot = telebot.TeleBot("1409542686:AAHrny9RYqsRqZ7WCaROOXk9bshxJsBNS2Q")

@bot.message_handler(commands=['start'])
def sendhi(message):
    Bot(bot).sendhi(message)


@bot.message_handler(content_types=CONTENT)
def index(message):
    bot.send_message(message.chat.id, "Нажмите /start чтобы начать")


bot.polling(none_stop=True)
