from utils.user_values import user_points
from utils.guild import guild_points


def topfaction_ext(update, context, data):
    bot_id = str(update.message.chat['id'])

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


def top_teams_ext(update, context, data):
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


def top3_ext(update, context, data):
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