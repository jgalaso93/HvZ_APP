import sys
import os
from random import randrange

pic_folder = os.path.join(sys.path[0], 'QR activos')


def send_pic(update, done_pics, folder_path):
    pics_in_folder = os.listdir(folder_path)
    pics_aviable = []
    for p in pics_in_folder:
        if p in done_pics.values():
            pass
        else:
            pics_aviable.append(p)

    number_of_photos = len(pics_aviable)
    if number_of_photos == 0:
        update.message.reply_text("No et queden missions en aquesta zona!")
        return None
    else:
        index = randrange(number_of_photos)
        final_foto_path = os.path.join(folder_path, pics_aviable[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)


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


def Comunicacio_ext(update, context, done_pics):
    foto_path = os.path.join(pic_folder, 'COM')
    send_pic(update, done_pics, foto_path)


def Edifici_B_central_ext(update, context, done_pics):
    foto_path = os.path.join(pic_folder, 'BCEN')
    send_pic(update, done_pics, foto_path)


def Edifici_B_Nord_ext(update, context, done_pics):
    foto_path = os.path.join(pic_folder, 'BNORD')
    send_pic(update, done_pics, foto_path)


def Edifici_B_Sud_ext(update, context, done_pics):
    foto_path = os.path.join(pic_folder, 'BSUD')
    send_pic(update, done_pics, foto_path)


def Edifici_C_ext(update, context, done_pics):
    foto_path = os.path.join(pic_folder, 'Ciencies')
    send_pic(update, done_pics, foto_path)


def Educacio(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'Educació')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)


def Etse_ext(update, context, done_pics):
    foto_path = os.path.join(pic_folder, 'ETSE')
    send_pic(update, done_pics, foto_path)


def FTI_ext(update, context, done_pics):
    foto_path = os.path.join(pic_folder, 'FTI')
    send_pic(update, done_pics, foto_path)


def Medicina_ext(update, context, done_pics):
    foto_path = os.path.join(pic_folder, 'MED')
    send_pic(update, done_pics, foto_path)


def SAF_ext(update, context, done_pics):
    foto_path = os.path.join(pic_folder, 'SAF')
    send_pic(update, done_pics, foto_path)


def Torres(update, context):
    foto_path = sys.path[0]
    foto_path = os.path.join(foto_path, 'Fotos de llocs a la uab')
    foto_path = os.path.join(foto_path, 'Torres Applus')
    number_of_photos = len(os.listdir(foto_path))
    index = randrange(number_of_photos)
    final_foto_path = os.path.join(foto_path, os.listdir(foto_path)[index])
    with open(final_foto_path, 'rb') as f:
        update.message.reply_photo(f)


def Veterinaria_ext(update, context, done_pics):
    foto_path = os.path.join(pic_folder, 'VET')
    send_pic(update, done_pics, foto_path)