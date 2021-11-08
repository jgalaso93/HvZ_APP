import logging
import telegram
from utils.animals import scrap_pics, image_sender
from random import randint
import pandas as pd
import os
import sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

conversation_db_file = 'D:\\Proyectos\\HvZ\\HvZ PvE\\HvZ_APP\\HappyNutrinsConversation.csv'
conver_data = pd.read_csv(conversation_db_file, sep=';', header=0, dtype={'BOT_ID': str}, encoding='cp1252')
talk_input = conver_data['INPUT'].tolist()
talk_output = conver_data['OUTPUT'].tolist()
talk = {k: v for k, v in zip(talk_input, talk_output)}


def start(update, context):
    output_text = """Bienvenida nutriiins!! (o quien sea que este mirando este bot.)
Vale, primero lo primero, *FELIIIIIZZZ CUMPLEAÑOS*, aun que puede que no estés mirando esto cuando sea tu cumple
Segundo, soy un bot, y mi creador piensa que es una chorrada y que puede que sea poca cosa pero yo te daré todo el amor que pueda :)
Luego, no sé contar pero puedo hacer cosas chachis, para saber más haz /help
Por último, eres preciosa y te mereces lo mejor del mundo mundial!!!!"""
    update.message.reply_text(output_text, parse_mode=telegram.ParseMode.MARKDOWN)


def ayuda(udpate, context):
    output_text = """Estas son todas las funciones que puedo hacer:
- /otter : Te dará una nutria :)
- /poema : Te dará el poema que te ha hecho tu nutrins bonita <3
    """
    udpate.message.reply_text(output_text, parse_mode=telegram.ParseMode.MARKDOWN)


def otter(update, context):
    urls = ['http://bit.ly/3pvmigD', 'http://bit.ly/3B6yLcD', 'http://bit.ly/3Gg4tI3']
    random_num = randint(0, (len(urls) - 1))
    pics = scrap_pics(urls[random_num])
    if pics:
        image_sender(update, pics)
    else:
        otter(update, context)


def poema(update, context):
    output_text = """Mira! Shaggy te ha escrito un poema:
    
Llévame de excursión
a donde dormir de la mano
sea tranquila pasión
La ira será siempre en vano

Nos mece el agua fluvial
Oniria nos acompaña al lago
tras la lluvia y todo el mal
No hay nada que sea aquel mal trago

Me parece bien verte a cualquier plazo
el clima tampoco es inconveniente
me basta si me refugia tu abrazo
o estar a tu lado y lo que se siente

En mi locura fuiste mi lazarillo
ahora no concibo vivir sin tu guía
Yo necesito frío y tu solo un cepillo
pero arrimamos el hombro cuando hay sequía

Bésame con el amor de un hermano
pues quiero acompañarte todo el camino
eres medicina con que me sano
y la llave de todo lo bueno que vino

https://www.instagram.com/p/CVUvDsxsZSg/"""
    update.message.reply_text(output_text)


def echo(update, context):
    """Check the message and act if it's an answer"""
    answer = update.message.text
    user_id = update.message.chat['id']
    if user_id < 0:
        return None

    if answer in talk.keys():
        update.message.reply_text(talk[answer])
    else:
        update.message.reply_text("No conozco lo que me dices, preuba otra cosas como \"te quiero\"")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    updater = Updater("1978438249:AAF6j4nfDYTCO8p26TGdOvKE6wiv1GKTP34", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", ayuda))
    dp.add_handler(CommandHandler("otter", otter))
    dp.add_handler(CommandHandler("poema", poema))

    # on noncommand i.e message - tree decision (WIP)
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()