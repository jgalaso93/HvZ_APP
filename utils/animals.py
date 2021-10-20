import os
import random

import requests
from random import randint
from bs4 import BeautifulSoup
from databases.db_paths import cats_db_file, cat_folder


list_of_frogs = [
"http://www.allaboutfrogs.org/funstuff/random/0001.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0002.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0003.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0004.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0005.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0006.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0007.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0008.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0009.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0010.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0011.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0012.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0013.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0014.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0015.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0016.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0017.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0018.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0019.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0020.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0021.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0022.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0023.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0024.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0025.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0026.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0027.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0028.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0028.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0029.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0030.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0031.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0032.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0033.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0034.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0035.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0036.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0037.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0038.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0039.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0040.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0041.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0042.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0043.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0044.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0045.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0046.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0047.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0048.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0049.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0050.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0051.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0052.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0053.jpg",
"http://www.allaboutfrogs.org/funstuff/random/0054.jpg"
]


def get_boop():
    page = "https://random.dog/"
    content = requests.get(page)

    if content.status_code == 200:
        soup = BeautifulSoup(content.content, "html.parser")

    while soup.img is None:
        content = requests.get(page)
        soup = BeautifulSoup(content.content, "html.parser")

    return page + str(soup.img)[23:-3]


def boop(update, context):
    image_url = get_boop()
    image = requests.get(image_url)
    update.message.reply_photo(image.content)


def meow(update, context):
    page = "https://cataas.com/cat"
    content = requests.get(page)
    if content.status_code == 200:
        update.message.reply_photo(content.content)


def ribbit(update, context):
    random_num = randint(0, (len(list_of_frogs) - 1))
    page = list_of_frogs[random_num]
    content = requests.get(page)
    if content.status_code == 200:
        update.message.reply_photo(content.content)


def get_boop():
    page = "https://random.dog/"
    content = requests.get(page)

    if content.status_code == 200:
        soup = BeautifulSoup(content.content, "html.parser")

    while soup.img is None:
        content = requests.get(page)
        soup = BeautifulSoup(content.content, "html.parser")

    return page + str(soup.img)[23:-3]


def ardillita(update, context):
    update.message.reply_text("La ardillita estará siempre en nuestros corazones. Love you Rigoberta. RIP")
    rigoberta_path = "D:\\Proyectos\\HvZ\\HvZ PvE\\HvZ_APP\\databases\\Animalicos\\Rigoberta.jpg"
    with open(rigoberta_path, "rb") as rigoberta:
        update.message.reply_photo(rigoberta)


def pok(update, context):
    url = 'https://www.generatormix.com/random-turtles'
    content = requests.get(url)
    if content.status_code == 200:
        soup = BeautifulSoup(content.content, "html.parser")
    values = str(soup.img).split("\"")
    page = ''
    for v in values:
        if 'https' in v:
            page = v
            break
    image = requests.get(page)
    update.message.reply_photo(image.content)


def ezo(update, message):
    file_path = "D:\\Proyectos\\HvZ\\HvZ PvE\\HvZ_APP\\databases\\Animalicos\\pok.png"
    with open(file_path, "rb") as pok:
        update.message.reply_photo(pok)
    update.message.reply_text("pok")


def scrap_pics(url):
    content = requests.get(url)

    if content.status_code == 200:
        soup = BeautifulSoup(content.content, "html.parser")
    else:
        return None

    content = str(soup).split('<')
    filtered_content = []
    for v in content:
        if 'img' in v and 'https' in v:
            filtered_content.append(v)

    only_pics = []
    for fv in filtered_content:
        s = fv.split("\"")
        for v in s:
            if 'https' in v:
                only_pics.append(v)
    return only_pics


def slugs(update, context):
    urls = ['https://bit.ly/3lThJKB', 'https://bit.ly/3AYihTH', 'https://bit.ly/3FXFB82']
    random_num = randint(0, (len(urls) - 1))
    pics = scrap_pics(urls[random_num])
    if pics:
        image_sender(update, pics)
    else:
        slugs(update, context)


def potatoes(update, context):
    urls = ['https://bit.ly/3aSDcgB', 'https://bit.ly/3vmylO2', 'https://bit.ly/2YZbVqb']
    random_num = randint(0, (len(urls) - 1))
    pics = scrap_pics(urls[random_num])
    if pics:
        image_sender(update, pics)
    else:
        potatoes(update, context)


def snek(update, context):
    urls = ['https://bit.ly/3n7NO0Q', 'https://bit.ly/3AT24PY']
    random_num = randint(0, (len(urls) - 1))
    pics = scrap_pics(urls[random_num])
    if pics:
        image_sender(update, pics)
    else:
        snek(update, context)


def image_sender(update, pics):
    random_pic = randint(0, (len(pics) - 1))
    content = requests.get(pics[random_pic])
    if content.status_code == 200:
        try:
            update.message.reply_photo(content.content)
        except:
            image_sender(update, pics)


#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#----------------------CATS FUNCTIONS---------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------


def getcat_ext(update, data_cat):
    bot_id = str(update.message.chat['id'])
    visitor_ids = data_cat['BOT_ID'].tolist()

    if bot_id not in visitor_ids:
        data_cat = addvisitor(bot_id, data_cat)

    cat = esElCosmos()

    if not visitedcat(bot_id, data_cat, cat):
        addcat(bot_id, data_cat, cat)

    showcat(update, cat)

    return data_cat


# Funcion que mira si ya tienes ese gato
def visitedcat(bot_id, data_cat, cat):
    visited_cats = str(data_cat[data_cat['BOT_ID'] == bot_id]['CATS'].values[0]).split(", ")
    if cat in visited_cats:
        return True
    else:
        return False


# Funcion que añade un gato a una persona a la base de datos de los gatos que se han visitado
def addcat(bot_id, data_cat, cat):
    visited_cats = str(data_cat[data_cat['BOT_ID'] == bot_id]['CATS'].values[0])

    if visited_cats == ' ':
        visited_cats = cat
    else:
        visited_cats = visited_cats.split(", ")
        visited_cats.append(cat)
        visited_cats = ', '.join(visited_cats)

    data_cat.loc[data_cat['BOT_ID'] == bot_id, 'CATS'] = visited_cats
    data_cat.to_csv(cats_db_file, index=False, sep=';', encoding='cp1252')
    return data_cat


# Funcion que añade una persona a la base de datos sin gatos
def addvisitor(bot_id, data_cat):
    new_row = dict()
    new_row['BOT_ID'] = bot_id
    new_row['CATS'] = ' '
    data_cat = data_cat.append(new_row, ignore_index=True)
    data_cat.to_csv(cats_db_file, index=False, sep=';', encoding='cp1252')
    return data_cat


# Funcion que enseña un gato
def showcat(update, cat):
    file_path = os.path.join(cat_folder, cat)
    with open(file_path, "rb") as pic:
        update.message.reply_photo(pic)
        update.message.reply_text("You've found a "+cat)


# Probabilidades gatos
def esElCosmos():
    commonCats = os.listdir(os.path.join(cat_folder, "commonCats"))
    rareCats = os.listdir(os.path.join(cat_folder, "rareCats"))
    epicCats = os.listdir(os.path.join(cat_folder, "epicCats"))
    legendaryCats = os.listdir(os.path.join(cat_folder, "legendaryCats"))
    theCat = os.listdir(os.path.join(cat_folder, "THECAT"))

    commonProb = 850
    rareProb = 950
    epicProb = 990
    legendaryProb = 999
    theCatProb = 1000

    random_num = randint(0, 500)
    if random_num < commonProb:
        random_cat = randint(0, len(commonCats)-1)
        return os.path.join("commonCats", commonCats[random_cat])
    elif random_num < rareProb:
        random_cat = randint(0, len(rareCats)-1)
        return os.path.join("rareCats", rareCats[random_cat])
    elif random_num < epicProb:
        random_cat = randint(0, len(epicCats)-1)
        return os.path.join("epicCats", epicCats[random_cat])
    elif random_num < legendaryProb:
        random_cat = randint(0, len(legendaryCats)-1)
        return os.path.join("legendaryCats", legendaryCats[random_cat])
    elif random_num < theCatProb:
        random_cat = randint(0, len(theCat)-1)
        return os.path.join("THECAT", theCat[random_cat])
