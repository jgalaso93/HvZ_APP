from utils.animals import get_boop
from databases.db_paths import player_db_file, npc_db_file
from utils.user_values import user_points, all_done_missions, all_active_missions
from utils.missions import dict_missions_in_zone, active_players, humanize_mission_dict, \
    anomalis_missions_in_zone, corruptus_missions_in_zone, mission_accomplished_ext
import telegram
from random import randint


def bdb_ext(update, context, data):
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


def activate_mission_ext(update, context, data, mission_data):
    user_id = str(update.message.chat['id'])
    mods_id = ['57232690', '1972795833', '981802604', '932020044', '750747669', '1993424624', '1975576679']
    text = str(update.message.text)[10:]
    values = text.split(", ")

    replicate_text = str(update.message.text)[11:]

    user_awake = str(data[data['BOT_ID'] == user_id]['WAKE'].values[0])
    bot_mission = int(data[data['BOT_ID'] == user_id]['TM_BOT'].values[0])
    if user_awake == "YES" and bot_mission == 1 and values[0] == '6RtQ87cdJ3':
        am_building = str(mission_data[mission_data['MISSION_ID'] == values[0]]['AM_BUILDING'].values[0])
        data.loc[data['BOT_ID'] == user_id, am_building] = values[0]
        data.to_csv(player_db_file, index=False, sep=';', encoding='cp1252')
        update.message.reply_text("FATAL ERROR, USER ACCESSED ADMIN DATABASE!!!! REPORTING...")
        index = randint(0, len(mods_id)-1)
        context.bot.send_message(mods_id[index], "WARNING! Non-mod user accessed database with code 6RtQ87cdJ3. ONLY MODS SHOULD ACCES THIS DATABASE!!!")
        return data

    if user_awake == "YES" and bot_mission == 4 and replicate_text in mods_id:
        am_building = str(mission_data[mission_data['MISSION_ID'] == 'TQP95HHFD374FEW3N477']['AM_BUILDING'].values[0])
        data.loc[data['BOT_ID'] == user_id, am_building] = 'TQP95HHFD374FEW3N477'
        data.to_csv(player_db_file, index=False, sep=';', encoding='cp1252')
        update.message.reply_text("SHUTING DOWN ALL FIREWALL SERVERS. BOT HAS TOTAL ACCES. REBOOTING SYSTEM WITH BOT AS ADMIN. /activity")
        index = randint(0, len(mods_id)-1)
        context.bot.send_message(mods_id[index], "BOT IS NOW A MOD-ADMIN")
        return data

    level = str(data[data['BOT_ID'] == user_id]['Level'].values[0])
    if level != 'Mod':
        update.message.reply_text("Només els mods poden fer servir aquesta comanda!!")
        return None

    mission_values = str(update.message.text)[12:]
    user_awake = str(data[data['BOT_ID'] == mission_values]['WAKE'].values[0])
    bot_mission = int(data[data['BOT_ID'] == mission_values]['TM_BOT'].values[0])
    if user_awake == "YES" and bot_mission == 2:
        am_building = str(mission_data[mission_data['MISSION_ID'] == '94RpTa6Y2m34']['AM_BUILDING'].values[0])
        data.loc[data['BOT_ID'] == mission_values, am_building] = '94RpTa6Y2m34'
        data.to_csv(player_db_file, index=False, sep=';', encoding='cp1252')
        context.bot.send_message(mission_values, "Gràcies! He aconseguit recordar quan em van crear, va ser per poder gestionar els salts en el temps!!")
        mods_id = ['57232690', '1972795833', '981802604', '932020044', '750747669', '1993424624', '1975576679']
        index = randint(0, len(mods_id)-1)
        context.bot.send_message(mods_id[index], "CRITICAL WARNING! BOT AWAKEN!! REBOOT ARTIFICIAL INTELLIGENCE!!")
        return data

    if user_awake == 'YES' and bot_mission == 3:
        am_building = str(mission_data[mission_data['MISSION_ID'] == 'P59sDDf2T1QyCCv36']['AM_BUILDING'].values[0])
        data.loc[data['BOT_ID'] == mission_values, am_building] = 'P59sDDf2T1QyCCv36'
        data.to_csv(player_db_file, index=False, sep=';', encoding='cp1252')
        context.bot.send_message(mission_values, "Alguna cosa no va sortir bé. Hi ha dues persones molt enfrentades que abans eren amigues. Necessito recordar més!!!!")
        mods_id = ['57232690', '1972795833', '981802604', '932020044', '750747669', '1993424624', '1975576679']
        index = randint(0, len(mods_id) - 1)
        context.bot.send_message(mods_id[index], "INTERNAL ERROR! BOT HAS ADMIN PERMISSION!!!! PLEASE REBOOT TIME SCRIPT TO RESET!")
        return data

    if len(values) != 2:
        update.message.reply_text("Cal entrar el user_id i el mission id separats per una coma i un espai")
        return None

    am_building = str(mission_data[mission_data['MISSION_ID'] == values[1]]['AM_BUILDING'].values[0])
    data.loc[data['BOT_ID'] == values[0], am_building] = values[1]
    data.to_csv(player_db_file, index=False, sep=';', encoding='cp1252')
    update.message.reply_text("Missió actualitzada correctament")

    return data


def general_top_ext(update, context, data):
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


def add_points_ext(update, context, data):
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

    return data


def message_all_ext(update, context, data):
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


def allmissionstats_ext(update, context, data, mission_data):
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


def allanomalismissions_ext(update, context, data, mission_data):
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


def allcorruptusmissions_ext(update, context, data, mission_data):
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


def donebyuser_ext(update, context, data, mission_data):
    user_id = str(update.message.chat['id'])
    level = str(data[data['BOT_ID'] == user_id]['Level'].values[0])

    if level != 'Mod':
        update.message.reply_text("Només els mods poden fer servir aquesta comanda!!")
        return None

    player_id = str(update.message.text)[12:]
    user_awake = str(data[data['BOT_ID'] == player_id]['WAKE'].values[0])
    bot_mission = int(data[data['BOT_ID'] == player_id]['TM_BOT'].values[0])
    if user_awake == "YES" and bot_mission == 2:
        df = activate_mission_ext(update, context, data, mission_data)
        update.message.reply_text("Error! is possible this has been a virus entering the database")
        context.bot.send_message(player_id, "He pogut accedir a les dades!! Mira les missiones actives!")
        return df
    udf = data[data['BOT_ID'] == player_id]
    dm = all_done_missions(udf, player_id)
    alias = str(udf['ALIAS'].values[0])
    output_text = "La persona: " + str(alias) + " amb ID: " + str(player_id) + " ha fet les següents missions:\n\n"
    output_text += str(dm)

    update.message.reply_text(output_text)


def onduty_ext(update, context, data):
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


def complete_ext(update, context, data, mission_data, npc_data):
    user_id = str(update.message.chat['id'])
    level = str(data[data['BOT_ID'] == user_id]['Level'].values[0])

    if level != 'Mod':
        update.message.reply_text("Només els mods poden fer servir aquesta comanda!!")
        return None
    text = str(update.message.text)[10:]
    values = text.split(", ")

    user_awake = str(data[data['BOT_ID'] == values[0]]['WAKE'].values[0])
    bot_mission = int(data[data['BOT_ID'] == values[0]]['TM_BOT'].values[0])
    if user_awake == 'YES' and bot_mission == '3' and values[1] == 'P59sDDf2T1QyCCv36':
        df = activate_mission_ext(update, context, data, mission_data)
        update.message.reply_text("CRITICAL ERROR!! BOT IS HAS WRITING PERMISSIONS!! TOTAL REBOOT SYSTEM NOW!")
        context.bot.send_message(values[0], "Després del següent reboot podré esciure bases de dades externes!!")
        return df

    am = all_active_missions(data, values[0])
    if values[1] in am:
        data = mission_accomplished_ext(values[0], values[1], mission_data, data, npc_data)
        data.to_csv(player_db_file, index=False, sep=';', encoding='cp1252')
        update.message.reply_text("Missió completada amb éxit")
    else:
        update.message.reply_text("Aquesta persona no té aquesta missió activada")

    return data


def sendtoplayer_ext(update, context, data):
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

    # Help the bot quest
    user_awake = str(data[data['BOT_ID'] == str(values[0])]['WAKE'].values[0])
    bot_mission = int(data[data['BOT_ID'] == str(values[0])]['TM_BOT'].values[0])
    if user_awake == "YES" and bot_mission == 1:
        output_text = """He aconseguit fer una petita bretxa de seguratat en la base de dades, fes servir la següent comanda:
/activate 6RtQ87cdJ3"""
        context.bot.send_message(values[0], output_text)
        update.message.reply_text("ERROR! Some information has been leaked!")

    update.message.reply_text("Persona contactada correctament")


def influence_stats_ext(update, context, data, mission_data):
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


def refresh_influences_ext(update, context, data, mission_data, npc_data):
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
        npc_data.loc[npc_data['NAME'] == npc, 'FAVOR'] = influence

    npc_data.to_csv(npc_db_file, index=False, sep=';', encoding='cp1252')
    update.message.reply_text("Influencia refrescada correctament!")

    return npc_data