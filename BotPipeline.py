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

from random import randrange, choice
from googletrans import Translator

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import requests
from bs4 import BeautifulSoup

from random import randint

# CONTANTS (frogs actually but u know, i don't even care anymore)
list_of_frogs = [
"http://www.allaboutfrogs.org/funstuff/random/0001.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0002.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0003.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0004.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0005.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0006.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0007.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0008.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0009.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0010.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0011.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0012.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0013.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0014.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0015.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0016.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0017.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0018.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0019.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0020.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0021.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0022.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0023.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0024.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0025.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0026.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0027.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0028.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0028.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0029.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0030.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0031.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0032.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0033.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0034.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0035.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0036.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0037.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0038.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0039.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0040.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0041.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0042.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0043.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0044.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0045.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0046.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0047.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0048.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0049.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0050.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0051.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0052.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0053.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0054.jpg"
]

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

translator = Translator(service_urls=[
      'translate.google.com',
      'translate.google.co.kr',
    ])


conver_file = os.path.join(sys.path[0], 'conversation_database.csv')
conver_data = pd.read_csv(conver_file, sep=';', header=0, dtype={'BOT_ID': str}, encoding='cp1252')
talk_input = conver_data['INPUT'].tolist()
talk_output = conver_data['OUTPUT'].tolist()
talk = {k: v for k, v in zip(talk_input, talk_output)}

teams_file = os.path.join(sys.path[0], 'teams_database.csv')
teams_data = pd.read_csv(teams_file, sep=';', header=0, encoding='cp1252', dtype={'FOUNDER': str})


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
    final_missions = []
    for ms in done_missions:
        missions_subset = ms.split(", ")
        for mis in missions_subset:
            final_missions.append(mis)
    return final_missions


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


def dict_of_missions(ams, ret={}):
    ams = list(filter(lambda x: x != ' ', ams))
    for p in ams:
        ms = p.split(", ")
        for m in ms:
            try:
                ret[m] += 1
            except:
                ret[m] = 1

    return ret


def dict_missions_in_zone(zone, ret={}):
    m = data[zone]
    return dict_of_missions(m, ret)


def anomalis_missions_in_zone(zone, ret={}):
    m = data[data['FACTION'] == 'Anomalis'][zone]
    return dict_of_missions(m, ret)


def corruptus_missions_in_zone(zone, ret={}):
    m = data[data['FACTION'] == 'Corruptus'][zone]
    return dict_of_missions(m, ret)


def humanize_mission_dict(d):
    d = dict(sorted(d.items(), key=lambda item: item[1], reverse=True))
    output_text = ""
    counter = 1
    for key, value in d.items():
        try:
            npc = str(mission_data[mission_data['MISSION_ID'] == key]['NPC'].values[0])
        except:
            npc = ' '

        output_text += str(counter) + ". *" + npc + "* - " + str(value) + " (" + str(key) + ")\n"
        counter += 1

    return output_text


def active_players(df):
    all_ids = df['BOT_ID'].tolist()
    count = 0
    for i in all_ids:
        m = amount_of_missions_done(df, i)
        if m > 0:
            count += 1
    return count


# TEAM HELPER FUNCTIONS
def check_is_founder(user_id):
    founders = teams_data['FOUNDER'].tolist()
    if user_id in founders:
        return True
    else:
        return False

# FUNNY FUNCTIONS
def get_boop():
    page = "https://random.dog/"
    content = requests.get(page)

    if content.status_code == 200:
        soup = BeautifulSoup(content.content, "html.parser")

    while soup.img is None:
        content = requests.get(page)
        soup = BeautifulSoup(content.content, "html.parser")

    return page + str(soup.img)[23:-3]


# TOOLS
def select_language(l):
    if l == 'Català':
        return 'ca'
    elif l == "Castellano":
        return 'es'
    elif l == 'English':
        return 'en'
    else:
        return l


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
        # add_influence(npc, mission_points % 10, faction)
    except IndexError:
        pass

    data.to_csv(database_file, index=False, sep=';')

    final_text = str(mission_data[mission_data['MISSION_ID'] == mission_id]['FINAL_TEXT'].values[0])
    if final_text != 'None':
        return final_text
    else:
        return None


def mission_can_be_done(user_id, mission_id):
    """
    Function that checks requirements for a mission and a person
     - Checks that missions indeed has requirements
     - In case yes, checks if one or multiple
       - For multiple checks all of them
       - If all done return None
       - If else returns all pending
     - In case not, checks if it's done
       - If it's done returns None
       - If else returns pending mission
    """
    dm = all_done_missions(data, user_id)
    mr = str(mission_data[mission_data['MISSION_ID'] == mission_id]['REQUIREMENTS'].values[0])
    if mr == 'None':
        return None

    if ',' in mr:
        mr = mr.split(", ")
        ret_list = []
        for m in mr:
            if m not in dm:
                ret_list.append(m)

        if len(ret_list) == 0:
            return None
        else:
            return ret_list

    else:
        if mr in dm:
            return None
        else:
            return [mr]


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
    return False

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


def guild_points(guild_name):
    gdf = data[data['GUILD'] == guild_name]
    gids = gdf['BOT_ID'].tolist()
    t_points = 0
    for i in gids:
        t_points += user_points(gdf, i)

    return t_points


def read_QR(update, context):
    bot_id = str(update.message.chat['id'])
    if check_pic(bot_id, update.message.photo[-1].file_unique_id):
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

    # Missiones de Lore
    if "LORE" in val:
        own_faction = str(data[data['BOT_ID'] == bot_id]['FACTION'].values[0])
        if own_faction == "Neutral":
            update.message.reply_text("Necessites ser d'una facció per fer aquesta missió: /joinanomalis o /joincorruptus")
            return None

        num = 0
        for l in val:
            try:
                num = int(l)
                num *= 10
            except:
                pass
        num /= 10

        if own_faction == "Anomalis":
            val = "ANOMA" + str(int(num))
        if own_faction == "Corruptus":
            val = "CORRU" + str(int(num))

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
    pending = mission_can_be_done(str(user_id), mission_id)
    aam = all_active_missions(data, str(user_id))
    if pending:
        ret_text = "Encara et falten les següents missions!"
        for m in pending:
            ret_text += str(m) +": "
            if m in aam:
                ret_text += str(mission_data[mission_data['MISSION_ID'] == mission_id]['TEXT'].values[0])
                ret_text += "\n"
            else:
                ret_text += "Encara no has trobat aquesta missio!\n"
        update.message.reply_text(ret_text)
        return None

    text = str(mission_data[mission_data['MISSION_ID'] == mission_id]['MISSION_P1'].values[0])
    language = str(data[data['BOT_ID'] == str(user_id)]['LANGUAGE'].values[0])
    am = mission_data[mission_data['MISSION_ID'] == mission_id]['AM_BUILDING']
    data.loc[data['BOT_ID'] == str(user_id), str(am.values[0])] = mission_id
    data.to_csv(database_file, index=False, sep=';')
    if language == 'ca':
        final_text = text
    else:
        translated_text = translator.translate(text=text, dest=language)
        final_text = translated_text.text

    try:
        update.message.reply_text(final_text)
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
    new_row['LANGUAGE'] = 'ca'
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
    # if True:
    #     update.message.reply_text('Las missiones aun no están activadas, esperate a las 11:00!')
    # else:
    update.message.reply_text('En quina zona vols fer una missio?'
                          '\n/Comunicacio'
                          '\n/Edifici_B_central'
                          '\n/Edifici_B_Nord'
                          '\n/Edifici_B_Sud'
                          '\n/Edifici_C'
                          '\n/Etse'
                          '\n/FTI'
                          '\n/Medicina'
                          '\n/SAF'
                          '\n/Veterinaria')

        # '\n/Aulari'
        # '\n/Carpa'
        # '\n/Civica'
        # '\n/Torres'
        # '\n/Educacio'


def Aulari(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'QR activos')
    foto_path = os.path.join(foto_path, 'MED')
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
    foto_path = os.path.join(foto_path, 'QR activos')
    foto_path = os.path.join(foto_path, 'COM')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def Edifici_B_central(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'QR activos')
    foto_path = os.path.join(foto_path, 'BCEN')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def Edifici_B_Nord(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'QR activos')
    foto_path = os.path.join(foto_path, 'BNORD')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def Edifici_B_Sud(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'QR activos')
    foto_path = os.path.join(foto_path, 'BSUD')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def Edifici_C(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'QR activos')
    foto_path = os.path.join(foto_path, 'Ciencies')
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
    foto_path = os.path.join(foto_path, 'QR activos')
    foto_path = os.path.join(foto_path, 'ETSE')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def FTI(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'QR activos')
    foto_path = os.path.join(foto_path, 'FTI')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def Medicina(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'QR activos')
    foto_path = os.path.join(foto_path, 'MED')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)

def SAF(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'QR activos')
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
    foto_path = os.path.join(foto_path, 'QR activos')
    foto_path = os.path.join(foto_path, 'VET')
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

    global teams_data
    founders = teams_data['FOUNDER'].tolist()
    print(founders)

    if user_id in founders:
        print(founders)
        print("YES")
        old_guild = str(teams_data[teams_data['FOUNDER'] == user_id]['GUILD'].values[0])
        teams_data.loc[teams_data['FOUNDER'] == user_id, 'GUILD'] = team_name

        all_members = data[data['GUILD'] == old_guild]['BOT_ID'].tolist()

        if len(all_members) == 0:
            pass
        else:
            new_leader = choice(all_members)
            old_requests = teams_data[teams_data['GUILD'] == old_guild]['REQUESTS'].tolist()

            new_row = dict()
            new_row['GUILD'] = old_guild
            new_row['FOUNDER'] = new_leader
            if len(old_requests) == 0:
                new_row['REQUESTS'] = 'None'
            else:
                new_row['REQUESTS'] = ', '.join(str(r) for r in old_requests)

            teams_data = teams_data.append(new_row, ignore_index=True)
            teams_data.to_csv(teams_file, index=False, sep=';')

            context.bot.send_message(new_leader, "El fundador del teu equip ha marxat, ara ets el nou fundador!")

    else:
        new_row = dict()
        new_row['GUILD'] = team_name
        new_row['FOUNDER'] = user_id
        new_row['REQUESTS'] = 'None'

        teams_data = teams_data.append(new_row, ignore_index=True)
        teams_data.to_csv(teams_file,  index=False, sep=';')

    reply_message = "L'equip " + team_name + " s'ha creat correctament!!! El teu rang és \"Founder\""
    update.message.reply_text(reply_message)


def join_team(update, context):
    global teams_data
    team_name = str(update.message.text)[10:]
    user_id = str(update.message.chat['id'])
    if user_id not in registred_ids:
        new_register(user_id, data)
    own_alias = str(data[data['BOT_ID'] == user_id]['ALIAS'].values[0])

    if team_name in teams_data['GUILD'].tolist():
        actual_requests = teams_data[teams_data['GUILD'] == team_name]['REQUESTS'].tolist()
        actual_requests.append(user_id)
        actual_requests = ', '.join(str(r) for r in actual_requests)
        teams_data.loc[data['GUILD'] == team_name, 'REQUESTS'] = actual_requests
        update.message.reply_text("La teva solucitud s'ha completat correctament!!")

        team_leader = str(teams_data[teams_data['GUILD'] == team_name]['FOUNDER'].values[0])
        leader_text = "La persona amb alias: " + own_alias + " es vol unir al teu equip! Per acceptar copia la següent comanda:"
        context.bot.send_message(team_leader, leader_text)
        leader_text = "/admit " + user_id
        context.bot.send_message(team_leader, leader_text)
        leader_text = "Per reubitjar-la, copia la següent comanda: "
        context.bot.send_message(team_leader, leader_text)
        leader_text = "/decline " + user_id
        context.bot.send_message(team_leader, leader_text)

    else:
        update.message.reply_text("No hi ha cap equip amb aquest nom!!")


def join_team_old(update, context):
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
    if len(values) == 1:
        update.message.reply_text("Compte! Has de separar l'alias i el rang per una coma i només un espai!")
        return None
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

    # guild_level = str(data[data['BOT_ID'] == bot_id]['GUILD_LEVEL'].values[0])
    founders = teams_data['FOUNDER'].tolist()
    if bot_id not in founders:
        update.message.reply_text("Només els \"Founders\" poden promocionar gent del seu equip!")
        return 0

    # if values[0] == own_alias:
    #     update.message.reply_text("Els \"Founders\" no poden canviar el seu propi rang!")
    #     return 0

    data.loc[(data['GUILD'] == guild_name) & (data['ALIAS'] == str(values[0])), 'GUILD_LEVEL'] = str(values[1])
    data.to_csv(database_file, index=False, sep=';')

    output_text = "Totes les persones amb alies " + values[0] + " han sigut ascendides a " + values[1]
    update.message.reply_text(output_text)


def kick(update, context):
    global data
    text = str(update.message.text)[6:]
    bot_id = str(update.message.chat['id'])
    if check_is_founder(bot_id):
        team_name = str(teams_data[teams_data['FOUNDER'] == bot_id]['GUILD'].values[0])
        if text == bot_id:
            update.message.reply_text("No et pots fer fora a tu mateix del teu equip!")
            return None
        member_ids = data[data['GUILD'] == team_name]['BOT_ID'].tolist()
        for i in member_ids:
            if text == str(i):
                print("YAS")
                data.loc[data['BOT_ID'] == i, 'GUILD'] = ' '
                data.loc[data['BOT_ID'] == i, 'GUILD_LEVEL'] = 'unguilded'
                data.to_csv(database_file, index=False, sep=';')
                update.message.reply_text("Has expulsat a la persona del teu equip!")
                context.bot.send_message(i, "T'han fet fora del teu equip!")
                return None
        update.message.reply_text("No hi ha ningú amb aquest id al teu equip!")
    else:
        update.message.reply_text("Només els founders poden fer fora a algu de l'equip!")


def admit(update, context):
    global data
    global teams_data
    text = str(update.message.text)[7:]
    bot_id = str(update.message.chat['id'])
    if check_is_founder(bot_id):
        team_name = str(teams_data[teams_data['FOUNDER'] == bot_id]['GUILD'].values[0])

        all_ids = data['BOT_ID'].tolist()
        if text not in all_ids:
            update.message.reply_text("Aquest id no està registrat al bot!!")
            return None

        requested_ids = str(teams_data[teams_data['FOUNDER'] == bot_id]['REQUESTS'].values[0])
        requested_ids = requested_ids.split(", ")
        if text not in requested_ids:
            update.message.reply_text("Aquest id no ha demanat entrar al teu equip!")
            return None

        data.loc[data['BOT_ID'] == text, 'GUILD'] = team_name
        data.loc[data['BOT_ID'] == text, 'GUILD_LEVEL'] = 'Newbie'

        data.to_csv(database_file, index=False, sep=';')

        actual_requests = str(teams_data[teams_data['FOUNDER'] == bot_id]['REQUESTS'].values[0])
        actual_requests = actual_requests.split(", ")
        actual_requests.remove(text)
        if len(actual_requests) == 0:
            actual_requests = 'None'
        else:
            actual_requests = ', '.join(str(r) for r in actual_requests)
        teams_data.loc[teams_data['FOUNDER'] == bot_id, 'REQUESTS'] = actual_requests

        teams_data.to_csv(teams_file, index=False, sep=';')

        update.message.reply_text("Has acceptat a l'usuari amb id " + text)
        context.bot.send_message(text, "Has entrat a l'equip: " + team_name)
    else:
        update.message.reply_text("Només els founders poden ademtre a algu a l'equip!")


def decline(update, context):
    global data
    global teams_data
    text = str(update.message.text)[9:]
    bot_id = str(update.message.chat['id'])
    if check_is_founder(bot_id):
        all_ids = data['BOT_ID'].tolist()
        if text not in all_ids:
            update.message.reply_text("Aquest id no està registrat al bot!!")
            return None

        requested_ids = str(teams_data[teams_data['FOUNDER'] == bot_id]['REQUESTS'].values[0])
        requested_ids = requested_ids.split(", ")
        if text not in requested_ids:
            update.message.reply_text("Aquest id no ha demanat entrar al teu equip!")
            return None

        actual_requests = str(teams_data[teams_data['FOUNDER'] == bot_id]['REQUESTS'].values[0])
        actual_requests = actual_requests.split(", ")
        actual_requests.remove(text)
        if len(actual_requests) == 0:
            actual_requests = 'None'
        else:
            actual_requests = ', '.join(str(r) for r in actual_requests)
        teams_data.loc[teams_data['FOUNDER'] == bot_id, 'REQUESTS'] = actual_requests

        teams_data.to_csv(teams_file, index=False, sep=';')

        update.message.reply_text("Has denegat a l'usuari amb id " + text + ". No se li comunicarà res a aquesta persona")
    else:
        update.message.reply_text("Només els founders poden ademtre a algu a l'equip!")


def mem_ids(update, context):
    bot_id = str(update.message.chat['id'])
    if check_is_founder(bot_id):
        team_name = str(teams_data[teams_data['FOUNDER'] == bot_id]['GUILD'].values[0])
        m_ids = data[data['GUILD'] == team_name]['BOT_ID'].tolist()
        output_text = "Els ids del teu equip són els següents:\n\n"
        for i in m_ids:
            output_text += "ID: " + str(i)
            alias = str(data[data['BOT_ID'] == str(i)]['ALIAS'].values[0])
            output_text += ". Alias: " + alias
            g_lvl = str(data[data['BOT_ID'] == str(i)]['GUILD_LEVEL'].values[0])
            output_text += ". Rang: " + g_lvl + "\n"
        update.message.reply_text(output_text)
    else:
        update.message.reply_text("Només els founders poden veure els ids de la gent de l'equip!")


def req_ids(update, context):
    bot_id = str(update.message.chat['id'])
    if check_is_founder(bot_id):
        m_ids = str(teams_data[teams_data['FOUNDER'] == bot_id]['REQUESTS'].values[0])
        m_ids = m_ids.split(", ")
        if m_ids[0] == 'None':
            update.message.reply_text("No hi ha peticions pendents!")
            return None
        output_text = "Els ids del teu equip són els següents:\n\n"
        for i in m_ids:
            output_text += "ID: " + str(i)
            alias = str(data[data['BOT_ID'] == str(i)]['ALIAS'].values[0])
            output_text += ". Alias: " + alias + "\n"
        update.message.reply_text(output_text)
    else:
        update.message.reply_text("Només els founders poden veure els ids de la gent de l'equip!")

def create_link(update, context):
    # link = update.create_chat_invite_link(update.message.chat['id'])
    print(telegram.ChatInviteLink(invite_link='https://t.me/joinchat/r7Cj1ej7vvg4NWE0', creator="Shaggy", is_primary=True, is_revoked=False))


def boop(update, context):
    bot_id = str(update.message.chat['id'])
    if bot_id not in registred_ids:
        new_register(bot_id, data)

    image_url = get_boop()
    image = requests.get(image_url)
    update.message.reply_photo(image.content)


def meow(update, context):
    bot_id = str(update.message.chat['id'])
    if bot_id not in registred_ids:
        new_register(bot_id, data)

    page = "https://cataas.com/cat"
    content = requests.get(page)
    if content.status_code == 200:
        update.message.reply_photo(content.content)


def ribbit(update, context):
    bot_id = str(update.message.chat['id'])
    if bot_id not in registred_ids:
        new_register(bot_id, data)

    random_num = randint(0, (len(list_of_frogs) - 1))
    page = list_of_frogs[random_num]
    content = requests.get(page)
    if content.status_code == 200:
        update.message.reply_photo(content.content)


def sendboop(update, context):
    bot_id = str(update.message.chat['id'])
    if bot_id not in registred_ids:
        new_register(bot_id, data)

    guild_name = str(data[data['BOT_ID'] == bot_id]['GUILD'].values[0])
    if guild_name == ' ':
        update.message.reply_text("No estàs a cap equip! Només pots enviar un boop si estàs a un equip!")
        return None

    alias = str(update.message.text)[10:]
    total_alias = data[data['GUILD'] == guild_name]['ALIAS'].tolist()
    own_alias = str(data[data['BOT_ID'] == bot_id]['ALIAS'].values[0])
    if alias in total_alias:
        receiver_id = str(data[(data['GUILD'] == guild_name) & (data['ALIAS'] == alias)]['BOT_ID'].values[0])
        output_text = own_alias + " sends a boop"
        context.bot.send_message(receiver_id, output_text)
        image_url = get_boop()
        context.bot.send_photo(receiver_id, image_url)
        update.message.reply_text("Has enviat un boop!")
    else:
        update.message.reply_text("No hi ha ningú amb aquest alias al teu equip!!")


def sendall(update, context):
    bot_id = str(update.message.chat['id'])
    if bot_id not in registred_ids:
        new_register(bot_id, data)

    guild_name = str(data[data['BOT_ID'] == bot_id]['GUILD'].values[0])
    if guild_name == ' ':
        update.message.reply_text("No estàs a cap equip! Només pots enviar un missatge si estàs a un equip!")
        return None

    message = str(update.message.text)[9:]
    total_alias = data[data['GUILD'] == guild_name]['ALIAS'].tolist()
    for alias in total_alias:
        receiver_id = str(data[(data['GUILD'] == guild_name) & (data['ALIAS'] == alias)]['BOT_ID'].values[0])
        context.bot.send_message(receiver_id, message)

    update.message.reply_text("Has enviat el teu missatge a tothom del teu equip!")


def sendallboop(update, context):
    bot_id = str(update.message.chat['id'])
    if bot_id not in registred_ids:
        new_register(bot_id, data)

    guild_name = str(data[data['BOT_ID'] == bot_id]['GUILD'].values[0])
    if guild_name == ' ':
        update.message.reply_text("No estàs a cap equip! Només pots enviar un missatge si estàs a un equip!")
        return None

    image_url = get_boop()
    own_alias = str(data[data['BOT_ID'] == bot_id]['ALIAS'].values[0])
    total_alias = data[data['GUILD'] == guild_name]['ALIAS'].tolist()
    for alias in total_alias:
        receiver_id = str(data[(data['GUILD'] == guild_name) & (data['ALIAS'] == alias)]['BOT_ID'].values[0])
        output_text = own_alias + " sends a boop"
        context.bot.send_message(receiver_id, output_text)
        context.bot.send_photo(receiver_id, image_url)

    update.message.reply_text("Has enviat un boop a tot el teu equip!")

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


def set_language(update, context):
    bot_id = str(update.message.chat['id'])
    if bot_id not in registred_ids:
        new_register(bot_id, data)

    new_language = select_language(str(update.message.text)[13:])
    actual_language = str(data[data['BOT_ID'] == bot_id]['LANGUAGE'].values[0])

    if new_language == actual_language:
        output_text = "Aquest ja és el teu idioma per les missions!"
        translated_text = translator.translate(text=output_text, dest=actual_language)
        update.message.reply_text(translated_text.text)
    else:
        data.loc[data['BOT_ID'] == bot_id, 'LANGUAGE'] = new_language
        data.to_csv(database_file, index=False, sep=';')
        output_text = "S'ha actualitzat el teu nou llenguatge per les missions!"
        translated_text = translator.translate(text=output_text, dest=new_language)
        update.message.reply_text(translated_text.text)


# Commands related to competition
def topfaction(update, context):
    bot_id = str(update.message.chat['id'])
    if bot_id not in registred_ids:
        new_register(bot_id, data)

    n = str(update.message.text)[12:]
    try:
        top = int(n)
    except ValueError:
        top = 10

    own_faction = str(data[data['BOT_ID'] == str(bot_id)]['FACTION'].values[0])
    if own_faction == 'Neutral':
        update.message.reply_text("Primer t'has d'unir a una facció! /joinanomalis o /joincorruptus")
        return None

    faction_df = data[(data['FACTION'] == own_faction) & ((data['Level'] == 'Player') | (data['BOT_ID'] == '1972795833' ) | (data['BOT_ID'] == '750747669'))]
    a_ids = faction_df['BOT_ID'].tolist()
    score = dict()
    for ai in a_ids:
        points = user_points(faction_df, ai)
        if points > 0:
            score[ai] = points
    score = dict(sorted(score.items(), key=lambda item: item[1], reverse=True))

    output_text = "Les millors puntuacions de la vostra facció són:\n"
    last_points = max(score.values())
    position = 1
    counter = 1

    for key, value in score.items():
        alias = str(faction_df[faction_df['BOT_ID'] == key]['ALIAS'].values[0])
        if alias == 'no_alias':
            continue
        if last_points != value:
            position += 1
            last_points = value
        output_text += str(position) + ". " + alias + ": " + str(value) + "\n"
        if counter == top:
            break
        counter += 1

    output_text += "\nRecordeu: només les persones amb alies surten al top! useu /setalias + \"alias\" per tenir-ne un"
    update.message.reply_text(output_text)


def top_teams(update, context):
    guilds = data['GUILD'].tolist()
    guilds = list(filter(lambda x: x != ' ', guilds))
    guilds = set(guilds)
    g_score = dict()

    n = str(update.message.text)[10:]
    try:
        top = int(n)
    except ValueError:
        top = 10

    for g in guilds:
        g_points = guild_points(g)
        if g_points > 0:
            g_score[g] = g_points

    g_score = dict(sorted(g_score.items(), key=lambda item: item[1], reverse=True))

    last_points = max(g_score.values())
    position = 1
    counter = 1
    output_text = "El top " + str(top) + " dels equips és:\n\n"
    for key, value in g_score.items():
        if last_points != value:
            position += 1
            last_points = value
        output_text += str(position) + ". " + str(key) + ": " + str(value) + "\n"
        if counter == top:
            break
        counter += 1

    update.message.reply_text(output_text)


def top3(update, context):
    all_ids = data['BOT_ID'].tolist()
    score = dict()
    for i in all_ids:
        points = user_points(data, i)
        if points > 0:
            score[i] = points

    score = dict(sorted(score.items(), key=lambda item: item[1], reverse=True))
    output_text = "El top 3 del joc tenen les següents puntuacions:\n\n"

    counter = 1
    for k, v in score.items():
        output_text += str(counter) + ": " + str(v) + "\n"
        if counter >= 3:
            break
        counter += 1

    output_text += "\nEnhorabona i seguiu així!!!!"

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


def help_basic(update, context):
    output_text = """💬 *BÁSICOS:*
- */start:* para recordar la información inicial.

- */rules:* para saber las normas del juego

- */help*: para volver a ver esta información.

- */use:* para obtener un tutorial de las misiones. 

- */getmyid:* para obtener tu ID, el número de identificación como jugador.

- */missions*: para saber dónde puedes encontrar misiones. 

- */contact*: si tienes dudas o problemas usa este comando para contactarnos!"""
    update.message.reply_text(output_text, parse_mode=telegram.ParseMode.MARKDOWN)


def help_competitive(update, context):
    output_text = """💬 *COMPETITIVOS:*
- */top3*: muestar la puntuación de los 3 jugadores con mayor puntuación

- */topfaction*: muestra el top de vuestra facción. Para entrar en el top requiere alias y más de 0 puntos

- */topteams*: mustra el top 10 de los equipos registrados."""
    update.message.reply_text(output_text, parse_mode=telegram.ParseMode.MARKDOWN)


def help_personal(update, context):
    output_text ="""💬 *PERSONALIZADOS:*
- */setalias + "el nombre de tu elección"*: para cambiar tu alias de registro. _Ejemplo: /setalias TimeEscapeBot_.

- */stats*: para conocer tus logros dentro del juego.

- */activity*: para saber las misiones activas que te quedan por resolver.

- */hint + "id de la misión"*: para obtener una pista de la misión. _Ejemplo: /hint C1_

- */join + "facción"*: para unirte a tu facción. _Ejemplos: /joinanomalis o /joincorruptus_ 

- */boop o /meow o /ribbit*: El bot te mandará un boop! o un meow! o un ribbit!"""
    update.message.reply_text(output_text, parse_mode=telegram.ParseMode.MARKDOWN)


def help_team(update, context):
    output_text = """💬 *DE EQUIPO:* Los equipos sirven para jugar con tus amigos y acumular puntos.

- */createteam + "nombre"*: para ser la fundadora de un equipo. _Ejemplo: /createteam HvZ_

- */jointeam + "nombre"*: para unirte a un equipo que ya exista. _Ejemplo: /jointeam HvZ_

- */showteam*: para obtener el ranking de tu equipo.

- */sendboop + "alias"*: mandar un boop a alguien con ese alias que esté en tu equipo. Boop!

- */sendall + "mensaje"*: mandar un mensaje a todo el mundo de tu equipo

- */help_founder*: Comandos que solo los fundadores pueden usar"""
    update.message.reply_text(output_text, parse_mode=telegram.ParseMode.MARKDOWN)


def help_founder(update, context):
    bot_id = str(update.message.chat['id'])
    if check_is_founder(bot_id):
        output_text = """💬 *DE FUNDADORAS DE EQUIPO:*
        
- */promote + "alias", "rango"*: para otorgar cargos dentro del equipo. _Ejemplo: /promote antonio, veterano_.

-*/kick + user_id*: Elimina la persona con ese id de tu equipo

-*/admit + user_id*: Admite a la persona con ese id a tu equipo

-*/decline + user_id*: Rechaza a la persona con ese id de tu equipo

-*/memberids*: Lista IDs, alias i rangos de todas las personas miembro

-*/requestsids*: Lista IDs i alias de todas las personas que estan pendientes de aprobación para entrar"""
        update.message.reply_text(output_text, parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        update.message.reply_text("No has fundat cap equip, no pots usar aquesta comanda!")


def help(update, context):
    """Send a message when the command /help is issued."""
    output_text = """Para ver los comandos basicos pulsa en:
💬 *BÁSICOS: /help_basic*

💬 *COMPETITIVOS: /help_competitive*

💬 *PERSONALIZADOS: /help_personal*

💬 *DE EQUIPO: /help_team*

⚠️ *REPORTAR UN PROBLEMA:* /report + El problema"""
    update.message.reply_text(output_text, parse_mode=telegram.ParseMode.MARKDOWN)

# - */help + "otro comando"*: para obtener información más detallada referente al comando. _Ejemplo: /help createteam_. (aun en desarrollo)


def use(update, context):
    output_text = """HOLA JUGADOR!!👋🏼
👀Leeme atentamente para saber cómo jugar a TIME ESCAPE y ganar puntos para tu facción.

*1. Encuentra un QR*
Ve por el campus y busca por todas partes hasta que veas un codigo QR.

*2. Hazle una foto*
Haz una foto del QR y mándamela por aquí. Puedes sacar la foto directamente desde este chat.

*3. Recibe la misión*
Después de asegurarme de que tu foto sea original, leeré el QR y te mandaré tu misión. 
⚠️ ¡Paciencia! Sóis muchos jugando y puede que me bloquee un poco. 
_Si en el momento no puedes realizar la misión, simpre podrás volver a ella usando el comando /activity_.

*4. Resuelve la misión*
Responde a la misión por este chat. Si tu respuesta es correcta, ganarás puntos para tu facción💪🏿

*5. Vuelta a empezar*
Repite este proceso con todos los QRs que encuentres para acumular puntos y cambiar la historia."""
    update.message.reply_text(output_text, parse_mode=telegram.ParseMode.MARKDOWN)


def rules(update, context):
    output_text = """*NORMAS:*
_Con tal de garantizar que TIME ESCAPE sea un juego divertido para todes, deberéis seguir la siguiente normativa_.

😷 En TIME ESCAPE respetaremos las medidas vigentes del Procicat y sus medidas para protegernos de la Covid-19.

❌ *No arranques QRs*: arrancar un QR será penalizado con la inmediata expulsión del juego.

❌ *No hagas spoilers*: revelar la ubicación de un QR o la solución de una misión por el grupo será penalizado con la expulsión del jugador en dicho grupo. _Esta norma no se aplica si se trata de tu equipo_.

❌ *No compartas el QR*: si una misma imagen se sube 2 veces, nuestro Bot todo poderoso lo sabrá y dicha imagen quedará inutilizada.

💕 *Treat people with kindness*: los demás jugadores (corruptus o anomalis), los moderadores (los de la bandana roja en la pierna) y las personas no jugadoras del campus merecen ser tratadas con respeto. El mobiliario y las instalaciones de la UAB también.

💕 *Stay safe*: todas las misiones se encuentran en sitios accesibles. No hagais burradas.

🛡️ *Escudos*: en TIME ESCAPE los escudos estan permitidos.


Y, para terminar...
✨ *NO SEAIS IDIOTES* ✨"""
    update.message.reply_text(output_text, parse_mode=telegram.ParseMode.MARKDOWN)


def contact(update, context):
    output_text = """Contacta con el Mod correspondiente según tu problema:
    
- *Problemas o dudas con el bot:* @ShaggyGalaso
- *Problemas con los QR:* @Nelaso
- *Problemas con la misión:* @Janadsb99
- *Problemas fuera del campus:* @AlexNevado
- *Dudas de normas:* @Sargento\_Zorro
- *Dudas de telegram:* @GuillemMoya
- *Problemas con otros jugadores:* @mar\_clua
- *Problemas por discriminación:* @AiHysteric"""
    update.message.reply_text(output_text, parse_mode=telegram.ParseMode.MARKDOWN)


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
    if user_id < 0:
        return None

    if user_id in registred_ids:
        new_register(user_id, data)
    mission_solved = check_answer(user_id, answer)
    faction = str(data[data['BOT_ID'] == str(user_id)]['FACTION'].values[0])
    if faction == "Neutral":
        update.message.reply_text("Abans de fer missions t'has d'unir a una facció, escull una de les dues:\n/joinanomalis \n/joincorruptus")
    elif mission_solved:
        to_send = "Enhorabona!! Has respost correctament la missio " + mission_solved + ". Continua així!"
        update.message.reply_text(to_send)
        final_text = mission_accomplished(str(user_id), mission_solved)
        update.message.reply_text(final_text)
    elif answer in talk.keys():
        update.message.reply_text(talk[answer])
    else:
        update.message.reply_text("El missatge que has enviat no és cap resposta de les teves missions actives!")
        update.message.reply_text("Escriu /help per saber més de com funciona el bot")


def get_my_id(update, context):
    update.message.reply_text(update.message.chat['id'])


def test(update, context):
    """Send link to the aliniation test"""
    update.message.reply_text('https://bit.ly/3urA0S0')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    # update.message.reply_text("Alguna cosa ha anat malament! Torna-ho a intentar o contacte amb @ShaggyGalaso")


# Mod commands
def bdb(update, context):
    image_url = get_boop()

    user_id = update.message.chat['id']
    if user_id < 0:
        return None

    if str(user_id) != '981802604':
        update.message.reply_text("Només el meu pare pot fer servir aquesta comanda")

    all_ids = data['BOT_ID'].tolist()
    for i in all_ids:
        try:
            context.bot.send_message(str(i), "Que tinguis un bon dia")
            context.bot.send_photo(str(i), image_url)
            context.bot.send_message(str(i), "boop! /boop per més")
        except:
            pass


def activate_mission(update, context):
    user_id = str(update.message.chat['id'])

    level = str(data[data['BOT_ID'] == user_id]['Level'].values[0])
    if level != 'Mod':
        update.message.reply_text("Només els mods poden fer servir aquesta comanda!!")
        return None

    text = str(update.message.text)[10:]
    values = text.split(", ")
    if len(values) != 2:
        update.message.reply_text("Cal entrar el user_id i el mission id separats per una coma i un espai")
        return None

    am_building = str(mission_data[mission_data['MISSION_ID'] == values[1]]['AM_BUILDING'].values[0])
    data.loc[data['BOT_ID'] == values[0], am_building] = values[1]
    data.to_csv(database_file, index=False, sep=';')
    update.message.reply_text("Missió actualitzada correctament")


def general_top(update, context):
    user_id = str(update.message.chat['id'])

    level = str(data[data['BOT_ID'] == user_id]['Level'].values[0])
    if level != 'Mod':
        update.message.reply_text("Només els mods poden fer servir aquesta comanda!!")
        return None

    update.message.reply_text("No me pienso esforzar en esto (:\n")
    n = str(update.message.text)[12:]
    try:
        top = int(n)
    except ValueError:
        top = 10

    anomalis_df = data[(data['FACTION'] == 'Anomalis') & ((data['Level'] == 'Player') | (data['BOT_ID'] == '1972795833') | (data['BOT_ID'] == '750747669'))]
    corruptus_df = data[(data['FACTION'] == 'Corruptus') & ((data['Level'] == 'Player') | (data['BOT_ID'] == '1972795833') | (data['BOT_ID'] == '750747669'))]
    a_ids = anomalis_df['BOT_ID'].tolist()
    score = dict()
    for ai in a_ids:
        points = user_points(anomalis_df, ai)
        if points > 0:
            score[ai] = points
    score = dict(sorted(score.items(), key=lambda item: item[1], reverse=True))

    output_text = "Les millors puntuacions d'anomalis són:\n"
    last_points = max(score.values())
    position = 1
    counter = 1

    for key, value in score.items():
        alias = str(anomalis_df[anomalis_df['BOT_ID'] == key]['ALIAS'].values[0])
        if alias == 'no_alias':
            continue
        if last_points != value:
            position += 1
            last_points = value
        output_text += str(position) + ". " + alias + ": " + str(value) + "\n"
        if counter == top:
            break
        counter += 1

    update.message.reply_text(output_text)

    a_ids = corruptus_df['BOT_ID'].tolist()
    score = dict()
    for ai in a_ids:
        points = user_points(corruptus_df, ai)
        if points > 0:
            score[ai] = points
    score = dict(sorted(score.items(), key=lambda item: item[1], reverse=True))

    output_text = "Les millors puntuacions de corruptus són:\n"
    last_points = max(score.values())
    position = 1
    counter = 1

    for key, value in score.items():
        alias = str(corruptus_df[corruptus_df['BOT_ID'] == key]['ALIAS'].values[0])
        if alias == 'no_alias':
            continue
        if last_points != value:
            position += 1
            last_points = value
        output_text += str(position) + ". " + alias + ": " + str(value) + "\n"
        if counter == top:
            break
        counter += 1

    update.message.reply_text(output_text)


def add_points(update, context):
    user_id = str(update.message.chat['id'])

    level = str(data[data['BOT_ID'] == user_id]['Level'].values[0])
    if level != 'Mod':
        update.message.reply_text("Només els mods poden fer servir aquesta comanda!!")
        return None

    text = str(update.message.text)[11:]
    values = text.split(", ")
    if len(values) != 2:
        update.message.reply_text("Cal entrar el user_id i els punts per separats per una coma i un espai")
        return None

    try:
        values[1] = int(values[1])
    except:
        update.message.reply_text("***ERROR***:El segon valor ha de ser un número enter")
        return None

    am_b = 'P_Aulari'
    actual_points = int(data[data['BOT_ID'] == values[0]][am_b])
    data.loc[data['BOT_ID'] == values[0], am_b] = actual_points + values[1]
    data.to_csv(database_file, index=False, sep=';')
    update.message.reply_text("Punts sumats correctament!!")


def message_all(update, context):
    user_id = str(update.message.chat['id'])

    level = str(data[data['BOT_ID'] == user_id]['Level'].values[0])
    if level != 'Mod':
        update.message.reply_text("Només els mods poden fer servir aquesta comanda!!")
        return None

    text = str(update.message.text)[12:]

    all_ids = data['BOT_ID'].tolist()
    for i in all_ids:
        try:
            context.bot.send_message(str(i), text)
        except:
            pass


def allmissionstats(update, context):
    ret = dict()
    ret = dict_missions_in_zone('DM_Aulari', ret)
    ret = dict_missions_in_zone('DM_Carpa', ret)
    ret = dict_missions_in_zone('DM_Civica', ret)
    ret = dict_missions_in_zone('DM_Comunicacio', ret)
    ret = dict_missions_in_zone('DM_EB_Sud', ret)
    ret = dict_missions_in_zone('DM_EB_Nord', ret)
    ret = dict_missions_in_zone('DM_EB_Central', ret)
    ret = dict_missions_in_zone('DM_ETSE', ret)
    ret = dict_missions_in_zone('DM_FTI', ret)
    ret = dict_missions_in_zone('DM_Med', ret)
    ret = dict_missions_in_zone('DM_SAF', ret)
    ret = dict_missions_in_zone('DM_EC', ret)
    ret = dict_missions_in_zone('DM_Torres', ret)
    ret = dict_missions_in_zone('DM_Vet', ret)

    output_text = "Active players: " + str(active_players(data) - 2)
    update.message.reply_text(output_text)
    update.message.reply_text(humanize_mission_dict(ret), parse_mode=telegram.ParseMode.MARKDOWN)


def allanomalismissions(update, context):
    ret = dict()
    ret = anomalis_missions_in_zone('DM_Aulari', ret)
    ret = anomalis_missions_in_zone('DM_Carpa', ret)
    ret = anomalis_missions_in_zone('DM_Civica', ret)
    ret = anomalis_missions_in_zone('DM_Comunicacio', ret)
    ret = anomalis_missions_in_zone('DM_EB_Sud', ret)
    ret = anomalis_missions_in_zone('DM_EB_Nord', ret)
    ret = anomalis_missions_in_zone('DM_EB_Central', ret)
    ret = anomalis_missions_in_zone('DM_ETSE', ret)
    ret = anomalis_missions_in_zone('DM_FTI', ret)
    ret = anomalis_missions_in_zone('DM_Med', ret)
    ret = anomalis_missions_in_zone('DM_SAF', ret)
    ret = anomalis_missions_in_zone('DM_EC', ret)
    ret = anomalis_missions_in_zone('DM_Torres', ret)
    ret = anomalis_missions_in_zone('DM_Vet', ret)

    output_text = "Active players: " + str(active_players(data[data['FACTION'] == 'Anomalis']))
    update.message.reply_text(output_text)
    update.message.reply_text(humanize_mission_dict(ret), parse_mode=telegram.ParseMode.MARKDOWN)


def allcorruptusmissions(update, context):
    ret = dict()
    ret = corruptus_missions_in_zone('DM_Aulari', ret)
    ret = corruptus_missions_in_zone('DM_Carpa', ret)
    ret = corruptus_missions_in_zone('DM_Civica', ret)
    ret = corruptus_missions_in_zone('DM_Comunicacio', ret)
    ret = corruptus_missions_in_zone('DM_EB_Sud', ret)
    ret = corruptus_missions_in_zone('DM_EB_Nord', ret)
    ret = corruptus_missions_in_zone('DM_EB_Central', ret)
    ret = corruptus_missions_in_zone('DM_ETSE', ret)
    ret = corruptus_missions_in_zone('DM_FTI', ret)
    ret = corruptus_missions_in_zone('DM_Med', ret)
    ret = corruptus_missions_in_zone('DM_SAF', ret)
    ret = corruptus_missions_in_zone('DM_EC', ret)
    ret = corruptus_missions_in_zone('DM_Torres', ret)
    ret = corruptus_missions_in_zone('DM_Vet', ret)

    output_text = "Active players: " + str(active_players(data[data['FACTION'] == 'Corruptus']))
    update.message.reply_text(output_text)
    update.message.reply_text(humanize_mission_dict(ret), parse_mode=telegram.ParseMode.MARKDOWN)


def donebyuser(update, context):
    user_id = str(update.message.chat['id'])
    level = str(data[data['BOT_ID'] == user_id]['Level'].values[0])

    if level != 'Mod':
        update.message.reply_text("Només els mods poden fer servir aquesta comanda!!")
        return None

    player_id = str(update.message.text)[12:]
    udf = data[data['BOT_ID'] == player_id]
    dm = all_done_missions(udf, player_id)
    alias = str(udf['ALIAS'].values[0])
    output_text = "La persona: " + str(alias) + " amb ID: " + str(player_id) + " ha fet les següents missions:\n\n"
    output_text += str(dm)

    update.message.reply_text(output_text)


def onduty(update, context):
    user_id = str(update.message.chat['id'])
    level = str(data[data['BOT_ID'] == user_id]['Level'].values[0])

    if level != 'Mod':
        update.message.reply_text("Només els mods poden fer servir aquesta comanda!!")
        return None

    player_id = str(update.message.text)[8:]
    udf = data[data['BOT_ID'] == player_id]
    dm = all_active_missions(udf, player_id)
    alias = str(udf['ALIAS'].values[0])
    output_text = "La persona: " + str(alias) + " amb ID: " + str(player_id) + " té les següents missions actives:\n\n"
    output_text += str(dm)

    update.message.reply_text(output_text)


def complete(update, context):
    user_id = str(update.message.chat['id'])
    level = str(data[data['BOT_ID'] == user_id]['Level'].values[0])

    if level != 'Mod':
        update.message.reply_text("Només els mods poden fer servir aquesta comanda!!")
        return None
    text = str(update.message.text)[10:]
    values = text.split(", ")
    am = all_active_missions(data, values[0])
    if values[1] in am:
        mission_accomplished(values[0], values[1])
        update.message.reply_text("Missió completada amb éxit")
    else:
        update.message.reply_text("Aquesta persona no té aquesta missió activada")


def sendtoplayer(update, context):
    user_id = str(update.message.chat['id'])
    level = str(data[data['BOT_ID'] == user_id]['Level'].values[0])

    if level != 'Mod':
        update.message.reply_text("Només els mods poden fer servir aquesta comanda!!")
        return None
    text = str(update.message.text)[14:]
    values = text.split(", ")
    alias = str(data[data['BOT_ID'] == user_id]['ALIAS'].values[0])
    if text:
        output_text = "Li Mod " + alias + " diu el següent:\n\n"
        output_text += values[1]
        context.bot.send_message(values[0], output_text)

    update.message.reply_text("Persona contactada correctament")


def influence_stats(update, context):
    user_id = str(update.message.chat['id'])
    level = str(data[data['BOT_ID'] == user_id]['Level'].values[0])

    if level != 'Mod':
        update.message.reply_text("Només els mods poden fer servir aquesta comanda!!")
        return None
    
    all_ids = data['BOT_ID'].tolist()
    id_faction = dict()
    id_missions = dict()
    faction_values = {'Anomalis': 1, 'Corruptus': -1}
    for i in all_ids:
        value = all_done_missions(data, i)
        if len(value) != 0:
            key = str(data[data['BOT_ID'] == i]['FACTION'].values[0])
            if key == "Neutral":
                continue
            id_faction[i] = key
            id_missions[i] = value

    all_mission_id = mission_data['MISSION_ID'].tolist()

    mission_npc = dict()
    for mid in all_mission_id:
        if str(mid) == 'nan':
            continue
        npc = str(mission_data[mission_data['MISSION_ID'] == mid]['NPC'].values[0])
        if npc == 'nan' or npc == 'None':
            continue
        mission_npc[mid] = npc

    npc_influence = dict()
    for n in mission_npc.values():
        npc_influence[n] = 0

    for i in id_missions.keys():
        inf_value = faction_values[id_faction[i]]
        missions = id_missions[i]
        for m in missions:
            if m in mission_npc.keys():
                npc = mission_npc[m]
                actual_value = npc_influence[npc]
                actual_value += inf_value
                npc_influence[npc] = actual_value

    output_text = "Així està l'actual estat d'influencia: \n(Positiu Anomalis, Negatiu Corruptus)\n\n"
    for k, v in npc_influence.items():
        output_text += str(k) + ": " + str(v) + "\n"

    update.message.reply_text(output_text)


def help_mod(update, context):
    user_id = str(update.message.chat['id'])

    level = str(data[data['BOT_ID'] == user_id]['Level'].values[0])
    if level != 'Mod':
        update.message.reply_text("Només els mods poden fer servir aquesta comanda!!")
        return None

    output_text = """💬 *COMANDOS DE SOLO MODS:*
-*/generaltop*: Muestra el top 10 de las dos facciones. Se puede añadir un numero para que sea el top ese numero

-*/activate + user_id, mission_id*: Le activa a ese usuario esa mission

-*/complete + user_id, mission_id*: Le hace esa mision a esa persona

-*/donebyuser + user_id*: Te dice todas las misiones que ha hecho esa persona 

-*/onduty + user_id*: Te dice todas las misiones activas de esa persona
 
-*/addpoints + user_id, puntos*: Le suma a ese usuario tantos puntos

-*/sendtoplayer + user_id, texto*: Manda el texto a ese usuario

-*/messageall + texto*: Le manda a todos los jugadores ese texto

-*/allmissionstats*: Muestra los stats de todas las misiones

-*/allanomalisstats*: Muestra los stats de todas las misiones

-*/allcorruptusstats*: Muestra los stats de todas las misiones

-*/influencestats*: Muestra el estado de influencia de todos los NPCS"""
    update.message.reply_text(output_text, parse_mode=telegram.ParseMode.MARKDOWN)


def reportproblem(update, context):
    bot_id = str(update.message.chat['id'])
    if bot_id not in registred_ids:
        new_register(bot_id, data)

    alias = str(data[data['BOT_ID'] == bot_id]['ALIAS'].values[0])
    problem = str(update.message.text)[8:]
    if problem:
        output_text = "La persona amb alies: " + alias + " i id: " + bot_id + " reporta el seqüent problema:\n\n"
        output_text += problem
        context.bot.send_message('981802604', output_text)
        context.bot.send_message('981802604', str(bot_id))

    update.message.reply_text("Problema correctamente reportado a @ShaggyGalaso, hablale si tarda mucho en resolverse")


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

    # Command to report a problem
    dp.add_handler(CommandHandler("report", reportproblem))

    # Commands related to competition
    dp.add_handler(CommandHandler("topfaction", topfaction))
    dp.add_handler(CommandHandler("top3", top3))
    dp.add_handler(CommandHandler("topteams", top_teams))

    # Commands related to teams
    dp.add_handler(CommandHandler("createteam", create_team))
    dp.add_handler(CommandHandler("jointeam", join_team))
    dp.add_handler(CommandHandler("showteam", show_team))
    dp.add_handler(CommandHandler("createlink", create_link))
    dp.add_handler(CommandHandler("sendboop", sendboop))
    dp.add_handler(CommandHandler("sendall", sendall))
    dp.add_handler(CommandHandler("sendallboop", sendallboop))

    # Commands for team founders
    dp.add_handler(CommandHandler("promote", promote))
    dp.add_handler(CommandHandler("kick", kick))
    dp.add_handler(CommandHandler("admit", admit))
    dp.add_handler(CommandHandler("decline", decline))
    dp.add_handler(CommandHandler("memberids", mem_ids))
    dp.add_handler(CommandHandler("requestsids", req_ids))

    # Commands related to personal stuff
    dp.add_handler(CommandHandler("setalias", set_alias))
    dp.add_handler(CommandHandler("stats", show_me))
    dp.add_handler(CommandHandler("activity", activity))
    dp.add_handler(CommandHandler("hint", hint))
    dp.add_handler(CommandHandler("joinanomalis", join_anomalis))
    dp.add_handler(CommandHandler("joincorruptus", join_corruptus))
    dp.add_handler(CommandHandler("setlanguage", set_language))
    dp.add_handler(CommandHandler("boop", boop))
    dp.add_handler(CommandHandler("meow", meow))
    dp.add_handler(CommandHandler("ribbit", ribbit))

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("rules", rules))
    dp.add_handler(CommandHandler("halal", halal))
    dp.add_handler(CommandHandler("corruptus", corruptus))
    dp.add_handler(CommandHandler("test", test))
    dp.add_handler(CommandHandler("use", use))
    dp.add_handler(CommandHandler("contact", contact))

    # Commands for help
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("help_personal", help_personal))
    dp.add_handler(CommandHandler("help_team", help_team))
    dp.add_handler(CommandHandler("help_competitive", help_competitive))
    dp.add_handler(CommandHandler("help_basic", help_basic))
    dp.add_handler(CommandHandler("help_founder", help_founder))

    # Mod Commands
    dp.add_handler(CommandHandler("bondiaboop", bdb))
    dp.add_handler(CommandHandler("activate", activate_mission))
    dp.add_handler(CommandHandler("generaltop", general_top))
    dp.add_handler(CommandHandler("addpoints", add_points))
    dp.add_handler(CommandHandler("messageall", message_all))
    dp.add_handler(CommandHandler("allmissionstats", allmissionstats))
    dp.add_handler(CommandHandler("allanomalisstats", allanomalismissions))
    dp.add_handler(CommandHandler("allcorruptusstats", allcorruptusmissions))
    dp.add_handler(CommandHandler("donebyuser", donebyuser))
    dp.add_handler(CommandHandler("onduty", onduty))
    dp.add_handler(CommandHandler("complete", complete))
    dp.add_handler(CommandHandler("sendtoplayer", sendtoplayer))
    dp.add_handler(CommandHandler("influencestats", influence_stats))
    dp.add_handler(CommandHandler("helpmods", help_mod))

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