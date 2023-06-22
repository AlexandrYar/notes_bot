from telebot import types

startMenu = types.InlineKeyboardMarkup(row_width=1)
btn_new_task = types.InlineKeyboardButton("Добавить новое задание", callback_data="add_new_task")
btn_all_tasks = types.InlineKeyboardButton('Показать все мои задания', callback_data='all_my_task')
startMenu.add(btn_new_task, btn_all_tasks)

