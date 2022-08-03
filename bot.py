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
        bot.reply_to(message, "you need to specify the address after command")
    else:
    #проверяем аргумент на валидность
        pattern = re.compile("^((?:\/\/)?)?\w+(?:[-.]\w+)+(?:\/)*$")
        if pattern.match(site[0]):
            return(site[0])
        else:
            #аргумент невалиден
            bot.reply_to(message, "address is not valid")
            return False

def is_file_empty(file_name):
    try:
        with open(file_name, 'r') as read_obj:
         one_char = read_obj.read(1)
         if one_char:
            return False
    except OSError:
        bot.reply_to(message, "unable to open a list file")
    return True

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if isAdmin(message):
        bot.reply_to(message, """available commands: 
"/add google.com"       - add google.com to unblock list
"/remove google.com"    - remove google.com from unblock list
"/list                  - list unblocked hosts
        """)

@bot.message_handler(func=lambda message: message.text is not None and '/start' not in message.text)
def main(message):
    if isAdmin(message):
        if message.text.startswith('/add'):
            site = extract_arg(message.text)
            if urlValidator(message, site):
                #добавляем наш сайт в файл
                try:
                    with open(cfg.hostlist, 'a+') as file:
                        file.seek(0)
                        content = file.read()
                        if site[0] not in content:
                            file.write(site[0] + '\n')                           
                            bot.reply_to(message, "address: " + site[0] + " added")
                        else:
                            bot.reply_to(message, "address " + site[0] + " is already added")
                    file.close()
                except OSError:
                    bot.reply_to(message, "unable to open a list file")


        elif message.text.startswith('/remove'):
            site = extract_arg(message.text)
            if urlValidator(message, site):
                if not is_file_empty(cfg.hostlist):
                    try:
                        with open(cfg.hostlist, 'r+') as f:
                            lines = f.readlines()
                            f.close()
                            with open(cfg.hostlist, 'w') as f:
                                for line in lines:
                                    if site[0] not in line:
                                        f.write(line)
                            f.close()  
                            bot.reply_to(message, "Site " + site[0] + " removed")
                    except OSError:
                        bot.reply_to(message, "unable to open a list file")
                else:
                    bot.reply_to(message, "file is empty, nothing to delete")


        elif message.text.startswith('/list'):
            #выводим список хостов
            if not is_file_empty(cfg.hostlist):
                try:
                    with open(cfg.hostlist, 'r') as f:
                        hostslist = f.read()
                        f.close()
                        bot.reply_to(message, hostslist)
                except OSError:
                    bot.reply_to(message, "unable to open a list file")           
            else:
                bot.reply_to(message, "file is empty")


        elif message.text.startswith('/status'):
            #выводим список хостов
            bot.reply_to(message, "Надо придумать статусы на основные сервисы")
        else:
            bot.reply_to(message, "Unknown command")

# ------------------#
bot.polling(True)