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
from random import randrange
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

NPC_file = os.path.join(sys.path[0], 'NPC_database.csv')
NPC_data = pd.read_csv(NPC_file, sep=';', header=0, encoding='cp1252')


# Functions about all the things of a given user
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


def amount_of_missions_done(df, user_id):
    """
    For a given user_id returns the amount of missions done by this user
    """
    amount_missions = 0
    amount_missions += df[df['BOT_ID'] == user_id]['TM_Aulari']
    amount_missions += df[df['BOT_ID'] == user_id]['TM_Carpa']
    amount_missions += df[df['BOT_ID'] == user_id]['TM_Civica']
    amount_missions += df[df['BOT_ID'] == user_id]['TM_Comunicacio']
    amount_missions += df[df['BOT_ID'] == user_id]['TM_EB_Sud']
    amount_missions += df[df['BOT_ID'] == user_id]['TM_EB_Nord']
    amount_missions += df[df['BOT_ID'] == user_id]['TM_EB_Central']
    amount_missions += df[df['BOT_ID'] == user_id]['TM_ETSE']
    amount_missions += df[df['BOT_ID'] == user_id]['TM_FTI']
    amount_missions += df[df['BOT_ID'] == user_id]['TM_Med']
    amount_missions += df[df['BOT_ID'] == user_id]['TM_SAF']
    amount_missions += df[df['BOT_ID'] == user_id]['TM_EC']
    amount_missions += df[df['BOT_ID'] == user_id]['TM_Torres']
    amount_missions += df[df['BOT_ID'] == user_id]['TM_Vet']
    return amount_missions.values[0]


def user_points(df, user_id):
    """
    For a given user_id returns the amount of points achieved due to missions
    """
    total_points = 0
    total_points += df[df['BOT_ID'] == user_id]['P_Aulari']
    total_points += df[df['BOT_ID'] == user_id]['P_Carpa']
    total_points += df[df['BOT_ID'] == user_id]['P_Civica']
    total_points += df[df['BOT_ID'] == user_id]['P_Comunicacio']
    total_points += df[df['BOT_ID'] == user_id]['P_EB_Sud']
    total_points += df[df['BOT_ID'] == user_id]['P_EB_Nord']
    total_points += df[df['BOT_ID'] == user_id]['P_EB_Central']
    total_points += df[df['BOT_ID'] == user_id]['P_ETSE']
    total_points += df[df['BOT_ID'] == user_id]['P_FTI']
    total_points += df[df['BOT_ID'] == user_id]['P_Med']
    total_points += df[df['BOT_ID'] == user_id]['P_SAF']
    total_points += df[df['BOT_ID'] == user_id]['P_EC']
    total_points += df[df['BOT_ID'] == user_id]['P_Torres']
    total_points += df[df['BOT_ID'] == user_id]['P_Vet']
    return total_points.values[0]


# TOOLS
def mission_accomplished(user_id, mission_id):
    """
    Function that handles an accomplished mission:
     - Erases the active mission to empty
     - Added the accomplished mission to the done pile
     - Adds one the total mission accomplished
     - Adds the points value to the total value points of the user
    """
    building = mission_data[mission_data['MISSION_ID'] == mission_id]['AM_BUILDING']
    am_filed = building.values[0]
    dm_field = 'D' + am_filed[1:]
    tm_field = 'T' + am_filed[1:]
    p_field = 'P' + am_filed[2:]
    done_missions = data[data['BOT_ID'] == user_id][dm_field]
    total_missions = data[data['BOT_ID'] == user_id][tm_field]
    mission_points = mission_data[mission_data['MISSION_ID'] == mission_id]['POINTS']
    total_points = data[data['BOT_ID'] == user_id][p_field]
    try:
        if done_missions.values[0] == ' ':
            updated_done_missions = mission_id
        else:
            updated_done_missions = done_missions.values[0] + ', ' + mission_id
    except:
        updated_done_missions = mission_id

    data.loc[data['BOT_ID'] == user_id, am_filed] = ' '
    data.loc[data['BOT_ID'] == user_id, dm_field] = updated_done_missions
    data.loc[data['BOT_ID'] == user_id, tm_field] = int(total_missions.values[0]) + 1
    data.loc[data['BOT_ID'] == user_id, p_field] = int(total_points.values[0]) + int(mission_points)

    try:
        npc = str(mission_data[mission_data['MISSION_ID'] == mission_id]['NPC'].values[0])
        faction = str(data[data['BOT_ID'] == user_id]['FACTION'].values[0])
        add_influence(npc, mission_points % 10, faction)
    except IndexError:
        pass

    data.to_csv(database_file, index=False, sep=';')


def add_influence(npc_name, influence_points, user_faction):
    actual_points = NPC_data[NPC_data['NAME'] == npc_name]['FAVOR']
    favor_value = position_value(actual_points, user_faction)
    NPC_data.loc[NPC_data['NAME'] == npc_name, 'FAVOR'] = actual_points + (influence_points * favor_value)
    NPC_data.to_csv(NPC_file, index=False, sep=';')


def position_value(npc_favor, user_faction):
    if user_faction == 'Anomalis':
        return 1
    if user_faction == 'Corruptus':
        return -1

    if user_faction == 'Neutral':
        if npc_favor > 0:
            return -1
        if npc_favor < 0:
            return 1
        if npc_favor == 0:
            return 0


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


def check_pic(user_id, photo_id):
    df_pics = os.path.join(sys.path[0], 'fotos_database.csv')
    db_pics = pd.read_csv(df_pics, sep=';', header=0)
    pics = db_pics['IMAGE_ID'].tolist()
    if photo_id in pics:
        return True
    else:
        new_row = dict()
        new_row['BOT_ID'] = user_id
        new_row['IMAGE_ID'] = photo_id

        db_pics = db_pics.append(new_row, ignore_index=True)
        db_pics.to_csv(df_pics, index=False, sep=';')
        return False


def read_QR(update, context):
    if check_pic(str(update.message.chat['id']), update.message.photo[-1].file_unique_id):
        update.message.reply_text("Aquesta foto ja s'ha fet servir!!")
        return 0
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
    text = mission_data[mission_data['MISSION_ID'] == mission_id]['MISSION_P1']
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
    new_row['ALIAS'] = 'no_alias'
    new_row['GUILD'] = ' '
    new_row['GUILD_LEVEL'] = 'unguilded'
    new_row['Level'] = 'Player'
    new_row['FACTION'] = 'Neutral'

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
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def Carpa(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'Carpa letras')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def Civica(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'Civica')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def Comunicacio(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'Comunicación')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def Edifici_B_central(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'Edifici B central')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def Edifici_B_Nord(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'Edifici B Nord')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def Edifici_B_Sud(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'Edifici B Sud')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def Edifici_C(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'Edifici C')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def Educacio(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'Educació')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def Etse(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'Etse')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def FTI(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'FTI')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def Medicina(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'Medicina')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def SAF(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'SAF')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def Torres(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'Torres Applus')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def Veterinaria(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'Veterinaria')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)


# Team related functions
def create_team(update, context):
    global data
    team_name = str(update.message.text)[12:]
    user_id = str(update.message.chat['id'])
    if user_id not in registred_ids:
        new_register(user_id, data)

    data.loc[data['BOT_ID'] == user_id, 'GUILD'] = team_name
    data.loc[data['BOT_ID'] == user_id, 'GUILD_LEVEL'] = 'Founder'

    data.to_csv(database_file, index=False, sep=';')

    reply_message = "L'equip " + team_name + " s'ha creat correctament!!! El teu rang és \"Founder\""
    update.message.reply_text(reply_message)


def join_team(update, context):
    global data
    team_name = str(update.message.text)[10:]
    user_id = str(update.message.chat['id'])
    if user_id not in registred_ids:
        new_register(user_id, data)

    if team_name in data['GUILD'].tolist():
        data.loc[data['BOT_ID'] == user_id, 'GUILD'] = team_name
        data.loc[data['BOT_ID'] == user_id, 'GUILD_LEVEL'] = 'Newbie'

        data.to_csv(database_file, index=False, sep=';')

        reply_message = "T'has unit a l'equip " + team_name + " correctament!!! El teu rang és \"Newbie\""
        update.message.reply_text(reply_message)

    else:
        reply_message = "L'equip " + team_name + " no existeix!!! Comproba que ho hagis escrit correctament! Majúscules incloses!"
        update.message.reply_text(reply_message)


def show_team(update, context):
    bot_id = str(update.message.chat['id'])
    guild_name = str(data[data['BOT_ID'] == bot_id]['GUILD'].values[0])
    if bot_id not in registred_ids:
        new_register(bot_id, data)

    if guild_name == ' ':
        update.message.reply_text("No estàs a cap equip!")
    else:
        guild_ids = data[data['GUILD'] == guild_name]['BOT_ID'].tolist()
        output_text = ""
        for bid in guild_ids:
            output_text += "La persona amb alies: " + str(data[data['BOT_ID'] == bid]["ALIAS"].values[0])
            done_missions = amount_of_missions_done(data, bid)
            tp = user_points(data, bid)
            output_text += " ha fet " + str(done_missions) + " missions"
            output_text += "\nTé acumulats " + str(tp)
            output_text += " punts per la seva faccio\n\n"

        update.message.reply_text(output_text)


def promote(update, context):
    text = str(update.message.text)[9:]
    values = text.split(", ")
    bot_id = str(update.message.chat['id'])

    if bot_id not in registred_ids:
        new_register(bot_id, data)
        update.message.reply_text("El teu registre no estava complert! Si us plau uneix-te a un equip primer")
        return 0

    own_alias = str(data[data['BOT_ID'] == bot_id]['ALIAS'].values[0])
    guild_name = str(data[data['BOT_ID'] == bot_id]['GUILD'].values[0])
    if guild_name == " ":
        update.message.reply_text("No formes part de cap equip!")
        return 0

    guild_level = str(data[data['BOT_ID'] == bot_id]['GUILD_LEVEL'].values[0])
    if guild_level != "Founder":
        update.message.reply_text("Només els \"Founders\" poden promocionar gent del seu equip!")
        return 0

    if values[0] == own_alias:
        update.message.reply_text("Els \"Founders\" no poden canviar el seu propi rang!")
        return 0

    data.loc[(data['GUILD'] == guild_name) & (data['ALIAS'] == str(values[0])), 'GUILD_LEVEL'] = str(values[1])
    data.to_csv(database_file, index=False, sep=';')

    output_text = "Totes les persones amb alies " + values[0] + " han sigut ascendides a " + values[1]
    update.message.reply_text(output_text)


# Personal stuff related methods
def set_alias(update, context):
    alias = str(update.message.text)[10:]
    bot_id = str(update.message.chat['id'])
    if bot_id not in registred_ids:
        new_register(bot_id, data)

    if alias == '' or alias is None:
        update.message.reply_text("L'alias que has escollit no és vàlid!!")
    else:
        data.loc[data['BOT_ID'] == bot_id, 'ALIAS'] = alias
        data.to_csv(database_file, index=False, sep=';')

        output_text = 'El teu alias ha canviat correctament a ' + alias
        update.message.reply_text(output_text)


def show_me(update, context):
    bot_id = str(update.message.chat['id'])
    if bot_id not in registred_ids:
        new_register(bot_id, data)

    output_text = "El teu alias és " + str(data[data['BOT_ID'] == bot_id]['ALIAS'].values[0]) + "\n"
    output_text += "El teu equip és " + str(data[data['BOT_ID'] == bot_id]['GUILD'].values[0]) + "\n"
    output_text += "El teu rang és " + str(data[data['BOT_ID'] == bot_id]['GUILD_LEVEL'].values[0]) + "\n"
    output_text += "La teva facció és " + str(data[data['BOT_ID'] == bot_id]['FACTION'].values[0]) + "\n"

    dm = amount_of_missions_done(data, bot_id)
    tp = user_points(data, bot_id)

    output_text += "Has fet un total de " + str(dm) + " missions per tot el campus\n"
    output_text += "Tens acumulats un total de " + str(tp) + " punts per la teva facció\n"

    update.message.reply_text(output_text)


def activity(update, context):
    bot_id = str(update.message.chat['id'])
    if bot_id not in registred_ids:
        new_register(bot_id, data)

    am = all_active_missions(data, bot_id)
    output_text = "Missions actives acutals, codi i enunciat\n"
    for m in am:
        output_text += str(m) + ": "
        output_text += str(mission_data[mission_data['MISSION_ID'] == m]['MISSION_P1'].values[0])
        output_text += "\n"

    update.message.reply_text(output_text)


def hint(update, context):
    bot_id = str(update.message.chat['id'])
    if bot_id not in registred_ids:
        new_register(bot_id, data)

    am = str(update.message.text)[6:]

    real_active = all_active_missions(data, bot_id)
    if am not in real_active:
        output_text = "La missió per la que demanes pista no és una missió que tinguis activa! " \
                      "Troba i escaneja el seu QR primer!"
        update.message.reply_text(output_text)
        return 0

    try:
        pista = str(mission_data[mission_data['MISSION_ID'] == am]['HINT'].values[0])
        output_text = "La pista per la missió amb codi " + am + " és:\n"
        output_text += pista

    except IndexError:
        output_text = "La missió de la qual demanes no té pista"

    update.message.reply_text(output_text)


def join_anomalis(update, context):
    bot_id = str(update.message.chat['id'])
    if bot_id not in registred_ids:
        new_register(bot_id, data)

    actual_faction = str(data[data['BOT_ID'] == bot_id]['FACTION'].values[0])
    if actual_faction == 'Neutral':
        data.loc[data['BOT_ID'] == bot_id, 'FACTION'] = 'Anomalis'
        data.to_csv(database_file, index=False, sep=';')
        output_text = "Ja t'has unit a la facció, ara uneix-te al canal de la teva facció: https://t.me/joinchat/PKx1bv81WUMyMGU0"
        update.message.reply_text(output_text)
    else:
        output_text = "Tu ja ets " + actual_faction + ". No es pot canviar de facció. Contacta amb els organitzadors" \
                                                      "per demanar-ho"
        update.message.reply_text(output_text)


def join_corruptus(update, context):
    bot_id = str(update.message.chat['id'])
    if bot_id not in registred_ids:
        new_register(bot_id, data)

    actual_faction = str(data[data['BOT_ID'] == bot_id]['FACTION'].values[0])
    if actual_faction == 'Neutral':
        data.loc[data['BOT_ID'] == bot_id, 'FACTION'] = 'Corruptus'
        data.to_csv(database_file, index=False, sep=';')
        output_text = "Ja t'has unit a la facció, uneix-te al canal de la teva facció: https://t.me/joinchat/dLP2gZDhDKUwMmZk"
        update.message.reply_text(output_text)
    else:
        output_text = "Tu ja ets " + actual_faction + ". No es pot canviar de facció. Contacta amb els organitzadors" \
                                                      "per demanar-ho"
        update.message.reply_text(output_text)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    bot_id = str(update.message.chat['id'])
    if bot_id not in registred_ids:
        new_register(bot_id, data)
    output_text = """Hola, ¡soy el bot que os va a estar ayudando esta edición!

Os voy a hacer un pequeño resumen de como usarme, no os preocupéis, ¡es muy fácil!

Para registraros, el formulario de inscripción os pedirá el ID, tu ID es: {}. Para tener vuestro ID con un formato fácil de copiar, escribid /getmyid. Si no sabes de qué formulario te hablo, sigue este link: https://bit.ly/3meBpHL

Si tenéis cualquier duda sobre qué comandos utilizar, escribid /help. Allí os explicaré los comandos principales que tengo y como usarlos. 

Si queréis saber como funcionan las normas, escribid /use. Allí os explicaré como hacer y resolver las misiones. 

Si tenéis dudas que yo no os pueda responder, escribid /contact. Allí os pasaremos el contacto de algún moderador que os podrá resolver la duda personalmente. 

Si queréis volver a leer este mensaje en algún momento, escribid /start. 

No hace falta que siempre escribáis los comandos, podéis pulsar encima del comando y se activará automáticamente. 

Por último, si ya sabéis a qué Facción pertenecéis, usad el comando /joincorruptus o /joinanomalis. 

¡Muchas gracias por participar, a jugar!""".format(bot_id)
    update.message.reply_text(output_text)


def register(update, context):
    bot_id = update.message.chat['id']
    if str(bot_id) in registred_ids:
        update.message.reply_text('Tu registro ya está completado')
    else:
        new_register(bot_id, data)
        update.message.reply_text('Te has registrado!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Esto es la ayuda! Este comando aun está en desarrollo')


def use(update, context):
    update.message.reply_text('Esto es la guía de uso! Este comando aun está en desarrollo')


def contact(update, context):
    output_text = """Para hablar con un organizador abre conversación a una de las siguientes personas:
@ShaggyGalaso
@Janadsb99
@Nel_tu_mod_fav"""
    update.message.reply_text(output_text)


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
        mission_accomplished(str(user_id), mission_solved)
    else:
        update.message.reply_text("El missatge que has enviat no és cap resposta de les teves missions actives!")
        update.message.reply_text("Escriu /help per saber més de com funciona el bot")


def get_my_id(update, context):
    update.message.reply_text(update.message.chat['id'])


def test(update, context):
    print(update.message)
    print(update.message.text)
    print(str(update.message.text)[6:])


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1975748853:AAG2-lzGxFToo0d2-hVwQQ7f_t499SEU_fk", use_context=True)
    path = os.path.join(sys.path[0], 'zarigueyas.txt')
    file = open(path, "r")
    zz = file.read()
    file.close()
    updater = Updater(zz, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Commands related to teams
    dp.add_handler(CommandHandler("createteam", create_team))
    dp.add_handler(CommandHandler("jointeam", join_team))
    dp.add_handler(CommandHandler("showteam", show_team))
    dp.add_handler(CommandHandler("promote", promote))

    # Commands related to personal stuff
    dp.add_handler(CommandHandler("setalias", set_alias))
    dp.add_handler(CommandHandler("stats", show_me))
    dp.add_handler(CommandHandler("activity", activity))
    dp.add_handler(CommandHandler("hint", hint))
    dp.add_handler(CommandHandler("joinanomalis", join_anomalis))
    dp.add_handler(CommandHandler("joincorruptus", join_corruptus))

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("halal", halal))
    dp.add_handler(CommandHandler("corruptus", corruptus))
    dp.add_handler(CommandHandler("test", test))
    dp.add_handler(CommandHandler("use", use))
    dp.add_handler(CommandHandler("contact", contact))

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