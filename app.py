import telebot
import subprocess
import os
import requests
from telebot import types

API_TOKEN = "7302759788:AAHFMBSTD1YHT8UGYraxKEw1kZwXxQCFhZQ"
bot = telebot.TeleBot(API_TOKEN)
running_processes = {}
all_files = []
MAX_RUNNING_FILES = 4

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    reply_message = f"""
╔━━━━━🧟‍♂WELCOME🧟‍♂━━━━━━╗

  💃𝐇𝐢 {first_name} 𝐢𝐧 𝐦𝐲 𝐁𝐨𝐭🥶

  🍀استضاقه ملفات بوتات بايثون مجاني 🍀
  
  🌟𝚜𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕𝚕𝚢 𝚕𝚘𝚐𝚒𝚗🌟
  
  ♻️ برجاء ارسال ملف بوتك حتي يتم تشغيله  
  لعرض جميع ملفاتك /list_all لمعرفه الملفات التي تعمل والتي لا تعمل  /user_info♻️

  [♻️] 𝗕𝗢𝗧 𝗕𝘆 @F_0_1X★👑★

╚━━━━━━━━━👑👑━━━━━━━━━╝
"""
    bot.reply_to(message, reply_message)
@bot.message_handler(content_types=['document'])
def handle_docs(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_name = message.document.file_name

    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    all_files.append(file_name)
    bot.reply_to(message, f"𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹 : Your BoY [{file_name}]🎉")
    user_info = get_user_info(message)
    bot.send_message(message.chat.id, user_info)
    
    # عرض أزرار التحكم
    control_buttons = telebot.types.InlineKeyboardMarkup()
    control_buttons.add(
        telebot.types.InlineKeyboardButton('تشغيل', callback_data=f'run_{file_name}'),
        telebot.types.InlineKeyboardButton('إيقاف', callback_data=f'stop_{file_name}'),
        telebot.types.InlineKeyboardButton('إعادة تشغيل', callback_data=f'restart_{file_name}'),
        telebot.types.InlineKeyboardButton('حذف', callback_data=f'delete_{file_name}')
    )
    bot.send_message(message.chat.id, f"YOUR BOT 🐍: {file_name}", reply_markup=control_buttons)

def get_user_info(message):
    user = message.from_user
    user_id = user.id
    username = user.username
    running_count = len(running_processes)
    not_running_count = len(all_files) - running_count

    info = (f"معلومات المستخدم:\n"
            f"ID: {user_id}\n"
            f"Username: {username}\n"
            f"عدد الملفات التي تعمل: {running_count}\n"
            f"عدد الملفات التي لا تعمل: {not_running_count}")
    
    return info

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    command, file_name = call.data.split('_', 1)

    if command == 'run':
        run_file(call.message, file_name)
    elif command == 'stop':
        stop_file(call.message, file_name)
    elif command == 'restart':
        restart_file(call.message, file_name)
    elif command == 'delete':
        delete_file(call.message, file_name)

def run_file(message, file_name):
    if file_name in running_processes:
        bot.reply_to(message, f"الملف {file_name} يعمل بالفعل.")
    elif len(running_processes) >= MAX_RUNNING_FILES:
        bot.reply_to(message, f"لا يمكن تشغيل المزيد من الملفات، حد أقصى لعدد الملفات المعمول بها: {MAX_RUNNING_FILES}.")
    else:
        process = subprocess.Popen(['python', file_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        running_processes[file_name] = process
        bot.reply_to(message, f"تم تشغيل الملف {file_name}.\n\n{get_user_info(message)}")

def stop_file(message, file_name):
    if file_name in running_processes:
        process = running_processes[file_name]
        process.terminate()
        del running_processes[file_name]
        bot.reply_to(message, f"تم إيقاف الملف {file_name}.\n\n{get_user_info(message)}")
    else:
        bot.reply_to(message, f"الملف {file_name} لا يعمل حاليا.")

def restart_file(message, file_name):
    if file_name in running_processes:
        process = running_processes[file_name]
        process.terminate()
        process.wait()
        new_process = subprocess.Popen(['python', file_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        running_processes[file_name] = new_process
        bot.reply_to(message, f"تم إعادة تشغيل الملف {file_name}.\n\n{get_user_info(message)}")
    else:
        bot.reply_to(message, f"الملف {file_name} لا يعمل حاليا.")

def delete_file(message, file_name):
    if file_name in all_files:
        if file_name in running_processes:
            process = running_processes[file_name]
            process.terminate()
            del running_processes[file_name]
        os.remove(file_name)
        all_files.remove(file_name)
        bot.reply_to(message, f"تم حذف الملف {file_name}.\n\n{get_user_info(message)}")
    else:
        bot.reply_to(message, f"الملف {file_name} غير موجود.")

@bot.message_handler(commands=['list_running'])
def list_running_files(message):
    if running_processes:
        running_files = "\n".join(running_processes.keys())
        bot.reply_to(message, f"الملفات التي تعمل حاليا:\n{running_files}")
    else:
        bot.reply_to(message, "لا توجد ملفات تعمل حاليا.")

@bot.message_handler(commands=['list_all'])
def list_all_files(message):
    if all_files:
        all_files_list = "\n".join(all_files)
        bot.reply_to(message, f"جميع الملفات:\n{all_files_list}")
    else:
        bot.reply_to(message, "لا توجد ملفات مضافة.")

@bot.message_handler(commands=['user_info'])
def user_info(message):
    info = get_user_info(message)
    bot.reply_to(message, info)
def check_errors():
    for file_name, process in list(running_processes.items()):
        if process.poll() is not None: 
            stdout, stderr = process.communicate()
            if stderr:
                bot.send_message(user_id, f"حدث خطأ أثناء تشغيل الملف {file_name}:\n{stderr.decode()}")

if __name__ == '__main__':
    bot.polling(none_stop=True)
