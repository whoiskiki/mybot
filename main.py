import telebot
from telebot import types
import random
import pyodbc

botToken = telebot.TeleBot('5412185592:AAEX39exboJVWOWpb-VfP2Wn8s65b8EcFVE')

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=SEVERNAYAPOL;'
                      'Database=GenshinTest;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()


@botToken.message_handler(content_types=['text'])
def welcome(message):
    if message.text == "/start":
        sendMess = f'К звёздам и к безднам, <b>{message.from_user.first_name}</b>' \
                   f'\nЧем я могу помочь?'

        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("send meme", callback_data='meme')
        item3 = types.InlineKeyboardButton("get meme id", callback_data='id')
        item2 = types.InlineKeyboardButton("character info", callback_data='character')
        markup.add(item1, item2, item3)

        botToken.send_message(message.chat.id, sendMess, parse_mode='html', reply_markup=markup)
    else:
        botToken.send_message(message.chat.id,
                              "\'Моя\' \'твоя\' не понимать! Пропиши  команду /start для начала работы.")


@botToken.callback_query_handler(func=lambda call: True)
def callbackButtons(call):
    try:
        if call.message:
            if call.data == 'meme':
                with open('stc.txt') as i:
                    lines = i.readlines()
                randomLine = random.choice(lines).strip()

                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("send meme", callback_data='meme')
                item2 = types.InlineKeyboardButton("character info", callback_data='character')
                item3 = types.InlineKeyboardButton("get meme id", callback_data='id')
                markup.add(item1, item2, item3)
                botToken.send_sticker(call.message.chat.id, randomLine, reply_markup=markup)

            elif call.data == 'character':
                mark = types.InlineKeyboardMarkup(row_width=2)
                i1 = types.InlineKeyboardButton("Aether", callback_data='male')
                i2 = types.InlineKeyboardButton("Lumine", callback_data='female')
                i3 = types.InlineKeyboardButton("Go back fucker", callback_data='back')
                mark.add(i1, i2, i3)
                botToken.send_message(call.message.chat.id, "Ну че делаем?...", reply_markup=mark)

            elif call.data == 'male':
                cursor.execute("select namech from TblCharacter where id=1")
                res = cursor.fetchone()

                cursor.execute("select constellation from TblCharacter where id=1")
                sec = cursor.fetchone()
                cursor.commit()

                botToken.send_message(call.message.chat.id, f"Имя: {res[0]} \n Созвездие: {sec[0]}", reply_markup=None)
            elif call.data == 'female':
                cursor.execute("select namech from TblCharacter where id=2")
                res = cursor.fetchone()

                cursor.execute("select constellation from TblCharacter where id=2")
                sec = cursor.fetchone()
                cursor.commit()

                botToken.send_message(call.message.chat.id, f"Имя: {res[0]} \n Созвездие: {sec[0]}", reply_markup=None)

        botToken.edit_message_reply_markup(call.message.chat.id, message_id=call.message.id, reply_markup=None)
    except Exception as error:
        print(repr(error))


botToken.polling(none_stop=True)
conn.close()
