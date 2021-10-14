from utils.user_values import user_points, amount_of_missions_done
from utils.helpers import check_is_founder


def guild_points(guild_name, data):
    gdf = data[data['GUILD'] == guild_name]
    gids = gdf['BOT_ID'].tolist()
    t_points = 0
    for i in gids:
        t_points += user_points(gdf, i)

    return t_points


def show_team_ext(update, context, data):
    bot_id = str(update.message.chat['id'])
    guild_name = str(data[data['BOT_ID'] == bot_id]['GUILD'].values[0])

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


def mem_ids_ext(update, data, teams_data):
    bot_id = str(update.message.chat['id'])
    if check_is_founder(bot_id, teams_data):
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


def req_ids_ext(update, data, teams_data):
    bot_id = str(update.message.chat['id'])
    if check_is_founder(bot_id, teams_data):
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