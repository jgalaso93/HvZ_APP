#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

import logging
import os
import sys
import pandas as pd
from random import randint

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from databases.db_paths import teams_db_file, player_db_file, \
    npc_db_file, conversation_db_file, missions_db_file, npc_conversation_db_file, \
    npc_db_file_w2, cats_db_file

from utils.user_values import all_done_missions

from utils.animals import boop, meow, ribbit, ardillita, pok, ezo, slugs, potatoes, snek, getcat_ext

from utils.missions import lore_text, mission_accomplished_ext, check_answer_ext, read_qr_ext, missions

from utils.guild import show_team_ext, mem_ids_ext, req_ids_ext, create_team_ext, \
    join_team_ext, promote_ext, kick_ext, admit_ext, decline_ext, sendboop_ext, \
    sendall_ext, sendallboop_ext

from utils.database_functions import new_register_ext, set_alias_ext, show_me_ext, \
    activity_ext, hint_ext, join_anomalis_ext, join_corruptus_ext, set_language_ext, \
    donebyme_ext

from utils.competitive_functions import topfaction_ext, top_teams_ext, top3_ext

from utils.mods import bdb_ext, activate_mission_ext, general_top_ext, add_points_ext, \
    message_all_ext, allmissionstats_ext, allanomalismissions_ext, allcorruptusmissions_ext, \
    donebyuser_ext, onduty_ext, complete_ext, sendtoplayer_ext, influence_stats_ext, \
    refresh_influences_ext

from utils.pic_sender import Civica, Veterinaria_ext, Aulari, Carpa, Comunicacio_ext, Edifici_B_central_ext, \
    Edifici_B_Nord_ext, Edifici_B_Sud_ext, Edifici_C_ext, Educacio, Etse_ext, FTI_ext, Medicina_ext, SAF_ext, \
    Torres, Ocult_ext

from utils.bot_help import contact, help_basic, help_mod_ext, help_team, help, help_personal, \
    help_competitive, help_founder_ext, start_ext, rules, use

from utils.helpers import m_to_pic

#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#----------------------DATABASE VARIABLES-----------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

try:
    data = pd.read_csv(player_db_file, sep=';', header=0, dtype={'BOT_ID': str}, encoding='cp1252')
except:
    data = pd.read_csv(player_db_file, sep=',', header=0, dtype={'BOT_ID': str}, encoding='cp1252')

registred_ids = data['BOT_ID'].tolist()

mission_data = pd.read_csv(missions_db_file, sep=';', header=0,
                           dtype={'MISSION': str, 'RESULT_POOL': str},
                           encoding='cp1252')
mission_ids = mission_data['MISSION_ID'].tolist()

NPC_data = pd.read_csv(npc_db_file, sep=';', header=0, encoding='cp1252')
NPC_data2 = pd.read_csv(npc_db_file_w2, sep=';', header=0, encoding='cp1252')

conver_data = pd.read_csv(conversation_db_file, sep=';', header=0, dtype={'BOT_ID': str}, encoding='cp1252')
talk_input = conver_data['INPUT'].tolist()
talk_output = conver_data['OUTPUT'].tolist()
talk = {k: v for k, v in zip(talk_input, talk_output)}

teams_data = pd.read_csv(teams_db_file, sep=';', header=0, encoding='cp1252', dtype={'FOUNDER': str})

npc_conversation_data = pd.read_csv(npc_conversation_db_file, sep=';', header=0, encoding='cp1252')

data_cat = pd.read_csv(cats_db_file, sep=';', header=0, encoding='cp1252', dtype={'BOT_ID': str})


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


def read_qr(update, context):
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
    data = new_register_ext(bot_id, data)

    # Update the registred id's
    global registred_ids
    registred_ids = data['BOT_ID'].tolist()


def register(update, context):
    bot_id = update.message.chat['id']
    if str(bot_id) in registred_ids:
        update.message.reply_text('Tu registro ya está completado')
    else:
        new_register(bot_id, data)
        update.message.reply_text('Te has registrado!')


def start(update, context):
    bot_id = str(update.message.chat['id'])
    if bot_id not in registred_ids:
        new_register(bot_id, data)
    start_ext(update, context)


def set_alias(update, context):
    global data
    data = set_alias_ext(update, context, data)


def get_my_id(update, context):
    update.message.reply_text(update.message.chat['id'])


def show_me(update, context):
    show_me_ext(update, context, data)


def activity(update, context):
    activity_ext(update, context, data, mission_data)


def hint(update, context):
    hint_ext(update, context, data, mission_data)


def join_anomalis(update, context):
    global data
    data = join_anomalis_ext(update, context, data)


def join_corruptus(update, context):
    global data
    data = join_corruptus_ext(update, context, data)


def set_language(update, context):
    global data
    data = set_language_ext(update, context, data)


def getcat(update, context):
    getcat_ext(update, data_cat)


def donebyme(update, context):
    donebyme_ext(update, data)


#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#----------------------COMPETITIVE FUNCTIONS--------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

def topfaction(update, context):
    topfaction_ext(update, context, data)


def top_teams(update, context):
    top_teams_ext(update, context, data)


def top3(update, context):
    top3_ext(update, context, data)


#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#----------------------HELP FUNCTIONS---------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

def help_founder(update, context):
    help_founder_ext(update, context, teams_data)


def help_mod(update, context):
    help_mod_ext(update, context, data)


#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#----------------------ANSWER FUNCTIONS-------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------


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
    if particular_npc is not None:
        values = particular_npc.split(", ")
    else:
        values = []
    if len(values) == 2:
        if show[values[0]]:
            update.message.reply_text(talktome(values[0], values[1]))
            return None
        else:
            update.message.reply_text("Primer has de trobar aquest NPC per parlar-li!!")
            return None
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
                dfs = [NPC_data, NPC_data2]
                rn = randint(0, (len(dfs) - 1))
                df = dfs[rn]
                output_text = str(df[df['NAME'] == particular_npc][text_to_use].values[0])
                update.message.reply_text(output_text)
            else:
                update.message.reply_text("Hi ha hagut un error amb la base de dades, si us plau contacta a en @ShaggyGalaso")
        else:
            update.message.reply_text("El npc que has triat encara no el coneixes!!")


def talktome(npc, word):
    try:
        output = str(npc_conversation_data[npc_conversation_data['INPUT'] == word][npc].values[0])
    except IndexError:
        output = "No conec el que m'estàs dient, però pots intentar alguna altra frase"
    return output


#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#----------------------SENDERS FUNCTIONS------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

def get_done_pics(update):
    bot_id = str(update.message.chat['id'])
    adm = all_done_missions(data, bot_id)
    return m_to_pic(adm)


def Comunicacio(update, context):
    done_pics = get_done_pics(update)
    Comunicacio_ext(update, context, done_pics)


def Edifici_B_central(update, context):
    done_pics = get_done_pics(update)
    Edifici_B_central_ext(update, context, done_pics)


def Edifici_B_Nord(update, context):
    done_pics = get_done_pics(update)
    Edifici_B_Nord_ext(update, context, done_pics)


def Edifici_B_Sud(update, context):
    done_pics = get_done_pics(update)
    Edifici_B_Sud_ext(update, context, done_pics)


def Edifici_C(update, context):
    done_pics = get_done_pics(update)
    Edifici_C_ext(update, context, done_pics)


def Etse(update, context):
    done_pics = get_done_pics(update)
    Etse_ext(update, context, done_pics)


def FTI(update, context):
    done_pics = get_done_pics(update)
    FTI_ext(update, context, done_pics)


def Medicina(update, context):
    done_pics = get_done_pics(update)
    Medicina_ext(update, context, done_pics)


def SAF(update, context):
    done_pics = get_done_pics(update)
    SAF_ext(update, context, done_pics)


def Veterinaria(update, context):
    done_pics = get_done_pics(update)
    Veterinaria_ext(update, context, done_pics)


def Ocult(update, context):
    done_pics = get_done_pics(update)
    Ocult_ext(update, context, done_pics)


#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#----------------------MODS FUNCTIONS---------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

def bdb(update, context):
    bdb_ext(update, context, data)


def activate_mission(update, context):
    global data
    data = activate_mission_ext(update, context, data, mission_data)


def general_top(update, context):
    general_top_ext(update, context, data)


def add_points(update, context):
    global data
    data = add_points_ext(update, context, data)


def message_all(update, context):
    message_all_ext(update, context, data)


def allmissionstats(update, context):
    allmissionstats_ext(update, context, data, mission_data)


def allanomalismissions(update, context):
    allanomalismissions_ext(update, context, data, mission_data)


def allcorruptusmissions(update, context):
    allcorruptusmissions_ext(update, context, data, mission_data)


def donebyuser(update, context):
    donebyuser_ext(update, context, data)


def onduty(update, context):
    onduty_ext(update, context, data)


def complete(update, context):
    global data
    data = complete_ext(update, context, data, mission_data, NPC_data)


def sendtoplayer(update, context):
    sendtoplayer_ext(update, context, data)


def influence_stats(update, context):
    influence_stats_ext(update, context, data, mission_data)


def refresh_influences(update, context):
    global NPC_data
    NPC_data = refresh_influences_ext(update, context, data, mission_data, NPC_data)


#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#----------------------OTHER FUNCTIONS--------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

def halal(update, context):
    """Send a halal message when the command /halal is issued"""
    update.message.reply_text('القرآن')


def corruptus(update, context):
    """Send corruptus description when the command /corruptus is issued"""
    update.message.reply_text('Des de temps immemorials del passat, la diversitat d’idees ha portat a la Humanitat a viure grans guerres i conflictes que només han acabat amb la masacre de vides i amb la pèrdua dels nostres iguals. És hora de deixar enrere el individualisme egoista i el benestar personal i unir-nos sota un nou líder que alliberi finalment als éssers humans de la seva càrrega. No més desigualtat, no més destrucció. Volem un món pacífic per tots i això només ho aconseguirem plegats. La heterogeneïtat present en la societat és l’origen de tots els problemes actuals! És hora de canviar, uneix-te per preservar i salvar el planeta!')


def test(update, context):
    """Send link to the aliniation test"""
    update.message.reply_text('https://bit.ly/3urA0S0')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    # update.message.reply_text("Alguna cosa ha anat malament! Torna-ho a intentar o contacte amb @ShaggyGalaso")


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


#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#----------------------MAIN LOOP--------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

def main():
    """Start the bot."""
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
    dp.add_handler(CommandHandler("donebyme", donebyme))
    dp.add_handler(CommandHandler("hint", hint))
    dp.add_handler(CommandHandler("joinanomalis", join_anomalis))
    dp.add_handler(CommandHandler("joincorruptus", join_corruptus))
    dp.add_handler(CommandHandler("setlanguage", set_language))
    dp.add_handler(CommandHandler("boop", boop))
    dp.add_handler(CommandHandler("meow", meow))
    dp.add_handler(CommandHandler("ribbit", ribbit))
    dp.add_handler(CommandHandler("ardillita", ardillita))
    dp.add_handler(CommandHandler("pok", pok))
    dp.add_handler(CommandHandler("ezo", ezo))
    dp.add_handler(CommandHandler("pft", slugs))
    dp.add_handler(CommandHandler("potato", potatoes))
    dp.add_handler(CommandHandler("snek", snek))

    # Commands for help
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("help_personal", help_personal))
    dp.add_handler(CommandHandler("help_team", help_team))
    dp.add_handler(CommandHandler("help_competitive", help_competitive))
    dp.add_handler(CommandHandler("help_basic", help_basic))
    dp.add_handler(CommandHandler("help_founder", help_founder))
    dp.add_handler(CommandHandler("contact", contact))
    dp.add_handler(CommandHandler("use", use))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("rules", rules))

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

    # Other Commands
    dp.add_handler(CommandHandler("halal", halal))
    dp.add_handler(CommandHandler("corruptus", corruptus))
    dp.add_handler(CommandHandler("test", test))

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
    dp.add_handler(CommandHandler("Ocult", Ocult))

    # Commands about CATS of Menor
    dp.add_handler(CommandHandler("getcat", getcat))

    # on noncommand i.e message - tree decision (WIP)
    dp.add_handler(MessageHandler(Filters.text, echo))

    # on noncommand i.e pictures - activate QR protocol
    dp.add_handler(MessageHandler(Filters.photo, read_qr))

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