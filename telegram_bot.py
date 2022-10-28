import os
import parsers
# import requests

from telegram.ext import CommandHandler, Updater, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup

from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENDPOINT = 'https://api.telegram.org/bot{token}/sendDocument'
RETRY_TIME = 150
ZERO = 0


load_dotenv()
secret_token = os.getenv('TOKEN')
updater = Updater(token=secret_token)


def get_request(update, context):
    """Функция получает ссылку из сообщения юзера."""
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([
        ['/new_link'],
        ['/my_contacts'],
        ],
        resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Отправь ссылку на '
             'песню с адреса Amalgama-lab.com'.format(name),
        reply_markup=button
    )


def do(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    url = update.message.text
    parsers.parse(url)
    parsers.parse_name(url)
    doc = open(f"{parsers.parse_name(url)}.txt", encoding='utf-8')
    button = ReplyKeyboardMarkup([
        ['/new_link'],
        ['/my_contacts'],
        ],
        resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='{}, Скоро придет сообщение с файлом'.format(name),
        reply_markup=button
    )
    context.bot.send_document(
        chat_id=chat.id,
        document=doc,
        reply_markup=button
    )


def new_link(update, context):
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([
        ['/new_link'],
        ['/my_contacts'],
        ],
        resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='Отправь новую ссылку на песню с адреса Amalgama-lab.com',
        reply_markup=button
    )


def my_contacts(update, context):
    chat = update.effective_chat

    context.bot.send_message(
        chat_id=chat.id,
        text='Мой телеграм: @maidaritsydenov\nМоя почта: tmaidari@mail.ru',
    )


def main():
    updater = Updater(token=secret_token)
    updater.dispatcher.add_handler(CommandHandler('start', get_request))
    updater.dispatcher.add_handler(CommandHandler('my_contacts', my_contacts))
    updater.dispatcher.add_handler(CommandHandler('new_link', new_link))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, do))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
