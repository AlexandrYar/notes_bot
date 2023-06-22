from app.config import BOT_API
from markUp import startMenu
from app.db import User, Task, create_all_db

import telebot
import datetime
bot = telebot.TeleBot(BOT_API)
user = User()
task = Task()
create_all_db()

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):

    user.name = message.chat.username
    user.role = 'user'
    user.tg_id = str(message.chat.id)
    user.user_is_register(str(message.chat.id))

    bot.send_message(message.chat.id, '''Привет, {}! 
Это мой первый бот!
id :{}'''.format(message.chat.username, message.chat.id), reply_markup=startMenu)


@bot.callback_query_handler(func=lambda callback:True)
def callback_message(callback):
    if callback.data == 'add_new_task':
        task.date_of_creation = str(datetime.datetime.now().date())
        task.executor_id = user.get_id_by_tg_id(callback.message.chat.id)
        print(user.get_id_by_tg_id(callback.message.chat.id))
        bot.send_message(callback.message.chat.id, 'Введите дату окончания вашей заметки')
        bot.register_next_step_handler(callback.message, add_execute_date)
 
    elif callback.data == 'all_my_task':   
        all_tasks = user.get_all_users_task(callback.message.chat.id)
        for tasks in all_tasks.values():
            bot.send_message(callback.message.chat.id, '''Дата создания : {}, 
Дата окончания: {},
Описание: {}'''.format(tasks['date_of_creation'], tasks['execution_date'], tasks['description']))

def add_execute_date(message):
    task.execution_date = str(message.text)
    bot.send_message(message.chat.id, 'Введите описание вашей заметки')
    bot.register_next_step_handler(message, add_desctiption)

def add_desctiption(message):
    task.description = str(message.text)
    print(task)
    task.create_task()
    bot.send_message(message.chat.id, 'Задание успешно добавлено', reply_markup=startMenu)

bot.polling(non_stop=True)