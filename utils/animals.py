import requests
from random import randint
from bs4 import BeautifulSoup


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