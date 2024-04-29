
import telebot
from telebot import types
import marshal
import base64
import traceback

TOKEN = '6819299969:AAGxYhFYZhEN_wpAgCxbT4DcfpbnmD5Zs0c'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    try:
        if bot.get_chat_member("@cardsrmaden", message.from_user.id).status == "left":
            den = types.InlineKeyboardButton('my channel', url='t.me/cardsrmaden')
            kc = types.InlineKeyboardMarkup(row_width=2);kc.add(den)
            return bot.send_message(message.chat.id, '''<strong>
            عذرا عزيزي 📛
             عليك الاشتراك بقناة المطور و قناة البوت فضلا
            ليصلك كل جديد✨
             </strong>
              ''', parse_mode='html', reply_markup=kc)
    except AttributeError:
        pass
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton('تشفير كود', callback_data='encrypt_message'),
               types.InlineKeyboardButton('فك تشفير كود', callback_data='decrypt_message'))
    markup.row(types.InlineKeyboardButton('تشفير ملف', callback_data='encrypt_file'),
               types.InlineKeyboardButton('فك تشفير ملف', callback_data='decrypt_file'))
    markup.row(types.InlineKeyboardButton('تصحيح الأخطاء', callback_data='fix_errors'))

    bot.send_message(message.chat.id, "مرحبًا! بك عزيزي المستخدم 🤍 \n\n※ انا بوت تشفير وفك تشفير ويفي🌊 \n※ يمكنك تشفير وفك تشفير كود 🈲\n※ يمكنك تشفير وفك تشفير ملف 📂\n※ التشفيرات المدعومه <[ Base64 - Marshal ]>🖇\n※ ايضا يمكنك تصحيح الاخطاء 👨‍🔧:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'encrypt_message':
        bot.send_message(call.message.chat.id, "ارسل الكود اللي عاوز تشفره 🈲.")
    elif call.data == 'decrypt_message':
        bot.send_message(call.message.chat.id, "ارسل الكود اللي عاوز تفك تشفيره 🈲.")
    elif call.data == 'encrypt_file':
        bot.send_message(call.message.chat.id, "أرسل الملف اللي عاوز تشفره 📂.")
    elif call.data == 'decrypt_file':
        bot.send_message(call.message.chat.id, "أرسل الملف اللي عاوز تفك تشفيره 📂.")
    elif call.data == 'fix_errors':
        bot.send_message(call.message.chat.id, "أرسل الملف اللي عاوز تصحح أخطائه 👨‍🔧.")

@bot.message_handler(commands=['encrypt'])
def encrypt_message(message):
    try:
        content = message.text.split(' ', 1)[1]
        if content.endswith('.py'):
            with open(content, 'rb') as file:
                data = file.read()
                encoded = base64.b64encode(marshal.dumps(data))
                bot.reply_to(message, "الملف المشفر : {}".format(encoded.decode('utf-8')))
        else:
            encoded = base64.b64encode(marshal.dumps(content.encode('utf-8')))
            bot.reply_to(message, "الكود المشفرة\n : {}".format(encoded.decode('utf-8')))
    except IndexError:
        bot.reply_to(message, "Usage: /encrypt <message_or_file.py>")

@bot.message_handler(commands=['decrypt'])
def decrypt_message(message):
    try:
        content = message.text.split(' ', 1)[1]
        decoded = marshal.loads(base64.b64decode(content.encode('utf-8')))
        if decoded.endswith(b'.py'):
            with open('decrypted_file.py', 'wb') as file:
                file.write(decoded)
            bot.reply_to(message, "تم فك تشفير الملف بنجاح ✅.")
        else:
            bot.reply_to(message, "الكود المفكوك :\n {}".format(decoded.decode('utf-8')))
    except IndexError:
        bot.reply_to(message, "Usage: /decrypt <encrypted_message_or_file>")

@bot.message_handler(commands=['fix_errors'])
def fix_errors(message):
    try:
        content = message.text.split(' ', 1)[1]
        with open(content, 'r') as file:
            code = file.read()
            compiled_code = compile(code, '<string>', 'exec')
        bot.reply_to(message, "مفيش اخطاء في الكود ✅.")
    except SyntaxError:
        error_message = traceback.format_exc()
        bot.reply_to(message, "الخطأ اللي في الكود:\n{}".format(error_message))

bot.polling()
