def check_is_founder(user_id, t_df):
    founders = t_df['FOUNDER'].tolist()
    if user_id in founders:
        return True
    else:
        return False


def select_language(l):
    if l == 'Català':
        return 'ca'
    elif l == "Castellano":
        return 'es'
    elif l == 'English':
        return 'en'
    else:
        return l


def decode_lore(update, val, bot_id, data):
    if "LORE" in val:
        own_faction = str(data[data['BOT_ID'] == bot_id]['FACTION'].values[0])
        if own_faction == "Neutral":
            update.message.reply_text(
                "Necessites ser d'una facció per fer aquesta missió: /joinanomalis o /joincorruptus")
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

    return val


def create_new_row(bot_id, data):
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
    new_row['AM_BOT'] = ' '

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
    new_row['DM_BOT'] = ' '

    new_row['WOKE'] = 'NO'

    # ID registration
    new_row['ID'] = max(data['ID']) + 1
    return new_row


def m_to_pic(done_missions):
    ret = dict()
    for m in done_missions:
        ret[m] = str(m) + '.jpeg'
    ret['ANOMA1'] = 'CIVICA1.jpeg'
    ret['ANOMA2'] = 'CIVICA1.jpeg'
    ret['CORRU1'] = 'CIVICA1.jpeg'
    ret['CORRU2'] = 'CIVICA1.jpeg'
    ret['COM1'] = 'COMU1.jpeg'
    ret['COM2'] = 'COMU2.jpeg'
    return ret


def bot_mission_count(data, user_id):
    return int(data[data['BOT_ID'] == user_id]['TM_BOT'].values[0])