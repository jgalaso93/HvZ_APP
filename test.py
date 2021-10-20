import time
import os
import sys
import pandas as pd
from databases.db_paths import npc_db_file, player_db_file, teams_db_file, \
    conversation_db_file, missions_db_file, npc_conversation_db_file
from utils.user_values import all_done_missions
import requests
from random import randint
from bs4 import BeautifulSoup

from random import randrange

pic_folder = os.path.join(sys.path[0], 'QR activos')


data = pd.read_csv(player_db_file, sep=';', header=0, dtype={'BOT_ID': str}, encoding='cp1252')

mission_database_file = os.path.join(sys.path[0], 'bkcupmissiones_semana1.csv')
# mission_database_file = os.path.join(sys.path[0], 'mission_database.csv')
mission_data = pd.read_csv(missions_db_file, sep=';', header=0,
                   dtype={'MISSION': str, 'RESULT_POOL': str},
                   encoding='cp1252')

NPC_file = os.path.join(sys.path[0], 'NPC_database.csv')
NPC_data = pd.read_csv(npc_db_file, sep=';', header=0, encoding='cp1252')

conver_file = os.path.join(sys.path[0], 'conversation_database.csv')
conver_data = pd.read_csv(conversation_db_file, sep=';', header=0, encoding='cp1252')

teams_file = os.path.join(sys.path[0], 'teams_database.csv')
teams_data = pd.read_csv(teams_db_file, sep=';', header=0, encoding='cp1252', dtype={'FOUNDER': str})

npc_conversation_data = pd.read_csv(npc_conversation_db_file, sep=';', header=0, encoding='cp1252')


# url = 'https://www.google.com/search?q=babosas&tbm=isch&ved=2ahUKEwiWy8qF_NTzAhUJQhoKHT1ECF0Q2-cCegQIABAA&oq=babosas&gs_lcp=CgNpbWcQAzIFCAAQgAQyBQgAEIAEMgQIABAeMgQIABAeMgQIABAeMgQIABAeMgQIABAeMgQIABAeMgQIABAeMgQIABAeOgcIIxDvAxAnOgYIABAHEB46BAgAEEM6CAgAEIAEELEDOggIABCxAxCDAVCrngFYsacBYKaoAWgAcAB4AIABWIgBkgWSAQE4mAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=0-9tYdaVFYmEab2IoegF&bih=665&biw=1300&rlz=1C1CHBF_esES843ES843'
# content = requests.get(url)
#
# if content.status_code == 200:
#     soup = BeautifulSoup(content.content, "html.parser")
#
# print(soup)
# content = str(soup).split('<')
# print(content)
# filtred_content = []
# for v in content:
#     if 'img' in v and 'https' in v:
#         filtred_content.append(v)
#
# print(len(filtred_content))
#
# print(filtred_content)
# only_pics = []
# for fv in filtred_content:
#     s = fv.split("\"")
#     for v in s:
#         if 'https' in v:
#             only_pics.append(v)
#
# print(only_pics)


def scrap_pics(url):
    content = requests.get(url)

    if content.status_code == 200:
        soup = BeautifulSoup(content.content, "html.parser")

    content = str(soup).split('<')
    filtred_content = []
    for v in content:
        if 'img' in v and 'https' in v:
            filtred_content.append(v)

    only_pics = []
    for fv in filtred_content:
        s = fv.split("\"")
        for v in s:
            if 'https' in v:
                only_pics.append(v)
    return only_pics


a = scrap_pics('https://bit.ly/3lThJKB')
print(a)

# def m_to_pic(done_missions):
#     ret = dict()
#     for m in done_missions:
#         ret[m] = str(m) + '.jpeg'
#     ret['ANOMA1'] = 'CIVICA1.jpeg'
#     ret['ANOMA2'] = 'CIVICA1.jpeg'
#     ret['CORRU1'] = 'CIVICA1.jpeg'
#     ret['CORRU2'] = 'CIVICA1.jpeg'
#     ret['COM1'] = 'COMU1.jpeg'
#     ret['COM2'] = 'COMU2.jpeg'
#     return ret



# bot_id = '2034151605'
# bot_id = '981802604'
# adm = all_done_missions(data, bot_id)
# done_pics = m_to_pic(adm)
#
# foto_path = os.path.join(pic_folder, 'COM')
# pics_in_folder = os.listdir(foto_path)
# pics_aviable = []
# print(pics_in_folder)
# for p in pics_in_folder:
#     if p in done_pics.values():
#         pass
#     else:
#         pics_aviable.append(p)
# print(pics_aviable)
#
# number_of_photos = len(pics_aviable)
# if number_of_photos == 0:
#     update.message.reply_text("No et queden missions en aquesta zona!")
# else:
#     index = randrange(number_of_photos)
#     final_foto_path = os.path.join(foto_path, pics_aviable[index])











# print(npc_conversation_data)
#
#
# def talktome(npc, input):
#     try:
#         output = str(npc_conversation_data[npc_conversation_data['INPUT'] == input][npc].values[0])
#     except IndexError:
#         output = "No conec el que m'estàs dient, però pots intentar alguna altra frase"
#     return output
#
# print(talktome('Rosa Parks', 'fbhrusil'))



# print(player_db_file)
# data = pd.read_csv(player_db_file, sep=';', header=0, dtype={'BOT_ID': str}, encoding='cp1252')
# print(data)
# all_npcs = NPC_data['NAME'].tolist()
#
# print(all_npcs)

# team_name = 'Escuadrón Suicida'
# user_id = '2068411147'
# bot_id = '1754447751'
# requested_ids = str(teams_data[teams_data['FOUNDER'] == bot_id]['REQUESTS'].values[0])
# requested_ids = requested_ids.split(", ")
#
# if user_id not in requested_ids:
#     print("YAS")
#
# data.loc[data['BOT_ID'] == user_id, 'GUILD'] = team_name
# data.loc[data['BOT_ID'] == user_id, 'GUILD_LEVEL'] = 'Newbie'
#
# print(data[data['BOT_ID'] == user_id]['GUILD'])
# print(data[data['BOT_ID'] == user_id]['GUILD_LEVEL'])
#
# print(requested_ids)

# actual_requests = teams_data[teams_data['GUILD'] == team_name]['REQUESTS'].tolist()
# actual_requests.append(user_id)
# actual_requests = ', '.join(str(r) for r in actual_requests)
# teams_data.loc[teams_data['GUILD'] == team_name, 'REQUESTS'] = actual_requests
# print(teams_data)
# teams_data.to_csv(teams_file, index=False, sep=';', encoding='cp1252')

# def all_done_missions(df, user_id):
#     """
#     For a given user_id returns all the done missions as a list of strings
#     """
#     done_missions = []
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Aulari'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Carpa'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Civica'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Comunicacio'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_EB_Sud'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_EB_Nord'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_EB_Central'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_ETSE'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_FTI'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Med'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_SAF'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_EC'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Torres'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Vet'])
#     done_missions = list(filter(lambda x: x != ' ', done_missions))
#     final_missions = []
#     for ms in done_missions:
#         missions_subset = ms.split(", ")
#         for mis in missions_subset:
#             final_missions.append(mis)
#     return final_missions
#
#
# all_ids = data['BOT_ID'].tolist()
# # print(all_ids)
# id_faction = dict()
# id_missions = dict()
# faction_values = {'Anomalis': 1, 'Corruptus': -1}
# # print(faction_values)
# for i in all_ids:
#     value = all_done_missions(data, i)
#     if len(value) != 0:
#         key = str(data[data['BOT_ID'] == i]['FACTION'].values[0])
#         if key == "Neutral":
#             continue
#         id_faction[i] = key
#         id_missions[i] = value
#
# # print(id_faction)
# # print(id_missions)
#
# all_mission_id = mission_data['MISSION_ID'].tolist()
#
# mission_npc = dict()
# for mid in all_mission_id:
#     npc = str(mission_data[mission_data['MISSION_ID'] == mid]['NPC'].values[0])
#     if npc == 'nan':
#         continue
#     mission_npc[mid] = npc
#
# # print(mission_npc)
# npc_influence = dict()
# for n in mission_npc.values():
#     npc_influence[n] = 0
#
# # print(npc_influence)
# for i in id_missions.keys():
#     inf_value = faction_values[id_faction[i]]
#     missions = id_missions[i]
#     for m in missions:
#         if m in mission_npc.keys():
#             npc = mission_npc[m]
#             actual_value = npc_influence[npc]
#             actual_value += inf_value
#             npc_influence[npc] = actual_value
#
# # print(npc_influence)
# output_text = "Així està l'actual estat d'influencia: \n(Positiu Anomalis, Negatiu Corruptus)\n\n"
# for k, v in npc_influence.items():
#     output_text += str(k) + ": " + str(v) + "\n"
#
# print(output_text)







#
# a = teams_data['FOUNDER'].tolist()
# print(a)
# if '981802604' in a:
#     print("YAS")
#
# a = '132'
#
# b = ['132']
#
# if a in b:
#     print("YAS")




# founders = data[data['GUILD_LEVEL'] == 'Founder']['BOT_ID'].tolist()
# for f in founders:
#     guild = str(data[data['BOT_ID'] == f]['GUILD'].values[0])
#     new_row = dict()
#     new_row['GUILD'] = str(guild)
#     new_row['FOUNDER'] = str(f)
#     new_row['PASSWORD'] = 'None'
#     teams_data = teams_data.append(new_row, ignore_index=True)
#
# teams_data.to_csv(teams_file, sep=";", index=False)




# all_m = data[data['GUILD'] == 'Patatas']['BOT_ID'].tolist()
# a = choice(all_m)
# print(a)
#
# b = ', '.join(str(i) for i in all_m)
# print(b)
# print(type(b))
#
# a = teams_data[teams_data['GUILD'] == 'Patatas']['REQUESTS'].tolist()
# print(a)
# if a[0] == 'None':
#     print("YAS")

















# user_id = '1754447751'
# udf = data[data['BOT_ID'] == user_id]
# dm = all_done_missions(udf, user_id)
# alias = (udf['ALIAS'].values[0])
# output_text = "L'usuari: " + alias + " amb ID: " + user_id + "ha fet les següents missions:\n\n"
# output_text += str(dm)
#
# print(output_text)




# def guild_points(guild_name):
#     gdf = data[data['GUILD'] == guild_name]
#     gids = gdf['BOT_ID'].tolist()
#     t_points = 0
#     for i in gids:
#         t_points += user_points(gdf, i)
#
#     return t_points
#
# # print(data['GUILD'].tolist())
# guilds = data['GUILD'].tolist()
# guilds = list(filter(lambda x: x != ' ', guilds))
# guilds = set(guilds)
# g_score = dict()
#
# for g in guilds:
#     g_points = guild_points(g)
#     if g_points > 0:
#         g_score[g] = g_points
#
# g_score = dict(sorted(g_score.items(), key=lambda item: item[1], reverse=True))
#
# last_points = max(g_score.values())
# position = 1
# counter = 1
# top = 10
# output_text = "El top de los equipos es:\n\n"
# for key, value in g_score.items():
#     if last_points != value:
#         position += 1
#         last_points = value
#     output_text += str(position) + ". " + str(key) + ": " + str(value) + "\n"
#     if counter == top:
#         break
#     counter += 1
#
# print(output_text)
















# all_ids = data['BOT_ID'].tolist()
# count = 0
# for i in all_ids:
#     m = amount_of_missions_done(data, i)
#     if m > 0:
#         count += 1
#
# print(count - 2)
#
# d = data[data['FACTION'] == 'Corruptus']
# print(d)
# all_ids = d['BOT_ID'].tolist()
# count = 0
# for i in all_ids:
#     m = amount_of_missions_done(d, i)
#     if m > 0:
#         count += 1














#
# # print(data['DM_EC'].tolist())
# all_c = data['DM_EC'].tolist()
# all_c = list(filter(lambda x: x != ' ', all_c))
# # print(all_c)
# cie = dict()
# for p in all_c:
#     ms = p.split(", ")
#     for m in ms:
#         try:
#             cie[m] += 1
#         except:
#             cie[m] = 1
#
# print(cie)
#
#
# def dict_of_missions(all, ret={}):
#     all = list(filter(lambda x: x != ' ', all))
#     for p in all:
#         ms = p.split(", ")
#         for m in ms:
#             try:
#                 ret[m] += 1
#             except:
#                 ret[m] = 1
#
#     return ret
#
# missions = dict()
#
# missions = dict_of_missions(data['DM_Aulari'], missions)
# missions = dict_of_missions(data['DM_Carpa'], missions)
# missions = dict_of_missions(data['DM_Civica'], missions)
# missions = dict_of_missions(data['DM_Comunicacio'], missions)
# missions = dict_of_missions(data['DM_EB_Sud'], missions)
# missions = dict_of_missions(data['DM_EB_Nord'], missions)
# missions = dict_of_missions(data['DM_EB_Central'], missions)
# missions = dict_of_missions(data['DM_ETSE'], missions)
# missions = dict_of_missions(data['DM_FTI'], missions)
# missions = dict_of_missions(data['DM_Med'], missions)
# missions = dict_of_missions(data['DM_SAF'], missions)
# missions = dict_of_missions(data['DM_EC'], missions)
# missions = dict_of_missions(data['DM_Torres'], missions)
# missions = dict_of_missions(data['DM_Vet'], missions)
#
# print(missions)
#
# missions = dict(sorted(missions.items(), key=lambda item: item[1], reverse=True))
# output_text = ""
# for key, value in missions.items():
#     try:
#         npc = str(mission_data[mission_data['MISSION_ID'] == key]['NPC'].values[0])
#     except:
#         npc = ' '
#
#     output_text += "Missió: " + key + ". NPC: " + npc + ". Volum: " + str(value) +"\n"
#
# print (output_text)














#
# page = "http://allaboutfrogs.org/funstuff/randomfrog.html"
# content = requests.get(page)
# print(content.content)

# file = open("file1.jpg", "wb")
# file.write(content.content)
# file.close()


# if content.status_code == 200:
#     soup = BeautifulSoup(content.content, "html.parser")
#
# print(soup)

# while soup.img is None:
#     content = requests.get(page)
#     soup = BeautifulSoup(content.content, "html.parser")

# return page + str(soup.img)[23:-3]
# print(soup.img)
#
# list_of_frogs = [
# "http://www.allaboutfrogs.org/funstuff/random/0001.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0002.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0003.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0004.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0005.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0006.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0007.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0008.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0009.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0010.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0011.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0012.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0013.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0014.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0015.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0016.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0017.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0018.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0019.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0020.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0021.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0022.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0023.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0024.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0025.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0026.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0027.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0028.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0028.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0029.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0030.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0031.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0032.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0033.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0034.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0035.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0036.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0037.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0038.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0039.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0040.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0041.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0042.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0043.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0044.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0045.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0046.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0047.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0048.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0049.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0050.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0051.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0052.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0053.jpg",
# "http://www.allaboutfrogs.org/funstuff/random/0054.jpg"
# ]
#
# random_num = randint(0, (len(list_of_frogs)-1))
# page = list_of_frogs[random_num]
# content = requests.get(page)
#
# file = open("file1.jpg", "wb")
# file.write(content.content)
# file.close()










# print(conver_data)
#
# talk_input = conver_data['INPUT'].tolist()
# talk_output = conver_data['OUTPUT'].tolist()
# talk = {k: v for k, v in zip(talk_input, talk_output)}




















# all_ids = data['BOT_ID'].tolist()
# score = dict()
# for i in all_ids:
#     points = user_points(data, i)
#     if points > 0:
#         score[i] = points
#
# score = dict(sorted(score.items(), key=lambda item: item[1], reverse=True))
# print(score)
#
# output_text = "El top 5 del joc tenen les següents puntuacions:\n\n"
#
# counter = 1
# for k, v in score.items():
#     output_text += str(counter) + ": " + str(v) + "\n"
#     if counter >= 3:
#         break
#     counter += 1
#
# output_text += "\nEnhorabona i seguiu així!!!!"
#
# print (output_text)



# anomalis_df = data[(data['FACTION'] == 'Anomalis') & (data['Level'] == 'Player')]
# a_ids = anomalis_df['BOT_ID'].tolist()
# # print(a_ids)
# score = dict()
# for ai in a_ids:
#     points = user_points(anomalis_df, ai)
#     if points > 0:
#         score[ai] = points
# print(score)
# score = dict(sorted(score.items(), key=lambda item: item[1], reverse=True))
# print(score)
# output_text = "Les millors puntuacions de la vostra facció són:\n"
# last_points = max(score.values())
# position = 1
# counter = 1
#
# for key, value in score.items():
#     alias = str(anomalis_df[anomalis_df['BOT_ID'] == key]['ALIAS'].values[0])
#     if alias == 'no_alias':
#         continue
#     if last_points != value:
#         position += 1
#         last_points = value
#     output_text += str(position) + ". " + alias + ": " + str(value) + "\n"
#     if counter == 5:
#         break
#     counter += 1
#
# n = ''
# int (n)
# print(output_text)












# import requests
# from bs4 import BeautifulSoup
# import urllib
#
# page = "https://random.dog/"
# data = requests.get(page)
#
# if data.status_code == 200:
#     soup = BeautifulSoup(data.content, "html.parser")
#
# print(soup.img)
# image_name = str(soup.img)[23:-3]
# print(str(soup.img)[23:-3])
# image_url = page + str(soup.img)[23:-3]
# print(image_url)
#
# page = requests.get(image_url)
#
# f_ext = os.path.splitext(image_url)[-1]
# f_name = 'img{}'.format(f_ext)
# with open(f_name, 'wb') as f:
#     f.write(page.content)

from urllib.request import urlopen
from PIL import Image


# from PIL import Image
# import requests
# from io import BytesIO
# from StringIO import StringIO
#
# response = requests.get(page)
# img = Image.open(StringIO(response.raw))









# def all_done_missions(df, user_id):
#     """
#     For a given user_id returns all the done missions as a list of strings
#     """
#     done_missions = []
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Aulari'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Carpa'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Civica'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Comunicacio'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_EB_Sud'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_EB_Nord'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_EB_Central'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_ETSE'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_FTI'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Med'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_SAF'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_EC'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Torres'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Vet'])
#     done_missions = list(filter(lambda x: x != ' ', done_missions))
#     return done_missions
#
#
# #
#

#
#
# dm = all_done_missions(data, '981802604')
# print(dm)













# final_text = str(mission_data[mission_data['MISSION_ID'] == 'C1']['FINAL_TEXT'].values[0])
# print(final_text)






# translator = Translator(service_urls=[
#       'translate.google.com',
#       'translate.google.co.kr',
#     ])
# text = translator.translate(text='안녕하세요.', dest='en')
# print(text.text)






# mission = str(mission_data[mission_data['MISSION_ID'] == 'C6']['MISSION_P1'].values[0])
# print(mission)
# translated = translator.translate(text=mission, dest='en')
# print(translated.text)
#
#
# str(data[data['BOT_ID'] == '132']['LANGUAGE'].values[0])



# grup = data[data['BOT_ID'] == '1805031879']['FACTION'].values[0]
# print(grup)
# data.loc[data['BOT_ID'] == '1805031879', 'FACTION'] = 'Neutral'
# grup = data[data['BOT_ID'] == '1805031879']['FACTION'].values[0]
# print(grup)
# # data.to_csv(database_file, index=False, sep=';')











# def position_value(npc_favor, user_faction):
#     if user_faction == 'Anomalis':
#         return 1
#     if user_faction == 'Corruptus':
#         return -1
#
#     if user_faction == 'Neutral':
#         if npc_favor > 0:
#             return -1
#         if npc_favor < 0:
#             return 1
#         if npc_favor == 0:
#             return 0



#
# def add_influence(npc_name, influence_points):
#     actual_points = NPC_data[NPC_data['NAME'] == npc_name]['FAVOR']
#     NPC_data.loc[NPC_data['NAME'] == npc_name, 'FAVOR'] = actual_points + influence_points
#     NPC_data.to_csv(NPC_file, index=False, sep=';')




# # am = ['C1', 'COM2', 'VET1', 'BNORD1']
#
#
# def all_active_missions(df, user_id):
#     """
#     For a given user_id returns all the active missions as a list of strings
#     """
#     active_missions = []
#     active_missions.extend(df[df['BOT_ID'] == user_id]['AM_Aulari'])
#     active_missions.extend(df[df['BOT_ID'] == user_id]['AM_Carpa'])
#     active_missions.extend(df[df['BOT_ID'] == user_id]['AM_Civica'])
#     active_missions.extend(df[df['BOT_ID'] == user_id]['AM_Comunicacio'])
#     active_missions.extend(df[df['BOT_ID'] == user_id]['AM_EB_Sud'])
#     active_missions.extend(df[df['BOT_ID'] == user_id]['AM_EB_Nord'])
#     active_missions.extend(df[df['BOT_ID'] == user_id]['AM_EB_Central'])
#     active_missions.extend(df[df['BOT_ID'] == user_id]['AM_ETSE'])
#     active_missions.extend(df[df['BOT_ID'] == user_id]['AM_FTI'])
#     active_missions.extend(df[df['BOT_ID'] == user_id]['AM_Med'])
#     active_missions.extend(df[df['BOT_ID'] == user_id]['AM_SAF'])
#     active_missions.extend(df[df['BOT_ID'] == user_id]['AM_EC'])
#     active_missions.extend(df[df['BOT_ID'] == user_id]['AM_Torres'])
#     active_missions.extend(df[df['BOT_ID'] == user_id]['AM_Vet'])
#     active_missions = list(filter(lambda x: x != ' ', active_missions))
#     return active_missions
#
# am = all_active_missions(data, '132')
#
# output_text = "Missions actives acutals, codi i enunciat\n"
# am = ['PATATA']
# for m in am:
#     try:
#         output_text += str(m) + ": "
#         output_text += str(mission_data[mission_data['MISSION_ID'] == m]['MISSION_P1'].values[0])
#         output_text += "\n"
#     except IndexError:
#         print("YAS")
#
# print(output_text)

# print(mission_data[data['MISSION_ID'] == am]['MISSION_ID'])

# path = os.path.join(sys.path[0], 'zarigueyas.txt')
# file = open(path, "r")
# zz = file.read()
# print(zz)
# file.close()




#
# def user_points(df, user_id):
#     """
#     For a given user_id returns the amount of points achieved due to missions
#     """
#     total_points = 0
#     total_points += df[df['BOT_ID'] == user_id]['P_Aulari']
#     total_points += df[df['BOT_ID'] == user_id]['P_Carpa']
#     total_points += df[df['BOT_ID'] == user_id]['P_Civica']
#     total_points += df[df['BOT_ID'] == user_id]['P_Comunicacio']
#     total_points += df[df['BOT_ID'] == user_id]['P_EB_Sud']
#     total_points += df[df['BOT_ID'] == user_id]['P_EB_Nord']
#     total_points += df[df['BOT_ID'] == user_id]['P_EB_Central']
#     total_points += df[df['BOT_ID'] == user_id]['P_ETSE']
#     total_points += df[df['BOT_ID'] == user_id]['P_FTI']
#     total_points += df[df['BOT_ID'] == user_id]['P_Med']
#     total_points += df[df['BOT_ID'] == user_id]['P_SAF']
#     total_points += df[df['BOT_ID'] == user_id]['P_EC']
#     total_points += df[df['BOT_ID'] == user_id]['P_Torres']
#     total_points += df[df['BOT_ID'] == user_id]['P_Vet']
#     return total_points.values[0]
#
#
# def amount_of_missions_done(df, user_id):
#
#     """
#     For a given user_id returns the amount of missions done by this user
#     """
#     amount_missions = 0
#     amount_missions += df[df['BOT_ID'] == user_id]['TM_Aulari']
#     amount_missions += df[df['BOT_ID'] == user_id]['TM_Carpa']
#     amount_missions += df[df['BOT_ID'] == user_id]['TM_Civica']
#     amount_missions += df[df['BOT_ID'] == user_id]['TM_Comunicacio']
#     amount_missions += df[df['BOT_ID'] == user_id]['TM_EB_Sud']
#     amount_missions += df[df['BOT_ID'] == user_id]['TM_EB_Nord']
#     amount_missions += df[df['BOT_ID'] == user_id]['TM_EB_Central']
#     amount_missions += df[df['BOT_ID'] == user_id]['TM_ETSE']
#     amount_missions += df[df['BOT_ID'] == user_id]['TM_FTI']
#     amount_missions += df[df['BOT_ID'] == user_id]['TM_Med']
#     amount_missions += df[df['BOT_ID'] == user_id]['TM_SAF']
#     amount_missions += df[df['BOT_ID'] == user_id]['TM_EC']
#     amount_missions += df[df['BOT_ID'] == user_id]['TM_Torres']
#     amount_missions += df[df['BOT_ID'] == user_id]['TM_Vet']
#     return amount_missions.values[0]
#
#
# database_file = os.path.join(sys.path[0], 'database.csv')
# data = pd.read_csv(database_file, sep=';', header=0, dtype={'BOT_ID': str})
#
# # bot_id = update.message.chat['id']
# guild_name = str(data[data['BOT_ID'] == '981802604']['GUILD'].values[0])
#
# guild_ids = data[data['GUILD'] == 'Patatas']['BOT_ID'].tolist()
# output_text = ""
# for bid in guild_ids:
#     print (data[data['BOT_ID'] == bid]["ALIAS"])
#     output_text += "La persona amb alies: " + str(data[data['BOT_ID'] == bid]["ALIAS"].values[0])
#     done_missions = amount_of_missions_done(data, bid)
#     tp = user_points(data, bid)
#     output_text += " ha fet " + str(done_missions) + " missions"
#     output_text += " i actualment te " + str(tp)
#     output_text += " punts per la seva faccio\n"
#
# print(output_text)
#












# from datetime import datetime
# from datetime import timedelta
#
# d = datetime.now()
# t = timedelta(seconds=15)
#
# d1 = d + t
#
# print(d)
# print(d < d1)
#
# st = d.strftime("%d/%m/%Y; %H:%M:%S")
#
# print(st)
#
# d2 = datetime.strptime(st, '%d/%m/%Y; %H:%M:%S')
#
# print(d2)




# database_file = os.path.join(sys.path[0], 'database.csv')
# data = pd.read_csv(database_file, sep=';', header=0, dtype={'BOT_ID': str})
#
# mission_database_file = os.path.join(sys.path[0], 'mission_database.csv')
# mission_data = pd.read_csv(mission_database_file, sep=';', header=0,
#                    dtype={'MISSION': str, 'RESULT_POOL': str},
#                    encoding='cp1252')
#
# def amount_of_missions_done(df, user_id):
#     """
#     For a given user_id returns the amount of points achieved due to missions
#     """
#     total_points = 0
#     total_points += df[df['BOT_ID'] == user_id]['P_Aulari']
#     total_points += df[df['BOT_ID'] == user_id]['P_Carpa']
#     total_points += df[df['BOT_ID'] == user_id]['P_Civica']
#     total_points += df[df['BOT_ID'] == user_id]['P_Comunicacio']
#     total_points += df[df['BOT_ID'] == user_id]['P_EB_Sud']
#     total_points += df[df['BOT_ID'] == user_id]['P_EB_Nord']
#     total_points += df[df['BOT_ID'] == user_id]['P_EB_Central']
#     total_points += df[df['BOT_ID'] == user_id]['P_ETSE']
#     total_points += df[df['BOT_ID'] == user_id]['P_FTI']
#     total_points += df[df['BOT_ID'] == user_id]['P_Med']
#     total_points += df[df['BOT_ID'] == user_id]['P_SAF']
#     total_points += df[df['BOT_ID'] == user_id]['P_EC']
#     total_points += df[df['BOT_ID'] == user_id]['P_Torres']
#     total_points += df[df['BOT_ID'] == user_id]['P_Vet']
#     return total_points


# def mission_accomplished(user_id, mission_id):
#     building = mission_data[mission_data['MISSION_ID'] == mission_id]['AM_BUILDING']
#     am_filed = building.values[0]
#     dm_field = 'D' + am_filed[1:]
#     tm_field = 'T' + am_filed[1:]
#     p_field = 'P' + am_filed[2:]
#     done_missions = data[data['BOT_ID'] == user_id][dm_field]
#     total_missions = data[data['BOT_ID'] == user_id][tm_field]
#     mission_points = mission_data[mission_data['MISSION_ID'] == mission_id]['POINTS']
#     total_points = data[data['BOT_ID'] == user_id][p_field]
#     try:
#         if done_missions.values[0] == ' ':
#             updated_done_missions = mission_id
#         else:
#             updated_done_missions = done_missions.values[0] + ', ' + mission_id
#     except:
#         updated_done_missions = mission_id
#
#     data.loc[data['BOT_ID'] == user_id, am_filed] = ' '
#     data.loc[data['BOT_ID'] == user_id, dm_field] = updated_done_missions
#     data.loc[data['BOT_ID'] == user_id, tm_field] = total_missions.values[0] + 1
#     data.loc[data['BOT_ID'] == user_id, p_field] = total_points.values[0] + mission_points
#
#     data.to_csv(database_file, index=False, sep=';')
#
# user_id = '132'
# mission_id = 'C1'
# mission_accomplished(user_id, mission_id)
#
#
# b = mission_data[mission_data['MISSION_ID'] == mission_id]['AM_BUILDING']
# print(b.values[0])



# def all_done_missions(df, user_id):
#     """
#     For a given user_id returns all the active missions as a list of strings
#     """
#     done_missions = []
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Aulari'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Carpa'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Civica'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Comunicacio'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_EB_Sud'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_EB_Nord'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_EB_Central'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_ETSE'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_FTI'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Med'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_SAF'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_EC'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Torres'])
#     done_missions.extend(df[df['BOT_ID'] == user_id]['DM_Vet'])
#     done_missions = list(filter(lambda x: x != ' ', done_missions))
#     return done_missions
#
# user_id = '132'
# a = all_done_missions(data, user_id)
# print(a)



# def all_active_missions(df, user_id):
#     active_missions = []
#     active_missions.extend(df[df['BOT_ID'] == user_id]['AM_Aulari'])
#     active_missions.extend(df[df['BOT_ID'] == user_id]['AM_Carpa'])
#     active_missions.extend(df[df['BOT_ID'] == user_id]['AM_Civica'])
#     active_missions.extend(df[df['BOT_ID'] == user_id]['AM_Comunicacio'])
#     active_missions.extend(df[df['BOT_ID'] == user_id]['AM_EB_Sud'])
#     active_missions.extend(df[df['BOT_ID'] == user_id]['AM_EB_Nord'])
#     active_missions.extend(df[df['BOT_ID'] == user_id]['AM_EB_Central'])
#     active_missions.extend(df[df['BOT_ID'] == user_id]['AM_ETSE'])
#     active_missions.extend(df[df['BOT_ID'] == user_id]['AM_FTI'])
#     active_missions.extend(df[df['BOT_ID'] == user_id]['AM_Med'])
#     active_missions.extend(df[df['BOT_ID'] == user_id]['AM_SAF'])
#     active_missions.extend(df[df['BOT_ID'] == user_id]['AM_EC'])
#     active_missions.extend(df[df['BOT_ID'] == user_id]['AM_Torres'])
#     active_missions.extend(df[df['BOT_ID'] == user_id]['AM_Vet'])
#     active_missions = list(filter(lambda x: x != ' ', active_missions))
#     return active_missions
#
# def valid_answers(df, tam):
#     va = dict()
#     for am in tam:
#         result_pool = df[df['MISSION_ID'] == am]['RESULT_POOL']
#         try:
#             va[am] = result_pool.values[0].split(", ")
#         except IndexError:
#             pass
#     return va
#
#
# def check_answer(answer, va):
#     for key, value in va.items():
#         if answer in value:
#             return key
#
#     return False
#
#
# tam = all_active_missions(data, '981802604')
# va = valid_answers(mission_data, tam)
# print(tam)
# print(va)
#
# a = check_answer('patata', va)
# print(a)
#
# a = check_answer('Groc', va)
# print(a)


# mission_id = 'C2'
#
# print(mission_data['MISSION'])
# print(mission_data[mission_data['MISSION_ID'] == 'C2'])
# print(type(mission_data[mission_data['MISSION_ID'] == 'C2']['RESULT_POOL']))
#
# if str(mission_data[mission_data['MISSION_ID'] == 'C2']['RESULT_POOL']).find("Groga") != -1:
#     print("YES")
#
# text = mission_data[mission_data['MISSION_ID'] == mission_id]['MISSION']
# am = mission_data[mission_data['MISSION_ID'] == mission_id]['AM_BUILDING']
# # user_row = data.where(data=='57232690').dropna(how='all').dropna(axis=1)
# # user_col = am_col(str(am.values[0]))
# # data[data['BOT_ID'] == '981802604'][am] = mission_id
#
# data.loc[data['BOT_ID'] == '57232690', 'AM_EC'] = 'C2'
#
# # print(user_row.index)
# # print(user_col)
#
# print(data)
# print(am.values[0][3:])





# import telebot
# import telegram.ext
#
# print(dir(telegram.ext))

# p= [{'file_id': 'AgACAgQAAxkBAAIBQWFHWIXTwqaLCP865CLAC_aTAX4lAAKatjEbyxs4Uteo29rB5EumAQADAgADcwADIAQ', 'file_size': 2374, 'height': 79,'file_unique_id': 'AQADmrYxG8sbOFJ4', 'width': 90}, {'file_id': 'AgACAgQAAxkBAAIBQWFHWIXTwqaLCP865CLAC_aTAX4lAAKatjEbyxs4Uteo29rB5EumAQADAgADbQADIAQ', 'file_size': 8474, 'height': 150, 'file_unique_id': 'AQADmrYxG8sbOFJy', 'width': 170}]
import cv2
import json
# file1 = 'D:\\Proyectos\\HvZ\\HvZ PvE\\HvZ_APP\\file_1.png'
# file = 'D:\\Proyectos\\HvZ\\HvZ PvE\\QR Holiwi.png'
# # file = 'D:\\Proyectos\\HvZ\\HvZ PvE\\HvZ_APP\\Fotos de llocs a la uab\\Civica\\en la escalera.jpeg'
# img = cv2.imread(file)
# det = cv2.QRCodeDetector()
# print(det)
# val, pts, st_code=det.detectAndDecode(img)
# print(val)
# if val == '':
#     print("YES")
#
# # p_dict = json.loads(p[0])
# #
# # print(p_dict)
#
# img = cv2.imread(file)
# img1 = cv2.imread(file1)
# val1, pts1, st_code1 =det.detectAndDecode(img1)
# print("YES")








# import os
# import sys
# from qrtools.qrtools import QR
# import cv2
#
# folder = 'D:\\Proyectos\\HvZ\\HvZ PvE'
# # print(os.listdir(folder))
# file = 'D:\\Proyectos\\HvZ\\HvZ PvE\\QR Holiwi.png'
# my_QR = QR(filename=file)
# my_QR.decode()
# print (my_QR.data)







# import os
# import sys
#
# foto_path = sys.path[0]
# foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
# foto_path = os.path.join(foto_path, 'Edifici C')
#
# print(foto_path)
# print(os.listdir(foto_path))
# final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[0])
#
# print(final_foto_path)





# import os
# import sys
# import pandas as pd
#
# database_file = os.path.join(sys.path[0], 'database.csv')
#
# data = pd.read_csv(database_file, sep=';', header=0, dtype={'BOT_ID':str})
#
# print(data)
# print(type(data))
# print(data['BOT_ID'])
#
# if '981802604' in data['BOT_ID'].tolist():
#     print("yas")
#
# print(len(data.columns))
#
# new_row = dict()
# field = 'BOT_ID'
# value = '1975576679'
# for column in data.columns:
#     if column == field:
#         new_row[column] = str(value)
#         print("yes")
#     else:
#         new_row[column] = None
#         print("no")
# #
#
#
# print(max(data['ID']))
# new_row['ID'] = max(data['ID'])+1
#
# print(new_row)
#
# data = data.append(new_row, ignore_index=True)
#
# # values = [0 for _ in range(len(data.columns))]
# # data.append(dict(zip(data.columns, values)), ignore_index=True)
#
# print(data)
# #
# data.to_csv(database_file, index=False)
#
#
# # if data.isin({'ID': ['981802604']}):
# #     print ("yas")