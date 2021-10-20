import os
import cv2
import tempfile
import shutil
from googletrans import Translator

from utils.user_values import amount_of_missions_done, all_done_missions, all_active_missions
from databases.db_paths import player_db_file, npc_db_file
from utils.helpers import decode_lore

translator = Translator(service_urls=[
      'translate.google.com',
      'translate.google.co.kr',
    ])


def dict_of_missions(ams, ret={}):
    """
    ams: list or Series of zones
        all missions from the data
    ret: dictionary that can be empty
    """
    ams = list(filter(lambda x: x != ' ', ams))
    for p in ams:
        ms = p.split(", ")
        for m in ms:
            try:
                ret[m] += 1
            except:
                ret[m] = 1

    return ret


def dict_missions_in_zone(df, zone, ret={}):
    m = df[zone]
    return dict_of_missions(m, ret)


def anomalis_missions_in_zone(df, zone, ret={}):
    m = df[df['FACTION'] == 'Anomalis'][zone]
    return dict_of_missions(m, ret)


def corruptus_missions_in_zone(df, zone, ret={}):
    m = df[df['FACTION'] == 'Corruptus'][zone]
    return dict_of_missions(m, ret)


def humanize_mission_dict(d, m_df):
    """
    Function to create a text humanly readable about missions
    d: dictionary that can be empty
    m_df: mission_dataframe
    """
    d = dict(sorted(d.items(), key=lambda item: item[1], reverse=True))
    output_text = ""
    counter = 1
    for key, value in d.items():
        try:
            npc = str(m_df[m_df['MISSION_ID'] == key]['NPC'].values[0])
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


def lore_text(npc, npc_data):
    """
    npc_data: NPC_database
    """
    all_npcs = npc_data['NAME'].tolist()
    if npc in all_npcs:
        favor = int(npc_data[npc_data['NAME'] == npc]['FAVOR'].values[0])
        if favor <= -6:
            return "CORRUPTUS1"
        if favor >= 6:
            return "ANOMALIS1"
        return "NEUTRAL"
    else:
        return False


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


def mission_accomplished_ext(user_id, mission_id, mission_data, data, npc_data):
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
        add_influence(npc, 1, faction, npc_data)
    except IndexError:
        pass

    return data


def add_influence(npc_name, influence_points, user_faction, NPC_data):
    actual_points = NPC_data[NPC_data['NAME'] == npc_name]['FAVOR']
    favor_value = position_value(actual_points, user_faction)
    NPC_data.loc[NPC_data['NAME'] == npc_name, 'FAVOR'] = actual_points + (influence_points * favor_value)
    NPC_data.to_csv(npc_db_file, index=False, sep=';', encoding='cp1252')


def mission_can_be_done_ext(user_id, mission_id, data, mission_data):
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


def check_answer_ext(user_id, answer, data, mission_data):
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


def read_qr_ext(update, context, bot_id, mission_ids, data, mission_data):
    file = update.message.photo[-1].file_id
    obj = context.bot.get_file(file)
    tmp_dir = tempfile.mkdtemp()
    filename = os.path.join(tmp_dir, 'tmp_file.jpg')
    obj.download(filename)
    img = cv2.imread(filename=filename)
    shutil.rmtree(tmp_dir)
    det = cv2.QRCodeDetector()
    val, pts, st_code = det.detectAndDecode(img)

    val = decode_lore(update, val, bot_id, data)

    if val == "":
        update.message.reply_text("Esta imagen no contiene ningún QR!")
    else:
        if val in mission_ids:
            done_missions = all_done_missions(data, update.message.chat['id'])
            if val in done_missions:
                update.message.reply_text("Ja has fet aquesta missió!!")
            else:
                data = throw_mission(update, val, update.message.chat['id'], data, mission_data)
        else:
            update.message.reply_text("Aquest QR no té cap missió associada!")

    return data


def throw_mission(update, mission_id, user_id, data, mission_data):
    pending = mission_can_be_done_ext(str(user_id), mission_id, data, mission_data)
    aam = all_active_missions(data, str(user_id))
    adm = all_done_missions(data, str(user_id))
    if mission_id in adm:
        update.message.reply_text("Ja has fet aquesta missió! No pots tornar-la a fer!!")
        return None

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
    data.to_csv(player_db_file, index=False, sep=';', encoding='cp1252')
    if language == 'ca':
        final_text = text
    else:
        translated_text = translator.translate(text=text, dest=language)
        final_text = translated_text.text

    try:
        update.message.reply_text(final_text)
    except:
        update.message.reply_text("Hi ha un problema amb la base de dades d'aquesta missió, "
                                  "si us plau contacta amb el moderador Shaggy, gracies :)")

    return data


def missions(update, context):
    # '\n/Aulari'
    # '\n/Carpa'
    # '\n/Civica'
    # '\n/Torres'
    # '\n/Educacio'

    # if True:
    #     update.message.reply_text('Les missions estan en manteniment, si us plau, tornau a intentar en unes hores :)')
    #     return None
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
                      '\n/Veterinaria'
                      '\n/Civica'
                      '\n/Ocult')