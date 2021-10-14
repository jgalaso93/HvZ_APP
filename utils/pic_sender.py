import sys
import os
from random import randrange

pic_folder = os.path.join(sys.path[0], 'QR activos')


def Civica(update, context):
    foto_path = os.path.join(pic_folder, 'CIVICA')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)


def Aulari(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'QR activos')
    foto_path = os.path.join(foto_path, 'MED')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)


def Carpa(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'Carpa letras')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)


def Comunicacio(update, context):
    foto_path = os.path.join(pic_folder, 'COM')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)


def Edifici_B_central(update, context):
    foto_path = os.path.join(pic_folder, 'BCEN')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)


def Edifici_B_Nord(update, context):
    foto_path = os.path.join(pic_folder, 'BNORD')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)


def Edifici_B_Sud(update, context):
    foto_path = os.path.join(pic_folder, 'BSUD')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)


def Edifici_C(update, context):
    foto_path = os.path.join(pic_folder, 'Ciencies')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)


def Educacio(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'Educació')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)


def Etse(update, context):
    foto_path = os.path.join(pic_folder, 'ETSE')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)


def FTI(update, context):
    foto_path = os.path.join(pic_folder, 'FTI')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)


def Medicina(update, context):
    foto_path = os.path.join(pic_folder, 'MED')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)


def SAF(update, context):
    foto_path = os.path.join(pic_folder, 'SAF')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)


def Torres(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'Torres Applus')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)


def Veterinaria(update, context):
    foto_path = os.path.join(pic_folder, 'VET')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)