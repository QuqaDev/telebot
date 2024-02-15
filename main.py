import telebot
from telebot import types

bot = telebot.TeleBot('6871427421:AAF2WAK3Kh7O4gVcue_tmjAMkGlJUuWgF68')

# Начальное сообщение
start_message = """Привет, 🐰! Мне не терпится начать работу с Вами, но для начала хотел бы рассказать немного о нашей компании.
Мы ООО «Эколь» - предприятие с передовыми технологиями производства бытовой химии и современными методами организации и управления.
Мы производим стиральный порошок, белизну, а также кальцинированную соду.
Что Вас интересует?"""

# Словарь для хранения предыдущего сообщения пользователя
previous_message_dict = {}

# Создание Inline клавиатуры для главного меню
def create_main_menu():
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton('Продукция', callback_data='products'),
               types.InlineKeyboardButton('Где найти?', callback_data='find'))
    markup.row(types.InlineKeyboardButton('Дистрибьюторам', callback_data='distributors'),
               types.InlineKeyboardButton('Контакты', callback_data='contacts'))
    markup.row(types.InlineKeyboardButton('Задать вопрос', callback_data='question'))
    return markup

# Создание Inline клавиатуры для выбора продукции
def create_product_menu():
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton('Зифа', callback_data='zifa'),
               types.InlineKeyboardButton('Луч', callback_data='luch'))
    markup.row(types.InlineKeyboardButton('Назад', callback_data='back'))
    return markup

# Создание Inline клавиатуры для выбора локации
def create_location_menu():
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton('Уфа', callback_data='ufa'),
               types.InlineKeyboardButton('Салават', callback_data='salavat'),
               types.InlineKeyboardButton('Ишимбай', callback_data='ishimbay'))
    markup.row(types.InlineKeyboardButton('Назад', callback_data='back'))
    return markup

# Создание Inline клавиатуры для главного меню
def create_back_menu():
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton('Назад', callback_data='back'))
    return markup

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_start(message):
    markup = create_main_menu()
    msg = bot.send_message(message.chat.id, start_message, reply_markup=markup)
    previous_message_dict[message.chat.id] = msg.message_id
    bot.register_next_step_handler(msg, process_main_menu)

# Обработчик нажатий на Inline кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    if call.data == 'products':
        send_product_menu(call.message)
    elif call.data == 'find':
        send_location_menu(call.message)
    elif call.data == 'distributors':
        bot.send_message(chat_id, "Дистрибьюторам")
    elif call.data == 'contacts':
        bot.send_message(chat_id, "Контакты")
    elif call.data == 'question':
        bot.send_message(chat_id, "Задать вопрос")
    elif call.data == 'zifa' or call.data == 'luch':
        send_product_info(call)
    elif call.data == 'ufa' or call.data == 'salavat' or call.data == 'ishimbay':
        send_adress(call)
    elif call.data == 'back':
        send_previous_menu(chat_id)

# Обработчик нажатий на кнопки выбора продукции
def process_main_menu(message):
    if message.text == 'Продукция':
        send_product_menu(message)
    elif message.text == 'Где найти?':
        send_location_menu(message)

def send_adress(call):
    if call.data == 'ufa':
        markup = create_back_menu()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="dddddddddddddddddddddddddddddddddd...", reply_markup=markup)
    elif call.data == 'salavat':
        markup = create_back_menu()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="sdadadadasd", reply_markup=markup)
    elif call.data == 'ishimbay':
        markup = create_back_menu()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="22222222222222222222222", reply_markup=markup)

# Отправка Inline меню выбора продукции
def send_product_menu(message):
    markup = create_product_menu()
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                          text="Выберите продукцию:", reply_markup=markup)

# Отправка информации о продукте в том же сообщении
# Отправка информации о продукте в новом сообщении
def send_product_info(call):
    chat_id = call.message.chat.id
    if call.data == 'zifa':
        photo_path = 'C:\\Users\\halik\\PycharmProjects\\pythonProject1\\zifa-auto.jpg'
        sent_message = bot.send_photo(chat_id, open(photo_path, 'rb'), caption="Порошок Зифа\n\nСостав: ...", reply_markup=create_back_menu())
    elif call.data == 'luch':
        photo_path = 'C:\\Users\\halik\\PycharmProjects\\pythonProject1\\luch.jpg'
        sent_message = bot.send_photo(chat_id, open(photo_path, 'rb'), caption="Порошок Луч\n\nСостав: ...", reply_markup=create_back_menu())
    # Удаляем предыдущее сообщение с фотографией
    if chat_id in previous_message_dict:
        previous_message_id = previous_message_dict[chat_id]
        try:
            bot.delete_message(chat_id, previous_message_id)
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Error deleting previous message: {e}")
    # Обновляем словарь с ID предыдущего сообщения
    previous_message_dict[chat_id] = sent_message.message_id

# Отправка Inline меню выбора локации
def send_location_menu(message):
    markup = create_location_menu()
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                          text="Выберите локацию:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'back')
def back_button_handler(call):
    chat_id = call.message.chat.id
    send_previous_menu(chat_id)

def send_previous_menu(chat_id):
    if chat_id in previous_message_dict:
        previous_message_id = previous_message_dict.get(chat_id)
        if previous_message_id:
            try:
                # Отправляем новое сообщение с главным меню
                sent_message = bot.send_message(chat_id, start_message, reply_markup=create_main_menu())
                # Удаляем предыдущее сообщение
                bot.delete_message(chat_id, previous_message_id)
                # Обновляем словарь с ID предыдущего сообщения
                previous_message_dict[chat_id] = sent_message.message_id
            except telebot.apihelper.ApiTelegramException as e:
                print(f"Error sending or deleting previous message: {e}")
        else:
            print("Previous message id not found for chat:", chat_id)
    else:
        print("Chat id not found in previous_message_dict:", chat_id)

bot.polling(none_stop=True)

