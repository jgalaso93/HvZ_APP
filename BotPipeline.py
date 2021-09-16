#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, ada few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os
import sys
import pandas as pd

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
database_file = os.path.join(sys.path[0], 'database.csv')
data = pd.read_csv(database_file, sep=';', header=0, dtype={'BOT_ID': str})


# TOOLS
def write_in_db(bot_id, field, value):
    if bot_id in data['BOT_ID'].tolist():
        pass
    else:
        new_register(bot_id, data)


def new_register(bot_id, df):
    new_row = dict()
    field = 'BOT_ID'
    for column in df.columns:
        if column == field:
            new_row[column] = str(bot_id)
        else:
            new_row[column] = 'unactive'

    new_row['ID'] = max(data['ID']) + 1
    df = df.append(new_row, ignore_index=True)
    df.to_csv(database_file, index=False)

# LOGIC AND FUNCTIONALITY


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Bienvenides a HvZ!')


def register(update, context):
    bot_id = update.message.chat['id']
    if str(bot_id) in data['BOT_ID'].tolist():
        update.message.reply_text('Tu registra ya está completado')
    else:
        new_register(bot_id, data)
        update.message.reply_text('Te has registrado!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Esto es la ayuda!')


def halal(update, context):
    """Send a halal message when the command /halal is issued"""
    update.message.reply_text('القرآن')


def corruptus(update, context):
    """Send corruptus description when the command /corruptus is issued"""
    update.message.reply_text('Des de temps immemorials del passat, la diversitat d’idees ha portat a la Humanitat a viure grans guerres i conflictes que només han acabat amb la masacre de vides i amb la pèrdua dels nostres iguals. És hora de deixar enrere el individualisme egoista i el benestar personal i unir-nos sota un nou líder que alliberi finalment als éssers humans de la seva càrrega. No més desigualtat, no més destrucció. Volem un món pacífic per tots i això només ho aconseguirem plegats. La heterogeneïtat present en la societat és l’origen de tots els problemes actuals! És hora de canviar, uneix-te per preservar i salvar el planeta!')


def echo(update, context):
    """Echo the user message."""
    # update.message.reply_text(update.message.chat['id'])
    update.message.reply_text("Escribe /help para entrar a la ayuda")


def get_my_id(update, context):
    update.message.reply_text(update.message.chat['id'])


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1975748853:AAG2-lzGxFToo0d2-hVwQQ7f_t499SEU_fk", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("halal", halal))
    dp.add_handler(CommandHandler("corruptus", corruptus))

    # Util class to check the id of the conversation
    dp.add_handler(CommandHandler("GetMyId", get_my_id))

    # Test class to register
    dp.add_handler(CommandHandler("register", register))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

    #hola hehehehhe