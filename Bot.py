#coding: utf-8
import sys, os, telebot, urllib2,

__author__ = "Daniel Yohan"
__copyright__ = "Copyright 2017"
__credits__ = ["dyohan9", "eternnoir"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Daniel Yohan"
__email__ = "dyohan9@gmail.com"
__status__ = "Testing"
"""
    Library used: https://github.com/eternnoir/pyTelegramBotAPI
"""


bot = telebot.TeleBot("TOKEN")
config = {}

@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if m.chat.username in config["ranks"]["users"]:
        bot.send_message(cid, "Olá %s, vamos iniciar?\nDigite /help para saber os comandos disponíveis." %(str(m.chat.first_name)+" "+str(m.chat.last_name)))
    else:
        bot.send_message(cid, "Você não tem permissão para usar esse comando.")

@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    if m.chat.username in config["ranks"]["users"]:
        help = "Olá "+str(m.chat.first_name)+", eu posso ajudá-lo a baixar filmes.\n"+\
               "\n"+\
               "Você pode me controlar enviando esses comandos:\n"+\
               "\n"+\
               "/baixar <nome>#<url>\n"+\
               "/baixar <nome>#<url>#<extensão>\n\n"+\
               "Exemplo:\n/baixar Transformers#http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4\n\n"+\
               "Exemplo:\n/baixar Transformers#http://clips.vorwaerts-gmbh.de/big_buck_bunny#mp4"+\
               "\n\n"+\
               "Configurações do Bot\n"+\
               "/addadmin <usuário> - Permite que um usuário adiciona outros administradores\n"+\
               "/adduser <usuário> - Adiciona um novo usuário\n"+\
               "/removeuser <usuário> - Remove um usuário\n"+\
               "/removeadmin <usuário> - Remove um administrador"
               
        bot.send_message(cid, help)
    else:
        bot.send_message(cid, "Você não tem permissão para usar esse comando.")

@bot.message_handler(commands=['adduser', 'addadmin', 'addadmins'])
def commandPermission(m):
    cid = m.chat.id
    if m.chat.username in config["ranks"]["admins"]:
        command = m.text.replace("/", "").split(" ")[0]
        user = m.text[9:]
        if command == "adduser":
            if not user in config["ranks"]["users"]:
                config["ranks"]["users"].append(str(user))
                f = open('config.json', 'wb')
                f.write(json.dumps(config, indent=4, sort_keys=True))
                f.close()
            else:
                bot.send_message(cid, "Esse usuário já existe.")
        elif command == "addadmin" or command == "addadmins":
            user = user.replace(" ", "")
            if not user in config["ranks"]["users"]:
                config["ranks"]["users"].append(str(user))
            if not user in config["ranks"]["admins"]:
                config["ranks"]["admins"].append(str(user))
                f = open('config.json', 'wb')
                f.write(json.dumps(config, indent=4, sort_keys=True))
                f.close()
            else:
                bot.send_message(cid, "Esse usuário já existe.")
    else:
        bot.send_message(cid, "Você não tem permissão para usar esse comando.")

@bot.message_handler(commands=['removeuser', 'removeadmin'])
def commandPermission(m):
    cid = m.chat.id
    if m.chat.username in config["ranks"]["admins"]:
        command = m.text.replace("/", "").split(" ")[0]
        try:
            user = str(m.text.split(" ")[1])
        except:
            return bot.send_message(cid, "Este comando está faltando parametros, digite /help para mais informações.")
        count = 0
        found = False
        
        if command == "removeuser":
            for i in config["ranks"]["users"]:
                if i == user:
                    del config["ranks"]["users"][count]
                    found = True
                    break
                count += 1
            count = 0
            for b in config["ranks"]["admins"]:
                if b == user:
                    del config["ranks"]["admins"][count]
                    break
                count += 1
                
        elif command == "removeadmin":
            for i in config["ranks"]["admins"]:
                if i == user:
                    del config["ranks"]["admins"][count]
                    found = True
                    break
                count += 1
        f = open('config.json', 'wb')
        f.write(json.dumps(config, indent=4, sort_keys=True))
        f.close()
        if found:
            bot.send_message(cid, "Usuário "+str(user)+" foi removido com sucesso.")
        else:
            bot.send_message(cid, "Usuário "+str(user)+" não encontrado.")

def errorDownload(cid):
    bot.send_message(cid, "Não foi identificado a extensão do video\n"+\
                         "defina manualmente a extensão\n"+\
                         "/baixar <nome>#<url>\n"+\
                         "/baixar <nome>#<url>#<extensão>\n\n"+\
                         "Exemplo:\n/baixar Transformers#http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4\n\n"+\
                         "Exemplo:\n/baixar Transformers#http://clips.vorwaerts-gmbh.de/big_buck_bunny#mp4")

@bot.message_handler(commands=['baixar'])
def downloader(message):
    cid = message.chat.id
    if message.chat.username in config["ranks"]["users"]:
        try:
            nome = message.text[8:].split("#")[0]
            url = message.text[8:].split("#")[1]
        except:
            errorDownload(cid)
            return
        try:
            extension = message.text[8:].split("#")[2]
        except: 
            extension = url[-10:].lower().split(".")
            extension = extension[len(extension)-1]
        
        if extension in config["extensions"]:
            try:
                rsp = urllib2.urlopen(str(url))
                
            except:
                rsp = urllib2.urlopen(str(url+"."+str(extension)))
                
            dir = config["directory"]+str(nome.lower().replace(" ", "-"))

            if not os.path.exists(dir):
                os.makedirs(dir)
            else:
                return bot.send_message(cid, "Já existe um filme com o nome de "+str(nome)+"!")
            
            with open(dir+"/"+str(nome)+str("."+extension),'wb') as f:
                f.write(rsp.read())
            bot.send_message(cid, "Filme "+str(nome)+" baixado com sucesso.")
        else:
            errorDownload(cid)
         
    else:
        bot.send_message(cid, "Você não tem permissão para usar esse comando.")

if __name__ == "__main__":
    title = "\nTelegram Bot for Plex - Media Center"
    if sys.platform.startswith('win'):
        os.system("title "+title)
    print title+" Iniciado"
    with open("config.json", "r") as f:
        config = eval(f.read())
    bot.polling()
