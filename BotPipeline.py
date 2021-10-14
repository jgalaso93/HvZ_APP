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

from googletrans import Translator

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from databases.db_paths import teams_db_file, player_db_file, \
    npc_db_file, conversation_db_file, missions_db_file

from utils.user_values import all_done_missions, all_active_missions, user_points, amount_of_missions_done

from utils.animals import boop, meow, ribbit, get_boop

from utils.missions import dict_missions_in_zone, anomalis_missions_in_zone,\
    corruptus_missions_in_zone, humanize_mission_dict, active_players, lore_text, \
    mission_accomplished_ext, check_answer_ext, read_qr_ext, missions

from utils.guild import guild_points, show_team_ext, mem_ids_ext, req_ids_ext, \
    create_team_ext, join_team_ext, promote_ext, kick_ext, admit_ext, decline_ext, \
    sendboop_ext, sendall_ext, sendallboop_ext

from utils.pic_sender import Civica, Veterinaria, Aulari, Carpa, Comunicacio, Edifici_B_central, Edifici_B_Nord, \
    Edifici_B_Sud, Edifici_C, Educacio, Etse, FTI, Medicina, SAF, Torres

from utils.bot_help import contact, help_basic, help_mod_ext, help_team, help, help_personal, \
    help_competitive, help_founder_ext, start_ext, rules, use

from utils.helpers import select_language, create_new_row


#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#----------------------DATABASE VARIABLES-----------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
# database_file = os.path.join(sys.path[0], 'database.csv')
try:
    data = pd.read_csv(player_db_file, sep=';', header=0, dtype={'BOT_ID': str}, encoding='cp1252')
except:
    data = pd.read_csv(player_db_file, sep=',', header=0, dtype={'BOT_ID': str}, encoding='cp1252')

registred_ids = data['BOT_ID'].tolist()

# mission_database_file = os.path.join(sys.path[0], 'mission_database.csv')
mission_data = pd.read_csv(missions_db_file, sep=';', header=0,
                           dtype={'MISSION': str, 'RESULT_POOL': str},
                           encoding='cp1252')
mission_ids = mission_data['MISSION_ID'].tolist()

# NPC_file = os.path.join(sys.path[0], 'NPC_database.csv')
NPC_data = pd.read_csv(npc_db_file, sep=';', header=0, encoding='cp1252')

translator = Translator(service_urls=[
      'translate.google.com',
      'translate.google.co.kr',
    ])


# conver_file = os.path.join(sys.path[0], 'conversation_database.csv')
conver_data = pd.read_csv(conversation_db_file, sep=';', header=0, dtype={'BOT_ID': str}, encoding='cp1252')
talk_input = conver_data['INPUT'].tolist()
talk_output = conver_data['OUTPUT'].tolist()
talk = {k: v for k, v in zip(talk_input, talk_output)}

# teams_file = os.path.join(sys.path[0], 'teams_database.csv')
teams_data = pd.read_csv(teams_db_file, sep=';', header=0, encoding='cp1252', dtype={'FOUNDER': str})


#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#----------------------MISSIONS STRUCTURE-----------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

def mission_accomplished(user_id, mission_id):
    global data
    data = mission_accomplished_ext(user_id, mission_id, mission_data, data, NPC_data)
    data.to_csv(player_db_file, index=False, sep=';', encoding='cp1252')

    final_text = str(mission_data[mission_data['MISSION_ID'] == mission_id]['FINAL_TEXT'].values[0])
    if final_text != 'None':
        return final_text
    else:
        return None


def read_QR(update, context):
    global data
    bot_id = str(update.message.chat['id'])
    if check_pic(bot_id, update.message.photo[-1].file_unique_id):
        update.message.reply_text("Aquesta foto ja s'ha fet servir!!")
        return 0
    data = read_qr_ext(update, context, bot_id, mission_ids, data, mission_data)


def check_answer(user_id, answer):
    return check_answer_ext(user_id, answer, data, mission_data)

#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#----------------------ANTICHEAT CODE---------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------


def check_pic(user_id, photo_id):
    # return False

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
        db_pics.to_csv(df_pics, index=False, sep=';', encoding='cp1252')
        return False


#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#----------------------GUILD FUNCTIONS--------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

def mem_ids(update, context):
    mem_ids_ext(update, data, teams_data)


def show_team(update, context):
    show_team_ext(update, context, data)


def req_ids(update, context):
    req_ids_ext(update, data, teams_data)


def create_team(update, context):
    global data
    global teams_data
    data, teams_data = create_team_ext(update, context, data, teams_data)


def join_team(update, context):
    global teams_data
    teams_data = join_team_ext(update, context, data, teams_data)


def promote(update, context):
    global data
    data = promote_ext(update, context, data, teams_data)


def kick(update, context):
    global data
    data = kick_ext(update, context, data, teams_data)


def admit(update, context):
    global data
    global teams_data
    data, teams_data = admit_ext(update, context, data, teams_data)


def decline(update, context):
    global data
    global teams_data
    data, teams_data = decline_ext(update, context, data, teams_data)


def sendboop(update, context):
    sendboop_ext(update, context, data)


def sendall(update, context):
    sendall_ext(update, context, data)


def sendallboop(update, context):
    sendallboop_ext(update, context, data)


#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#----------------------DATABASE FUNCTIONS-----------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------


def new_register(bot_id, df):
    global data
    new_row = create_new_row(bot_id, data)
    # Save the new data to database
    data = data.append(new_row, ignore_index=True)
    data.to_csv(player_db_file, index=False, sep=';', encoding='cp1252')

    # Update the registred id's
    global registred_ids
    registred_ids = data['BOT_ID'].tolist()


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
        data.to_csv(player_db_file, index=False, sep=';', encoding='cp1252')

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
    output_text = "Missions actives actuals, codi i enunciat\n"
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
        data.to_csv(player_db_file, index=False, sep=';', encoding='cp1252')
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
        data.to_csv(player_db_file, index=False, sep=';', encoding='cp1252')
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
        data.to_csv(player_db_file, index=False, sep=';', encoding='cp1252')
        output_text = "S'ha actualitzat el teu nou llenguatge per les missions!"
        translated_text = translator.translate(text=output_text, dest=new_language)
        update.message.reply_text(translated_text.text)


#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#----------------------COMPETITIVE FUNCTIONS--------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

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
        g_points = guild_points(g, data)
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


def start(update, context):
    bot_id = str(update.message.chat['id'])
    if bot_id not in registred_ids:
        new_register(bot_id, data)
    start_ext(update, context)


def register(update, context):
    bot_id = update.message.chat['id']
    if str(bot_id) in registred_ids:
        update.message.reply_text('Tu registro ya está completado')
    else:
        new_register(bot_id, data)
        update.message.reply_text('Te has registrado!')


def help_founder(update, context):
    help_founder_ext(update, context, teams_data)


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


#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#----------------------MODS FUNCTIONS---------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

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
    data.to_csv(player_db_file, index=False, sep=';', encoding='cp1252')
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
    data.to_csv(player_db_file, index=False, sep=';', encoding='cp1252')
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
    ret = dict_missions_in_zone(data, 'DM_Aulari', ret)
    ret = dict_missions_in_zone(data, 'DM_Carpa', ret)
    ret = dict_missions_in_zone(data, 'DM_Civica', ret)
    ret = dict_missions_in_zone(data, 'DM_Comunicacio', ret)
    ret = dict_missions_in_zone(data, 'DM_EB_Sud', ret)
    ret = dict_missions_in_zone(data, 'DM_EB_Nord', ret)
    ret = dict_missions_in_zone(data, 'DM_EB_Central', ret)
    ret = dict_missions_in_zone(data, 'DM_ETSE', ret)
    ret = dict_missions_in_zone(data, 'DM_FTI', ret)
    ret = dict_missions_in_zone(data, 'DM_Med', ret)
    ret = dict_missions_in_zone(data, 'DM_SAF', ret)
    ret = dict_missions_in_zone(data, 'DM_EC', ret)
    ret = dict_missions_in_zone(data, 'DM_Torres', ret)
    ret = dict_missions_in_zone(data, 'DM_Vet', ret)

    output_text = "Active players: " + str(active_players(data) - 2)
    update.message.reply_text(output_text)
    update.message.reply_text(humanize_mission_dict(ret, mission_data), parse_mode=telegram.ParseMode.MARKDOWN)


def allanomalismissions(update, context):
    ret = dict()
    ret = anomalis_missions_in_zone(data, 'DM_Aulari', ret)
    ret = anomalis_missions_in_zone(data, 'DM_Carpa', ret)
    ret = anomalis_missions_in_zone(data, 'DM_Civica', ret)
    ret = anomalis_missions_in_zone(data, 'DM_Comunicacio', ret)
    ret = anomalis_missions_in_zone(data, 'DM_EB_Sud', ret)
    ret = anomalis_missions_in_zone(data, 'DM_EB_Nord', ret)
    ret = anomalis_missions_in_zone(data, 'DM_EB_Central', ret)
    ret = anomalis_missions_in_zone(data, 'DM_ETSE', ret)
    ret = anomalis_missions_in_zone(data, 'DM_FTI', ret)
    ret = anomalis_missions_in_zone(data, 'DM_Med', ret)
    ret = anomalis_missions_in_zone(data, 'DM_SAF', ret)
    ret = anomalis_missions_in_zone(data, 'DM_EC', ret)
    ret = anomalis_missions_in_zone(data, 'DM_Torres', ret)
    ret = anomalis_missions_in_zone(data, 'DM_Vet', ret)

    output_text = "Active players: " + str(active_players(data[data['FACTION'] == 'Anomalis']))
    update.message.reply_text(output_text)
    update.message.reply_text(humanize_mission_dict(ret, mission_data), parse_mode=telegram.ParseMode.MARKDOWN)


def allcorruptusmissions(update, context):
    ret = dict()
    ret = corruptus_missions_in_zone(data, 'DM_Aulari', ret)
    ret = corruptus_missions_in_zone(data, 'DM_Carpa', ret)
    ret = corruptus_missions_in_zone(data, 'DM_Civica', ret)
    ret = corruptus_missions_in_zone(data, 'DM_Comunicacio', ret)
    ret = corruptus_missions_in_zone(data, 'DM_EB_Sud', ret)
    ret = corruptus_missions_in_zone(data, 'DM_EB_Nord', ret)
    ret = corruptus_missions_in_zone(data, 'DM_EB_Central', ret)
    ret = corruptus_missions_in_zone(data, 'DM_ETSE', ret)
    ret = corruptus_missions_in_zone(data, 'DM_FTI', ret)
    ret = corruptus_missions_in_zone(data, 'DM_Med', ret)
    ret = corruptus_missions_in_zone(data, 'DM_SAF', ret)
    ret = corruptus_missions_in_zone(data, 'DM_EC', ret)
    ret = corruptus_missions_in_zone(data, 'DM_Torres', ret)
    ret = corruptus_missions_in_zone(data, 'DM_Vet', ret)

    output_text = "Active players: " + str(active_players(data[data['FACTION'] == 'Corruptus']))
    update.message.reply_text(output_text)
    update.message.reply_text(humanize_mission_dict(ret, mission_data), parse_mode=telegram.ParseMode.MARKDOWN)


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


def refresh_influences(update, context):
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

    for npc, influence in npc_influence.items():
        NPC_data.loc[NPC_data['NAME'] == npc, 'FAVOR'] = influence

    NPC_data.to_csv(npc_db_file, index=False, sep=';', encoding='cp1252')
    update.message.reply_text("Influencia refrescada correctament!")


def help_mod(update, context):
    help_mod_ext(update, context, data)


def npcs(update, context):
    bot_id = str(update.message.chat['id'])
    if bot_id not in registred_ids:
        new_register(bot_id, data)

    adm = all_done_missions(data, bot_id)
    all_npcs = NPC_data['NAME'].tolist()
    show = dict()
    for n in all_npcs:
        reveal_mission = str(NPC_data[NPC_data['NAME'] == n]['ACTIVATION_ID'].values[0])
        if reveal_mission in adm:
            show[n] = True
        else:
            show[n] = False

    particular_npc = str(update.message.text)[6:]
    if len(particular_npc) == 0:
        output_text = "Pots parlar amb els següents personatges:\n"
        for n, s in show.items():
            if s:
                output_text += "/talk " + n + "\n"

        update.message.reply_text(output_text)
    else:
        if show[particular_npc]:
            text_to_use = lore_text(particular_npc, NPC_data)
            if text_to_use:
                output_text = str(NPC_data[NPC_data['NAME'] == particular_npc][text_to_use].values[0])
                update.message.reply_text(output_text)
            else:
                update.message.reply_text("Hi ha hagut un error amb la base de dades, si us plau contacta a en @ShaggyGalaso")
        else:
            update.message.reply_text("El npc que has triat encara no el coneixes!!")


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

    # Commands related to lore
    dp.add_handler(CommandHandler("talk", npcs))

    # Commands related to competition
    dp.add_handler(CommandHandler("topfaction", topfaction))
    dp.add_handler(CommandHandler("top3", top3))
    dp.add_handler(CommandHandler("topteams", top_teams))

    # Commands related to teams
    dp.add_handler(CommandHandler("createteam", create_team))
    dp.add_handler(CommandHandler("jointeam", join_team))
    dp.add_handler(CommandHandler("showteam", show_team))
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
    dp.add_handler(CommandHandler("refreshinfluence", refresh_influences))
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