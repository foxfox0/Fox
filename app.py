import telebot
import requests
import json
from telebot import types
from threading import Timer


token = '6992311911:AAEhc8HIfEpYdMaqJw5jUE8liUcsnIHoSpU'
bot = telebot.TeleBot(token)

password1 = ""
email1 = ""

@bot.message_handler(commands=['start'])
def start(message):
    L7N1 = types.InlineKeyboardButton(text="Dev🐉", url="https://t.me/F_0_oX")
    L7N2 = types.InlineKeyboardButton(text="start⚡", callback_data="L7Nstart")
    L7N3 = types.InlineKeyboardButton(text="stop🛑", callback_data="L7Nstop")
    
    L7N_ = types.InlineKeyboardMarkup()
    L7N_.row_width = 2
    L7N_.add(L7N1)
    L7N_.add(L7N3)
    
    # Get user profile photo
    user_photo = bot.get_user_profile_photos(message.from_user.id, limit=1).photos
    if user_photo:
        photo_file_id = user_photo[0][0].file_id
        bot.send_photo(message.chat.id, photo_file_id, caption='''🐍XPR🔥''', reply_markup=L7N_, parse_mode='MarkdownV2')
    else:
        bot.send_message(message.chat.id, "Sorry, couldn't retrieve your profile photo.")
        
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
    bot.send_message(message.chat.id, '''البوت يعمل الان''')

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
        bot.send_message(message.chat.id, "Good Login")    
    elif "wrong username or password" in response1.text:
        bot.send_message(message.chat.id, "wrong username or password")
    else:
        bot.send_message(message.chat.id, "Error")
        exit()

    # Function to call faucet every minute
    def faucet_call(message, remaining_time=60):
        cookies = sufi1
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

        rr = requests.post('https://faucetearner.org/api.php', params=params, cookies=cookies, headers=headers).text
        if 'Congratulations on receiving' in rr:
            json_data = json.loads(rr)
            message_text = json_data["message"]
            start_index = message_text.find(">") + 1
            end_index = message_text.find(" ", start_index)
            balance = message_text[start_index:end_index]
            bot.send_message(message.chat.id, f"Done {balance} XRP£.")
            # Send button with countdown timer
            send_countdown_button(message.chat.id, remaining_time)
        elif 'You have already claimed, please wait for the next wave!' in rr:
            bot.send_message(message.chat.id, "Please Wait to Finshed Time !!!🧚.")
            # Send button with countdown timer
            send_countdown_button(message.chat.id, remaining_time)
        else:
            bot.send_message(message.chat.id, "Error")
        
        # Call the faucet function again after 60 seconds
        Timer(60, faucet_call, args=[message, remaining_time]).start()

    # Call the faucet function for the first time
    faucet_call(message)

def send_countdown_button(chat_id, remaining_time):
    # Send a button with countdown timer for 60 seconds
    countdown_button = types.InlineKeyboardButton(f"Retry in {remaining_time} seconds ⏳", callback_data="countdown")
    countdown_markup = types.InlineKeyboardMarkup().add(countdown_button)
    bot.send_message(chat_id, f"Retry in {remaining_time} seconds ⏳", reply_markup=countdown_markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    message = call.message
    if call.data == "L7Nstop":
        bot.send_message(message.chat.id, text="تم اقاف البوت🌑", parse_mode='MarkdownV2')

bot.infinity_polling()
