import telebot
import requests
import json
from telebot import types
import time

token = '6547783651:AAHQQhrK-ntNrqYZklnB0-CDwxZyjJu6vEU'
bot = telebot.TeleBot(token)

password1 = ""
email1 = ""

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    reply_message = f"""
    ╔━━━━━🧟‍♂WELCOME🧟‍♂━━━━━━╗

  💃𝐇𝐢 {first_name} 𝐢𝐧 𝐦𝐲 𝐁𝐨𝐭🥶
  
       🍀𝐂𝐨𝐥𝐥𝐞𝐜𝐭 𝐂𝐨𝐢𝐧 𝐗𝐏𝐑 𝐅𝐫𝐞𝐞🍀
       
 𝐓𝐨 𝐂𝐨𝐥𝐥𝐞𝐜𝐭 𝐗𝐑𝐏 𝐂𝐥𝐢𝐜𝐤 ⚡ᴄᴏʟʟᴇᴄᴛ    
 𝐓𝐨 𝐂𝐨𝐥𝐥𝐞𝐜𝐭 𝐗𝐑𝐏 𝐂𝐥𝐢𝐜𝐤  ♻️ᴡɪᴛʜᴅʀᴀᴡ    
 𝐓𝐨 𝐂𝐨𝐥𝐥𝐞𝐜𝐭 𝐗𝐑𝐏 𝐂𝐥𝐢𝐜𝐤 💲ʏᴏᴜʀ ʙᴀʟᴀɴᴄᴇ 
       
  [♻️] 𝗕𝗢𝗧 𝗕𝘆 @l_FOX_I★👑★
  
  
╚━━━━━━━━━👑👑━━━━━━━━━╝ """.format(first_name=first_name)

    L7N6 = types.InlineKeyboardButton(text="⚡ᴄᴏʟʟᴇᴄᴛ", callback_data="L7Nfoxcollect")
    L7N1 = types.InlineKeyboardButton(text="Dev🐉", url="https://t.me/F_0_oX")
    L7N2 = types.InlineKeyboardButton(text="♻️ᴡɪᴛʜᴅʀᴀᴡ", callback_data="L7Nfoxr")
    L7N3 = types.InlineKeyboardButton(text="💲ʏᴏᴜʀ ʙᴀʟᴀɴᴄᴇ", callback_data="L7Nbonce")
    L7N4 = types.InlineKeyboardButton(text="stop🛑", callback_data="L7Nstop")
    
    L7N_ = types.InlineKeyboardMarkup()
    L7N_.row_width = 3
    L7N_.add(L7N6)
    L7N_.add(L7N1)
    L7N_.add(L7N4)
    
    bot.send_message(message.chat.id, reply_message, reply_markup=L7N_)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    message = call.message
    if call.data == "L7Nfoxcollect":
        bot.send_message(message.chat.id, "Please enter your Gmail:")
        bot.register_next_step_handler(message, get_gmail)

def get_gmail(message):
    global email1
    email1 = message.text
    bot.send_message(message.chat.id, "Please enter your password:")
    bot.register_next_step_handler(message, get_password)

def get_password(message):
    global password1
    password1 = message.text
    execute_script(message)

def execute_script(message):
    global email1, password1
    
    headers1 = {
        'authority': 'faucetearner.org',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6',
        'content-type': 'application/json',
        'origin': 'https://faucetearner.org',
        'referer': 'https://faucetearner.org/login.php',
        'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params1 = {
        'act': 'login',
    }

    json_data1 = {
        'email': email1,
        'password': password1,
    }

    response1 = requests.post('https://faucetearner.org/api.php', params=params1, headers=headers1, json=json_data1)
    if "Login successful" in response1.text:
        sufi1 = response1.cookies.get_dict()
        user_photo = bot.get_user_profile_photos(message.from_user.id, limit=1).photos
        if user_photo:
            photo_file_id = user_photo[0][0].file_id
            bot.send_photo(message.chat.id, photo_file_id, caption='''🐍جاري تجميع عمله XPR🔥''', parse_mode='MarkdownV2')
            execute_faucet(message, sufi1)
    elif "wrong username or password" in response1.text:
        bot.send_message(message.chat.id,'''الجميل أو الباسورد خطاء 
برجاء ادخال الجميل الصحيح مره اخر 👇''')
        bot.register_next_step_handler(message, get_gmail)
    else:
        bot.send_message(message.chat.id, "حدث خطأ غير متوقع. يرجى المحاولة مرة أخرى.")
        bot.register_next_step_handler(message, get_gmail)

def execute_faucet(message, sufi1):
    while True:
        start_time = time.time()
        headers = {
            'authority': 'faucetearner.org',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6',
            'origin': 'https://faucetearner.org',
            'referer': 'https://faucetearner.org/faucet.php',
            'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        params = {
            'act': 'faucet',
        }

        rr = requests.post('https://faucetearner.org/api.php', params=params, cookies=sufi1, headers=headers).text
        if 'Congratulations on receiving' in rr:
            json_data = json.loads(rr)
            message_text = json_data["message"]
            start_index = message_text.find(">") + 1
            end_index = message_text.find(" ", start_index)
            balance = message_text[start_index:end_index]
            bot.send_message(message.chat.id, f"  تم اضافه {balance} XRP£.")
        elif 'You have already claimed, please wait for the next wave!' in rr:
            bot.send_message(message.chat.id, "الرجاء الانتظار حتى ينتهي الوقت!!!🧚.")
        else:
            bot.send_message(message.chat.id, "حدث خطأ غير متوقع. يرجى المحاولة مرة أخرى.")

        elapsed_time = time.time() - start_time
        remaining_time = 60 - elapsed_time
        if remaining_time > 0:
            time.sleep(remaining_time)

print('Bot يعمل الآن')
bot.infinity_polling()
    
