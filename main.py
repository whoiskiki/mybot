import telebot
import random
from telebot import types
import logging
import os
from config import *
from flask import Flask, request

import pyodbc

botToken = telebot.TeleBot(BOT_TOKEN)
server = Flask(__name__)  # name of the current module
logger = telebot.logger
logger.setLevel(10)  # set the level on the debug/ allows us to see debugging messages on the heroku


if __name__ == "main":  # guarantee that server will be working only with main-script (webhooks)
    botToken.remove_webhook()
    botToken.set_webhook(url=APP_URL)
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))  # makes the server public


#conn = pyodbc.connect('Driver={SQL Server};'
                      #'Server=SEVERNAYAPOL;'
                      #'Database=GenshinTest;'
                      #'Trusted_Connection=yes;')

#cursor = conn.cursor()


@server.route(f"/{BOT_TOKEN}", methods=["POST"])  # redirect messages from Flask to the server
def redirect_message():
    json_string = request.get_data().decode("utf-8")  # data from server in json format
    update = telebot.types.Update.de_json(json_string)
    botToken.process_new_updates([update])  # deliver messages to the bot
    return "!", 200


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
                #cursor.execute("select namech from TblCharacter where id=1")
                #res = cursor.fetchone()

                #cursor.execute("select constellation from TblCharacter where id=1")
                #sec = cursor.fetchone()
                #cursor.commit()
                
                botToken.send_message(call.message.chat.id, f"Имя: Эфир \n Созвездие: Камень", reply_markup=None)

                #botToken.send_message(call.message.chat.id, f"Имя: {res[0]} \n Созвездие: {sec[0]}", reply_markup=None)
            elif call.data == 'female':
                #cursor.execute("select namech from TblCharacter where id=2")
                #res = cursor.fetchone()

                #cursor.execute("select constellation from TblCharacter where id=2")
                #sec = cursor.fetchone()
                #cursor.commit()
                
                botToken.send_message(call.message.chat.id, f"Имя: Пошла \n Созвездие: Нахуй", reply_markup=None)

                #botToken.send_message(call.message.chat.id, f"Имя: {res[0]} \n Созвездие: {sec[0]}", reply_markup=None)

        botToken.edit_message_reply_markup(call.message.chat.id, message_id=call.message.id, reply_markup=None)
    except Exception as error:
        print(repr(error))


#botToken.polling(none_stop=True)
#conn.close()
