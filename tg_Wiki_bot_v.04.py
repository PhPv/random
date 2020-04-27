
import telebot
#import constants
import pypyodbc

mySQLServer = "dbwiki-eu-north-1b.c8t0n4npahtc.eu-north-1.rds.amazonaws.com,03306"
myDatabase = "CCWiki"

TOKEN = "704196414:AAEBBhNllaoHpKCosMFoOuzixq13C6ntwg4"
bot = telebot.TeleBot(TOKEN)
#bot = telebot.TeleBot(constants.token)

print(bot.get_me())

@bot.message_handler(commands =['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    user_markup.row('/start', '/stop')
    user_markup.row('btc', 'eth', 'ltc')
    bot.send_message(message.from_user.id, "Привет, введи интересующий тебя термин. Например: btc", reply_markup=user_markup)

@bot.message_handler(commands =['help'])
def handle_text(message):
    bot.send_message(message.from_user.id, "Привет! Я CryptoWiki_bot - вики-бот по теме криптовалют.\n "
                                           "Доступные комманды:\n "
                                           "Общий функционал:\n"
                                           "/start /help /stop\n"
                                           "Разделы: \n"
#                                           "/Tokens \n"
#                                           "/Personality \n"
#                                           "/Technologies \n"
                                           )


@bot.message_handler(commands =['stop'])
def handle_start(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, "Клавиатура убрана. ", reply_markup=hide_markup)
@bot.message_handler(content_types=['text'])
def text_handler(message):
    text = message.text.lower()
    chat_id = message.chat.id
    connection = pypyodbc.connect('Driver={SQL Server};'
                                  'Server=' + mySQLServer + ';'
                                  'Database=' + myDatabase + ';'
                                  'UID=' + 'dbWikiAdmin' + ';'
                                  'PWD=' + 'dbWikiPass' + ';')

    cursor = connection.cursor()

    mySQLQuery1 = """
                           SELECT Tid 
                           FROM CCWiki
                           WHERE Tname1=? OR Tname2=? OR Tname3=? OR Tname4=? OR Tname5=? OR Tname6=? OR Tname7=? OR Tname8=? OR Tname9=? OR Tname10=? 
                            """

    cursor.execute(mySQLQuery1, (text,text,text,text,text,text,text,text,text,text,))
    results1 = cursor.fetchall()
    if results1:
       for row in results1:
            Tid = row[0]
            mySQLQuery2 = """
                          SELECT Sdesc
                          FROM CCWiki
                          WHERE Tid=?
                    """

            cursor.execute(mySQLQuery2, (Tid,))
            results2 = cursor.fetchall()
            for row in results2:
                Sdesc = row[0]
                bot.send_message(chat_id, str(Sdesc))
    else:
        bot.send_message(chat_id, 'Извини, я тебя не понял :( Пожалуйста, переформулируй запрос.')
    connection.close()
bot.polling(none_stop=True, interval=0)

