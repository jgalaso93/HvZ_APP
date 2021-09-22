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
import cv2
import tempfile
import shutil

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
database_file = os.path.join(sys.path[0], 'database.csv')
try:
    data = pd.read_csv(database_file, sep=';', header=0, dtype={'BOT_ID': str})
except:
    data = pd.read_csv(database_file, sep=',', header=0, dtype={'BOT_ID': str})

registred_ids = data['BOT_ID'].tolist()

mission_database_file = os.path.join(sys.path[0], 'mission_database.csv')
mission_data = pd.read_csv(mission_database_file, sep=';', header=0,
                           dtype={'MISSION': str, 'RESULT_POOL': str},
                           encoding='cp1252')
mission_ids = mission_data['MISSION_ID'].tolist()


# TOOLS
def mission_accomplished(user_id, mission_id):
    """
    Function that erases the active mission and add the mission to the done pile
    """
    building = mission_data[mission_data['MISSION_ID'] == mission_id]['AM_BUILDING']
    am_filed = building.values[0]
    dm_field = 'D' + am_filed[1:]
    done_missions = data[data['BOT_ID'] == user_id][dm_field]
    try:
        if done_missions.values[0] == ' ':
            updated_done_missions = mission_id
        else:
            updated_done_missions = done_missions.values[0] + ', ' + mission_id
    except:
        updated_done_missions = mission_id

    data.loc[data['BOT_ID'] == user_id, dm_field] = updated_done_missions
    data.loc[data['BOT_ID'] == user_id, am_filed] = ' '

    data.to_csv(database_file, index=False, sep=';')


def all_active_missions(df, user_id):
    """
    For a given user_id returns all the active missions as a list of strings
    """
    active_missions = []
    active_missions.extend(df[df['BOT_ID'] == user_id]['AM_Aulari'])
    active_missions.extend(df[df['BOT_ID'] == user_id]['AM_Carpa'])
    active_missions.extend(df[df['BOT_ID'] == user_id]['AM_Civica'])
    active_missions.extend(df[df['BOT_ID'] == user_id]['AM_Comunicacio'])
    active_missions.extend(df[df['BOT_ID'] == user_id]['AM_EB_Sud'])
    active_missions.extend(df[df['BOT_ID'] == user_id]['AM_EB_Nord'])
    active_missions.extend(df[df['BOT_ID'] == user_id]['AM_EB_Central'])
    active_missions.extend(df[df['BOT_ID'] == user_id]['AM_ETSE'])
    active_missions.extend(df[df['BOT_ID'] == user_id]['AM_FTI'])
    active_missions.extend(df[df['BOT_ID'] == user_id]['AM_Med'])
    active_missions.extend(df[df['BOT_ID'] == user_id]['AM_SAF'])
    active_missions.extend(df[df['BOT_ID'] == user_id]['AM_EC'])
    active_missions.extend(df[df['BOT_ID'] == user_id]['AM_Torres'])
    active_missions.extend(df[df['BOT_ID'] == user_id]['AM_Vet'])
    active_missions = list(filter(lambda x: x != ' ', active_missions))
    return active_missions


def all_done_missions(df, user_id):
    """
    For a given user_id returns all the done missions as a list of strings
    """
    done_missions = []
    done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Aulari'])
    done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Carpa'])
    done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Civica'])
    done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Comunicacio'])
    done_missions.extend(df[df['BOT_ID'] == user_id]['DM_EB_Sud'])
    done_missions.extend(df[df['BOT_ID'] == user_id]['DM_EB_Nord'])
    done_missions.extend(df[df['BOT_ID'] == user_id]['DM_EB_Central'])
    done_missions.extend(df[df['BOT_ID'] == user_id]['DM_ETSE'])
    done_missions.extend(df[df['BOT_ID'] == user_id]['DM_FTI'])
    done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Med'])
    done_missions.extend(df[df['BOT_ID'] == user_id]['DM_SAF'])
    done_missions.extend(df[df['BOT_ID'] == user_id]['DM_EC'])
    done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Torres'])
    done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Vet'])
    done_missions = list(filter(lambda x: x != ' ', done_missions))
    return done_missions


def valid_answers(df, tam):
    """
    For a given list of strings containing mission_id returns a dit with the mission_id as key and the possible
    answers as value of the dict
    """
    va = dict()
    for am in tam:
        result_pool = df[df['MISSION_ID'] == am]['RESULT_POOL']
        try:
            va[am] = result_pool.values[0].split(", ")
        except IndexError:
            pass
    return va


def check_answer(user_id, answer):
    """
    For a given user_id and answer, check if the answer is part of a mission or not.
    In case it is returns the mission_id for the given answer's mission
    In case it is not, returns None
    """
    tam = all_active_missions(data, str(user_id))
    va = valid_answers(mission_data, tam)
    for key, value in va.items():
        if answer in value:
            return key

    return None

def read_QR(update, context):
    file = update.message.photo[-1].file_id
    obj = context.bot.get_file(file)
    tmp_dir = tempfile.mkdtemp()
    filename = os.path.join(tmp_dir, 'tmp_file.jpg')
    obj.download(filename)
    img = cv2.imread(filename=filename)
    shutil.rmtree(tmp_dir)
    det = cv2.QRCodeDetector()
    val, pts, st_code = det.detectAndDecode(img)
    if val == "":
        update.message.reply_text("Esta imagen no contiene ningún QR!")
    else:
        if val in mission_ids:
            done_missions = all_done_missions(data, update.message.chat['id'])
            if val in done_missions:
                update.message.reply_text("Ja has fet aquesta missió!!")
            else:
                throw_mission(update, val, update.message.chat['id'])
        else:
            update.message.reply_text("Aquest QR no té cap missió associada!")


def throw_mission(update, mission_id, user_id):
    # TODO: Check mission is not already done
    text = mission_data[mission_data['MISSION_ID'] == mission_id]['MISSION']
    am = mission_data[mission_data['MISSION_ID'] == mission_id]['AM_BUILDING']
    data.loc[data['BOT_ID'] == str(user_id), str(am.values[0])] = mission_id
    data.to_csv(database_file, index=False, sep=';')
    try:
        update.message.reply_text(text.values[0])
    except:
        update.message.reply_text("Hi ha un problema amb la base de dades d'aquesta missió, si us plau contacta amb el moderador Shaggy, gracies :)")


def write_in_db(bot_id, field, value):
    if bot_id in registred_ids:
        pass
    else:
        new_register(bot_id, data)


def new_register(bot_id, df):
    global data
    new_row = dict()
    field = 'BOT_ID'
    for column in data.columns:
        if column == field:
            new_row[column] = str(bot_id)
        else:
            new_row[column] = 0

    # Registration for new players
    new_row['Level'] = 'Player'
    new_row['Corruptus'] = 'False'
    new_row['Anomalis'] = 'False'

    # Set missions to a empty value
    new_row['AM_Aulari'] = ' '
    new_row['AM_Carpa'] = ' '
    new_row['AM_Civica'] = ' '
    new_row['AM_Comunicacio'] = ' '
    new_row['AM_EB_Sud'] = ' '
    new_row['AM_EB_Nord'] = ' '
    new_row['AM_EB_Central'] = ' '
    new_row['AM_Educacio'] = ' '
    new_row['AM_ETSE'] = ' '
    new_row['AM_FTI'] = ' '
    new_row['AM_Med'] = ' '
    new_row['AM_SAF'] = ' '
    new_row['AM_EC'] = ' '
    new_row['AM_Torres'] = ' '
    new_row['AM_Vet'] = ' '

    new_row['DM_Aulari'] = ' '
    new_row['DM_Carpa'] = ' '
    new_row['DM_Civica'] = ' '
    new_row['DM_Comunicacio'] = ' '
    new_row['DM_EB_Sud'] = ' '
    new_row['DM_EB_Nord'] = ' '
    new_row['DM_EB_Central'] = ' '
    new_row['DM_Educacio'] = ' '
    new_row['DM_ETSE'] = ' '
    new_row['DM_FTI'] = ' '
    new_row['DM_Med'] = ' '
    new_row['DM_SAF'] = ' '
    new_row['DM_EC'] = ' '
    new_row['DM_Torres'] = ' '
    new_row['DM_Vet'] = ' '

    # ID registration
    new_row['ID'] = max(data['ID']) + 1

    # Save the new data to database
    data = data.append(new_row, ignore_index=True)
    data.to_csv(database_file, index=False, sep=';')

    # Update the registred id's
    global registred_ids
    registred_ids = data['BOT_ID'].tolist()


# LOGIC AND FUNCTIONALITY
def missions(update, context):
    update.message.reply_text('En quina zona vols fer una missio?'
                              '\n/Aulari'
                              '\n/Carpa'
                              '\n/Civica'
                              '\n/Comunicacio'
                              '\n/Edifici_B_central'
                              '\n/Edifici_B_Nord'
                              '\n/Edifici_B_Sud'
                              '\n/Edifici_C'
                              '\n/Educacio'
                              '\n/Etse'
                              '\n/FTI'
                              '\n/Medicina'
                              '\n/SAF'
                              '\n/Torres'
                              '\n/Veterinaria')


def Aulari(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'Aulari Central')
    # TODO: index WIP
    index = 0
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def Carpa(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'Carpa letras')
    # TODO: index WIP
    index = 0
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def Civica(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'Civica')
    # TODO: index WIP
    index = 0
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def Comunicacio(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'Comunicación')
    # TODO: index WIP
    index = 0
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def Edifici_B_central(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'Edifici B central')
    # TODO: index WIP
    index = 0
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def Edifici_B_Nord(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'Edifici B Nord')
    # TODO: index WIP
    index = 0
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def Edifici_B_Sud(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'Edifici B Sud')
    # TODO: index WIP
    index = 0
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def Edifici_C(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'Edifici C')
    # TODO: index WIP
    index = 0
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def Educacio(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'Educació')
    # TODO: index WIP
    index = 0
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def Etse(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'Etse')
    # TODO: index WIP
    index = 0
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def FTI(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'FTI')
    # TODO: index WIP
    index = 0
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def Medicina(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'Medicina')
    # TODO: index WIP
    index = 0
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def SAF(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'SAF')
    # TODO: index WIP
    index = 0
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def Torres(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'Torres Applus')
    # TODO: index WIP
    index = 0
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def Veterinaria(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'Veterinaria')
    # TODO: index WIP
    index = 0
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Bienvenides a HvZ!')


def register(update, context):
    bot_id = update.message.chat['id']
    if str(bot_id) in registred_ids:
        update.message.reply_text('Tu registro ya está completado')
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
    """Check the message and act if it's an answer"""
    answer = update.message.text
    user_id = update.message.chat['id']
    if user_id in registred_ids:
        new_register(user_id, data)
    mission_solved = check_answer(user_id, answer)
    if mission_solved:
        to_send = "Enhorabona!! Has respost correctament la missio " + mission_solved + ". Continua així!"
        update.message.reply_text(to_send)
        mission_accomplished(user_id, mission_solved)
    else:
        update.message.reply_text("El missatge que has enviat no és cap resposta de les teves missions actives!")
        update.message.reply_text("Escriu /help per saber més de com funciona el bot")


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

    # Mission handlers
    dp.add_handler(CommandHandler("missions", missions))
    dp.add_handler(CommandHandler("Aulari", Aulari))
    dp.add_handler(CommandHandler("Carpa", Carpa))
    dp.add_handler(CommandHandler("Civica", Civica))
    dp.add_handler(CommandHandler("Comunicacio", Comunicacio))
    dp.add_handler(CommandHandler("Edifici_B_Central", Edifici_B_central))
    dp.add_handler(CommandHandler("Edifici_B_Nord", Edifici_B_Nord))
    dp.add_handler(CommandHandler("Edifici_B_Sud", Edifici_B_Sud))
    dp.add_handler(CommandHandler("Edifici_C", Edifici_C))
    dp.add_handler(CommandHandler("Educacio", Educacio))
    dp.add_handler(CommandHandler("ETSE", Etse))
    dp.add_handler(CommandHandler("FTI", FTI))
    dp.add_handler(CommandHandler("Medicina", Medicina))
    dp.add_handler(CommandHandler("SAF", SAF))
    dp.add_handler(CommandHandler("Torres", Torres))
    dp.add_handler(CommandHandler("Veterinaria", Veterinaria))

    # on noncommand i.e message - tree decision (WIP)
    dp.add_handler(MessageHandler(Filters.text, echo))

    # on noncommand i.e pictures - activate QR protocol
    dp.add_handler(MessageHandler(Filters.photo, read_QR))

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