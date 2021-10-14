from utils.user_values import user_points, amount_of_missions_done
from utils.helpers import check_is_founder
from utils.animals import get_boop
from databases.db_paths import player_db_file, teams_db_file

from random import choice


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


def create_team_ext(update, context, data, teams_data):
    team_name = str(update.message.text)[12:]
    user_id = str(update.message.chat['id'])

    data.loc[data['BOT_ID'] == user_id, 'GUILD'] = team_name
    data.loc[data['BOT_ID'] == user_id, 'GUILD_LEVEL'] = 'Founder'

    data.to_csv(player_db_file, index=False, sep=';', encoding='cp1252')

    founders = teams_data['FOUNDER'].tolist()

    if user_id in founders:
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
            teams_data.to_csv(teams_db_file, index=False, sep=';', encoding='cp1252')

            context.bot.send_message(new_leader, "El fundador del teu equip ha marxat, ara ets el nou fundador!")

    else:
        new_row = dict()
        new_row['GUILD'] = team_name
        new_row['FOUNDER'] = user_id
        new_row['REQUESTS'] = 'None'

        teams_data = teams_data.append(new_row, ignore_index=True)
        teams_data.to_csv(teams_db_file,  index=False, sep=';', encoding='cp1252')

    reply_message = "L'equip " + team_name + " s'ha creat correctament!!! El teu rang és \"Founder\""
    update.message.reply_text(reply_message)
    return data, teams_data


def join_team_ext(update, context, data, teams_data):
    team_name = str(update.message.text)[10:]
    user_id = str(update.message.chat['id'])
    own_alias = str(data[data['BOT_ID'] == user_id]['ALIAS'].values[0])

    if team_name in teams_data['GUILD'].tolist():
        actual_requests = teams_data[teams_data['GUILD'] == team_name]['REQUESTS'].tolist()
        actual_requests.append(user_id)
        actual_requests = ', '.join(str(r) for r in actual_requests)
        teams_data.loc[teams_data['GUILD'] == team_name, 'REQUESTS'] = actual_requests
        teams_data.to_csv(teams_db_file, index=False, sep=';', encoding='cp1252')
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

    return teams_data


def promote_ext(update, context, data, teams_data):
    registred_ids = data['BOT_ID'].tolist()
    text = str(update.message.text)[9:]
    values = text.split(", ")
    if len(values) == 1:
        update.message.reply_text("Compte! Has de separar l'alias i el rang per una coma i només un espai!")
        return None
    bot_id = str(update.message.chat['id'])

    if bot_id not in registred_ids:
        update.message.reply_text("El teu registre no estava complert! Fes /start")
        return 0

    guild_name = str(data[data['BOT_ID'] == bot_id]['GUILD'].values[0])
    if guild_name == " ":
        update.message.reply_text("No formes part de cap equip!")
        return 0

    founders = teams_data['FOUNDER'].tolist()
    if bot_id not in founders:
        update.message.reply_text("Només els \"Founders\" poden promocionar gent del seu equip!")
        return 0

    data.loc[(data['GUILD'] == guild_name) & (data['ALIAS'] == str(values[0])), 'GUILD_LEVEL'] = str(values[1])
    data.to_csv(player_db_file, index=False, sep=';', encoding='cp1252')

    output_text = "Totes les persones amb alies " + values[0] + " han sigut ascendides a " + values[1]
    update.message.reply_text(output_text)

    return data


def kick_ext(update, context, data, teams_data):
    text = str(update.message.text)[6:]
    bot_id = str(update.message.chat['id'])
    if check_is_founder(bot_id, teams_data):
        team_name = str(teams_data[teams_data['FOUNDER'] == bot_id]['GUILD'].values[0])
        if text == bot_id:
            update.message.reply_text("No et pots fer fora a tu mateix del teu equip!")
            return None
        member_ids = data[data['GUILD'] == team_name]['BOT_ID'].tolist()
        for i in member_ids:
            if text == str(i):
                data.loc[data['BOT_ID'] == i, 'GUILD'] = ' '
                data.loc[data['BOT_ID'] == i, 'GUILD_LEVEL'] = 'unguilded'
                data.to_csv(player_db_file, index=False, sep=';', encoding='cp1252')
                update.message.reply_text("Has expulsat a la persona del teu equip!")
                context.bot.send_message(i, "T'han fet fora del teu equip!")
                return None
        update.message.reply_text("No hi ha ningú amb aquest id al teu equip!")
    else:
        update.message.reply_text("Només els founders poden fer fora a algu de l'equip!")

    return data


def admit_ext(update, context, data, teams_data):
    text = str(update.message.text)[7:]
    bot_id = str(update.message.chat['id'])
    if check_is_founder(bot_id, teams_data):
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

        data.to_csv(player_db_file, index=False, sep=';', encoding='cp1252')

        actual_requests = str(teams_data[teams_data['FOUNDER'] == bot_id]['REQUESTS'].values[0])
        actual_requests = actual_requests.split(", ")
        actual_requests.remove(text)
        if len(actual_requests) == 0:
            actual_requests = 'None'
        else:
            actual_requests = ', '.join(str(r) for r in actual_requests)
        teams_data.loc[teams_data['FOUNDER'] == bot_id, 'REQUESTS'] = actual_requests

        teams_data.to_csv(teams_db_file, index=False, sep=';', encoding='cp1252')

        update.message.reply_text("Has acceptat a l'usuari amb id " + text)
        context.bot.send_message(text, "Has entrat a l'equip: " + team_name)
    else:
        update.message.reply_text("Només els founders poden ademtre a algu a l'equip!")

    return data, teams_data


def decline_ext(update, context, data, teams_data):
    text = str(update.message.text)[9:]
    bot_id = str(update.message.chat['id'])
    if check_is_founder(bot_id, teams_data):
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

        teams_data.to_csv(teams_db_file, index=False, sep=';', encoding='cp1252')

        update.message.reply_text("Has denegat a l'usuari amb id " + text + ". No se li comunicarà res a aquesta persona")
    else:
        update.message.reply_text("Només els founders poden ademtre a algu a l'equip!")

    return data, teams_data


def sendboop_ext(update, context, data):
    bot_id = str(update.message.chat['id'])

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


def sendall_ext(update, context, data):
    bot_id = str(update.message.chat['id'])

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


def sendallboop_ext(update, context, data):
    bot_id = str(update.message.chat['id'])

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