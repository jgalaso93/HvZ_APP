import telegram
from utils.helpers import check_is_founder


def contact(update, context):
    output_text = """Contacta con el Mod correspondiente según tu problema:

- *Problemas o dudas con el bot:* @ShaggyGalaso
- *Problemas con los QR:* @Nelaso
- *Problemas con la misión:* @Janadsb99
- *Problemas fuera del campus:* @AlexNevado
- *Dudas de normas:* @Sargento\_Zorro
- *Dudas de telegram:* @GuillemMoya
- *Problemas con otros jugadores:* @mar\_clua
- *Problemas por discriminación:* @AiHysteric"""
    update.message.reply_text(output_text, parse_mode=telegram.ParseMode.MARKDOWN)


def help_mod_ext(update, context, data):
    user_id = str(update.message.chat['id'])

    level = str(data[data['BOT_ID'] == user_id]['Level'].values[0])
    if level != 'Mod':
        update.message.reply_text("Només els mods poden fer servir aquesta comanda!!")
        return None

    output_text = """💬 *COMANDOS DE SOLO MODS:*
-*/generaltop*: Muestra el top 10 de las dos facciones. Se puede añadir un numero para que sea el top ese numero

-*/activate + user_id, mission_id*: Le activa a ese usuario esa mission

-*/complete + user_id, mission_id*: Le hace esa mision a esa persona

-*/donebyuser + user_id*: Te dice todas las misiones que ha hecho esa persona 

-*/onduty + user_id*: Te dice todas las misiones activas de esa persona

-*/addpoints + user_id, puntos*: Le suma a ese usuario tantos puntos

-*/sendtoplayer + user_id, texto*: Manda el texto a ese usuario

-*/messageall + texto*: Le manda a todos los jugadores ese texto

-*/allmissionstats*: Muestra los stats de todas las misiones

-*/allanomalisstats*: Muestra los stats de todas las misiones

-*/allcorruptusstats*: Muestra los stats de todas las misiones

-*/influencestats*: Muestra el estado de influencia de todos los NPCS

-*/refreshinfluence*: Refresca en la base de datos la influencia calculada"""
    update.message.reply_text(output_text, parse_mode=telegram.ParseMode.MARKDOWN)


def rules(update, context):
    output_text = """*NORMAS:*
_Con tal de garantizar que TIME ESCAPE sea un juego divertido para todes, deberéis seguir la siguiente normativa_.

😷 En TIME ESCAPE respetaremos las medidas vigentes del Procicat y sus medidas para protegernos de la Covid-19.

❌ *No arranques QRs*: arrancar un QR será penalizado con la inmediata expulsión del juego.

❌ *No hagas spoilers*: revelar la ubicación de un QR o la solución de una misión por el grupo será penalizado con la expulsión del jugador en dicho grupo. _Esta norma no se aplica si se trata de tu equipo_.

❌ *No compartas el QR*: si una misma imagen se sube 2 veces, nuestro Bot todo poderoso lo sabrá y dicha imagen quedará inutilizada.

💕 *Treat people with kindness*: los demás jugadores (corruptus o anomalis), los moderadores (los de la bandana roja en la pierna) y las personas no jugadoras del campus merecen ser tratadas con respeto. El mobiliario y las instalaciones de la UAB también.

💕 *Stay safe*: todas las misiones se encuentran en sitios accesibles. No hagais burradas.

🛡️ *Escudos*: en TIME ESCAPE los escudos estan permitidos.


Y, para terminar...
✨ *NO SEAIS IDIOTES* ✨"""
    update.message.reply_text(output_text, parse_mode=telegram.ParseMode.MARKDOWN)


def use(update, context):
    output_text = """HOLA JUGADOR!!👋🏼
👀Leeme atentamente para saber cómo jugar a TIME ESCAPE y ganar puntos para tu facción.

*1. Encuentra un QR*
Ve por el campus y busca por todas partes hasta que veas un codigo QR.

*2. Hazle una foto*
Haz una foto del QR y mándamela por aquí. Puedes sacar la foto directamente desde este chat.

*3. Recibe la misión*
Después de asegurarme de que tu foto sea original, leeré el QR y te mandaré tu misión. 
⚠️ ¡Paciencia! Sóis muchos jugando y puede que me bloquee un poco. 
_Si en el momento no puedes realizar la misión, simpre podrás volver a ella usando el comando /activity_.

*4. Resuelve la misión*
Responde a la misión por este chat. Si tu respuesta es correcta, ganarás puntos para tu facción💪🏿

*5. Vuelta a empezar*
Repite este proceso con todos los QRs que encuentres para acumular puntos y cambiar la historia."""
    update.message.reply_text(output_text, parse_mode=telegram.ParseMode.MARKDOWN)


def help(update, context):
    """Send a message when the command /help is issued."""
    output_text = """Para ver los comandos basicos pulsa en:
💬 *BÁSICOS: /help_basic*

💬 *COMPETITIVOS: /help_competitive*

💬 *PERSONALIZADOS: /help_personal*

💬 *DE EQUIPO: /help_team*

⚠️ *REPORTAR UN PROBLEMA:* /report + El problema"""
    update.message.reply_text(output_text, parse_mode=telegram.ParseMode.MARKDOWN)


def help_founder_ext(update, context, teams_data):
    bot_id = str(update.message.chat['id'])
    if check_is_founder(bot_id, teams_data):
        output_text = """💬 *DE FUNDADORAS DE EQUIPO:*

- */promote + "alias", "rango"*: para otorgar cargos dentro del equipo. _Ejemplo: /promote antonio, veterano_.

-*/kick + user_id*: Elimina la persona con ese id de tu equipo

-*/admit + user_id*: Admite a la persona con ese id a tu equipo

-*/decline + user_id*: Rechaza a la persona con ese id de tu equipo

-*/memberids*: Lista IDs, alias i rangos de todas las personas miembro

-*/requestsids*: Lista IDs i alias de todas las personas que estan pendientes de aprobación para entrar"""
        update.message.reply_text(output_text, parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        update.message.reply_text("No has fundat cap equip, no pots usar aquesta comanda!")


def help_team(update, context):
    output_text = """💬 *DE EQUIPO:* Los equipos sirven para jugar con tus amigos y acumular puntos.

- */createteam + "nombre"*: para ser la fundadora de un equipo. _Ejemplo: /createteam HvZ_

- */jointeam + "nombre"*: para unirte a un equipo que ya exista. _Ejemplo: /jointeam HvZ_

- */showteam*: para obtener el ranking de tu equipo.

- */sendboop + "alias"*: mandar un boop a alguien con ese alias que esté en tu equipo. Boop!

- */sendall + "mensaje"*: mandar un mensaje a todo el mundo de tu equipo

- */help_founder*: Comandos que solo los fundadores pueden usar"""
    update.message.reply_text(output_text, parse_mode=telegram.ParseMode.MARKDOWN)


def help_personal(update, context):
    output_text ="""💬 *PERSONALIZADOS:*
- */setalias + "el nombre de tu elección"*: para cambiar tu alias de registro. _Ejemplo: /setalias TimeEscapeBot_.

- */stats*: para conocer tus logros dentro del juego.

- */activity*: para saber las misiones activas que te quedan por resolver.

- */hint + "id de la misión"*: para obtener una pista de la misión. _Ejemplo: /hint C1_

- */join + "facción"*: para unirte a tu facción. _Ejemplos: /joinanomalis o /joincorruptus_ 

- */donebyme*: para ver que missiones has hecho

- */boop o /meow o /ribbit o /pok o /ardillita*: El bot te mandará un boop! o un meow! o un ribbit! o un pok! o ponerte sad!"""
    update.message.reply_text(output_text, parse_mode=telegram.ParseMode.MARKDOWN)


def help_competitive(update, context):
    output_text = """💬 *COMPETITIVOS:*
- */top3*: muestar la puntuación de los 3 jugadores con mayor puntuación

- */topfaction*: muestra el top de vuestra facción. Para entrar en el top requiere alias y más de 0 puntos

- */topteams*: mustra el top 10 de los equipos registrados.

- */talk*: muestra los NPCS con los que puedes hablar. Pon el nombre seguido de talk para hablar con algun en particular"""
    update.message.reply_text(output_text, parse_mode=telegram.ParseMode.MARKDOWN)


def help_basic(update, context):
    output_text = """💬 *BÁSICOS:*
- */start:* para recordar la información inicial.

- */rules:* para saber las normas del juego

- */help*: para volver a ver esta información.

- */use:* para obtener un tutorial de las misiones. 

- */getmyid:* para obtener tu ID, el número de identificación como jugador.

- */missions*: para saber dónde puedes encontrar misiones. 

- */contact*: si tienes dudas o problemas usa este comando para contactarnos!"""
    update.message.reply_text(output_text, parse_mode=telegram.ParseMode.MARKDOWN)


def start_ext(update, context):
    """Send a message when the command /start is issued."""
    bot_id = str(update.message.chat['id'])
    output_text = """Hola, ¡soy el bot que os va a estar ayudando esta edición!

Os voy a hacer un pequeño resumen de como usarme, no os preocupéis, ¡es muy fácil!

Para registraros, el formulario de inscripción os pedirá el ID, tu ID es: {}. Para tener vuestro ID con un formato fácil de copiar, escribid /getmyid. Si no sabes de qué formulario te hablo, sigue este link: https://bit.ly/3meBpHL

Si tenéis cualquier duda sobre qué comandos utilizar, escribid /help. Allí os explicaré los comandos principales que tengo y como usarlos. 

Si queréis saber como funcionan las normas, escribid /use. Allí os explicaré como hacer y resolver las misiones. 

Si tenéis dudas que yo no os pueda responder, escribid /contact. Allí os pasaremos el contacto de algún moderador que os podrá resolver la duda personalmente. 

Si queréis volver a leer este mensaje en algún momento, escribid /start. 

No hace falta que siempre escribáis los comandos, podéis pulsar encima del comando y se activará automáticamente. 

Por último, si ya sabéis a qué Facción pertenecéis, usad el comando /joincorruptus o /joinanomalis. 

¡Muchas gracias por participar, a jugar!""".format(bot_id)
    update.message.reply_text(output_text)