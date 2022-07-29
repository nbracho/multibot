#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""Simple inline keyboard bot with multiple CallbackQueryHandlers.

This Bot uses the Application class to handle the bot.
First, a few callback functions are defined as callback query handler. Then, those functions are
passed to the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot that uses inline keyboard that has multiple CallbackQueryHandlers arranged in a
ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line to stop the bot.
"""
import logging
from pickle import FALSE, TRUE
import mysql.connector
import re

from telegram import __version__ as TG_VER
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Stages
START_ROUTES, END_ROUTES = range(2)
# Callback data
ATRAS, GARANTIAS, CATALOGOS, ADELANTE, TIPO= range(5)

indicador=0
contador=1
ejecutar=1
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    #await update.message.reply_text("Bienvenid@ Soy tu Asesora Virtual de Ventas Selecciona una Opcion")
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [
            InlineKeyboardButton("Garantias", callback_data='GARANTIAS'),
    #        InlineKeyboardButton("Catalogos", callback_data='CATALOGOS'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    await update.message.reply_text("Bienvenid@ Soy tu Asesora Virtual de Ventas Selecciona una Opcion", reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return START_ROUTES


async def tipo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    if  1==1:       
        mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="garantias"
)
        num = re.findall('[0-9]+', query.data)
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT tipo.id, tipo.tipo, tipo.garantia FROM `tipo` WHERE tipo.id_marca = {num[0]}")
        myresult = mycursor.fetchall()

        keyboard= [[]]

        for x in myresult:
            keyboard[0].append(InlineKeyboardButton(x[0], callback_data="DD"+str(x[0])) )
        #keyboard[0].append(InlineKeyboardButton('>>', callback_data='ADELANTE'))

        

        text=f' Por Favor Seleccione Un Tipo de Garantia: \n'
        for x in myresult:
            text +=str(x[0]) + " "+x[1]+"\n"
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup) 
        
    return START_ROUTES

async def detalle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    if  1==1:       
        mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="garantias"
)
        num = re.findall('[0-9]+', query.data)
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT marcas.nombre, tipo.tipo, tipo.garantia FROM tipo INNER JOIN marcas ON marcas.id = tipo.id_marca WHERE tipo.id = {num[0]}")
        myresult = mycursor.fetchall()

        keyboard= [[]]

        for x in myresult:
            text=f'Marca: '+str(x[0])+'\n Tipo: '+str(x[1])+'\n Garantia: '+str(x[2])
        keyboard[0].append(InlineKeyboardButton("Volver", callback_data="VOLVER") )

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup) 
        
    return START_ROUTES

async def garantias(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="garantias"
)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM marcas LIMIT 0, 5")
    myresult = mycursor.fetchall()
    
    

    # Get CallbackQuery from Update
    query = update.callback_query
  
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery

    await query.answer()
    keyboard= [[]]
    for x in myresult:
        keyboard[0].append(InlineKeyboardButton(x[0], callback_data="TT"+str(x[0])) )
    keyboard[0].append(InlineKeyboardButton('>>', callback_data='ADELANTE'))

        

    text='  Por Favor Seleccione Una Marca: \n O Escriba El Nombre para Buscarla \n'
    for x in myresult:
        text +=str(x[0]) + " "+x[1]+"\n"
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup) 
    return END_ROUTES

async def catalogos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="garantias"
)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM marcas LIMIT 0, 5")
    myresult = mycursor.fetchall()
    
    

    # Get CallbackQuery from Update
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    keyboard= [[]]
    i = 1
    for x in myresult:
        keyboard[0].append(InlineKeyboardButton(x[0], callback_data=str(i)) )
        i=i+1
    keyboard[0].append(InlineKeyboardButton('>>', callback_data='ADELANTE'))

        

    text='  Por Favor Seleccione Una Marca: \n O Escriba El Nombre para Buscarla \n'
    for x in myresult:
        text +=str(x[0]) + " "+x[1]+"\n"
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup) 
    return START_ROUTES

      







async def atras(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global indicador
    global contador
    mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="garantias"
)
    indicador=indicador-5
    contador=contador-1
    if indicador < 0:
        indicador = 0
        contador=1 
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM marcas LIMIT "+str(indicador)+", 5" )
    myresult = mycursor.fetchall()

    
    

    # Get CallbackQuery from Update
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    keyboard= [[InlineKeyboardButton('<<', callback_data='ATRAS')]]
    if indicador <= 0:
        keyboard= [[]]
    for x in myresult:
        keyboard[0].append(InlineKeyboardButton(x[0], callback_data='TT'+str(x[0])) )
    keyboard[0].append(InlineKeyboardButton('>>', callback_data='ADELANTE'))
    text='Seleccione Una Marca:\n Pagina: '+str(contador)+'   \n'
    for x in myresult:
        text +=str(x[0]) + " "+x[1]+"\n"
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup) 
    return START_ROUTES

async def adelante(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: #----------------------
    global indicador
    global contador
    mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="garantias"
)
    indicador+=5
    contador=contador+1
    mycursor = mydb.cursor()
    r=mycursor.execute("SELECT * FROM marcas LIMIT "+str(indicador)+", 5" )
    myresult = mycursor.fetchall()
    logger.info("arrojo  %s registros filtrados.", r)

async def buscar_marca(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: #----------------------#################################
    global contador
    mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="garantias"
)
    marca=update.message.text
    contador=contador+1
    mycursor = mydb.cursor()
    r=mycursor.execute(f"SELECT * FROM marcas where lower(nombre) like concat('%',lower('{marca}'),'%') LIMIT 0, 5" )
    myresult = mycursor.fetchall()
    logger.info("arrojo  %s registros filtrados.", r)   


    # Get CallbackQuery from Update
    query = update.callback_query

    #await query.answer()
    keyboard= [[]]
    for x in myresult:
        keyboard[0].append(InlineKeyboardButton(x[0], callback_data='TT'+str(x[0])) )
   
    
    text=''
    for x in myresult:
        text +=str(x[0]) + " "+x[1]+"\n"
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    await update.message.reply_text(
        "Resultados de la Busqueda: "+str(marca) + "\n " + text,
        reply_markup=reply_markup,
    )
    #await query.edit_message_text(text, reply_markup=reply_markup) 
    return START_ROUTES
#------------------------------------ fin del boton adelante ---------------------------------------------


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    query = update.callback_query
    #logger.info("User %s started the conversation.", user.first_name)
    #await update.message.reply_text("Bienvenid@ Soy tu Asesora Virtual de Ventas Selecciona una Opcion")
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [
            InlineKeyboardButton("Garantias", callback_data='GARANTIAS'),
#            InlineKeyboardButton("Catalogos", callback_data='CATALOGOS'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    await query.edit_message_text("Comencemos de Nuevo, Selecciona una Opcion", reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return START_ROUTES


 
def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5465994967:AAE-CFMmPSf8LOhflcRw_a1B8vUN0-2tr0I").build()

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(garantias, pattern="^GARANTIAS$"),
                CallbackQueryHandler(atras, pattern="^ATRAS$"),
                CallbackQueryHandler(adelante, pattern="^ADELANTE$"),
                CallbackQueryHandler(tipo, pattern="^TT[0-9]*$"),
                CallbackQueryHandler(detalle, pattern="^DD[0-9]*$"),
                CallbackQueryHandler(end, pattern="^VOLVER$"),
            ],
            END_ROUTES: [
                
    #            CallbackQueryHandler(end, pattern="^" + str(TWO) + "$"),
                MessageHandler(filters.TEXT,buscar_marca ),
                CallbackQueryHandler(tipo, pattern="^TT[0-9]*$"),
            ],

        },
        fallbacks=[CommandHandler("start", start)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()



if __name__ == "__main__":
    main()
