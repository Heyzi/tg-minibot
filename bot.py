import telebot
import re
import config as cfg

bot = telebot.TeleBot(cfg.TOKEN)

def extract_arg(arg):
    return arg.split()[1:]

def isAdmin(message):
    if message.from_user.username in cfg.admins:
        return True

def urlValidator(message, site):
        #если аргументов нет
    if not site:
        bot.reply_to(message, "No url added")
    else:
    #проверяем аргумент на валидность
        pattern = re.compile("^((?:\/\/)?)?\w+(?:[-.]\w+)+(?:\/)*$")
        if pattern.match(site[0]):
            return(site[0])
        else:
            #аргумент невалиден
            bot.reply_to(message, "URL format incorrect")
            return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if isAdmin(message):
        bot.reply_to(message, """Примеры команд: 
"/add google.com"       - добавить google.com
"/remove google.com"    - удалить google.com
"/list                  - вывести список хостов
        """)

@bot.message_handler(func=lambda message: message.text is not None and '/start' not in message.text)
def main(message):
    if isAdmin(message):
        if message.text.startswith('/add'):
            site = extract_arg(message.text)
            if urlValidator(message, site):
                #дописать часть на добавление
                bot.reply_to(message, "URL added: " + site[0])

        elif message.text.startswith('/remove'):
            site = extract_arg(message.text)
            if urlValidator(message, site):
                #дописать часть на удаление
                bot.reply_to(message, "URL removed: " + site[0])
            
        elif message.text.startswith('/list'):
            #выводим список хостов
            try:
                with open(cfg.hostlist, 'r') as f:
                    hostslist = f.read()
                    f.close()
                    bot.reply_to(message, hostslist)
            except OSError:
                bot.reply_to(message, "Cant open host file")

        elif message.text.startswith('/status'):
            #выводим список хостов
            bot.reply_to(message, "Надо придумать статусы на основные сервисы")

        else:
            bot.reply_to(message, "Unknown command")

# ------------------#
bot.polling(True)