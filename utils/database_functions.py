from utils.helpers import create_new_row, select_language
from utils.user_values import amount_of_missions_done, user_points, all_active_missions, all_done_missions
from databases.db_paths import player_db_file

from googletrans import Translator

translator = Translator(service_urls=[
      'translate.google.com',
      'translate.google.co.kr',
    ])


def new_register_ext(bot_id, data):
    new_row = create_new_row(bot_id, data)
    data = data.append(new_row, ignore_index=True)
    data.to_csv(player_db_file, index=False, sep=';', encoding='cp1252')
    return data


def set_alias_ext(update, context, data):
    alias = str(update.message.text)[10:]
    bot_id = str(update.message.chat['id'])

    if alias == '' or alias is None:
        update.message.reply_text("L'alias que has escollit no és vàlid!!")
    else:
        data.loc[data['BOT_ID'] == bot_id, 'ALIAS'] = alias
        data.to_csv(player_db_file, index=False, sep=';', encoding='cp1252')

        output_text = 'El teu alias ha canviat correctament a ' + alias
        update.message.reply_text(output_text)

    return data


def show_me_ext(update, context, data):
    bot_id = str(update.message.chat['id'])

    output_text = "El teu alias és " + str(data[data['BOT_ID'] == bot_id]['ALIAS'].values[0]) + "\n"
    output_text += "El teu equip és " + str(data[data['BOT_ID'] == bot_id]['GUILD'].values[0]) + "\n"
    output_text += "El teu rang és " + str(data[data['BOT_ID'] == bot_id]['GUILD_LEVEL'].values[0]) + "\n"
    output_text += "La teva facció és " + str(data[data['BOT_ID'] == bot_id]['FACTION'].values[0]) + "\n"

    dm = amount_of_missions_done(data, bot_id)
    tp = user_points(data, bot_id)

    output_text += "Has fet un total de " + str(dm) + " missions per tot el campus\n"
    output_text += "Tens acumulats un total de " + str(tp) + " punts per la teva facció\n"

    update.message.reply_text(output_text)


def activity_ext(update, context, data, mission_data):
    bot_id = str(update.message.chat['id'])

    am = all_active_missions(data, bot_id)
    output_text = "Missions actives actuals, codi i enunciat\n"
    for m in am:
        output_text += str(m) + ": "
        output_text += str(mission_data[mission_data['MISSION_ID'] == m]['MISSION_P1'].values[0])
        output_text += "\n"

    update.message.reply_text(output_text)


def hint_ext(update, context, data, mission_data):
    bot_id = str(update.message.chat['id'])

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


def join_anomalis_ext(update, context, data):
    bot_id = str(update.message.chat['id'])

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

    return data


def join_corruptus_ext(update, context, data):
    bot_id = str(update.message.chat['id'])

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

    return data


def set_language_ext(update, context, data):
    bot_id = str(update.message.chat['id'])

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

    return data


def donebyme_ext(update, data):
    user_id = str(update.message.chat['id'])

    udf = data[data['BOT_ID'] == user_id]
    dm = all_done_missions(udf, user_id)
    output_text = "Has fet les següents missions:\n\n"
    output_text += str(dm)

    update.message.reply_text(output_text)
