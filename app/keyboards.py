from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('Каталог').add('Корзина').add('Контакты')

main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add('Каталог').add('Корзина').add('Контакты').add('Админ-панель')

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add('Добавить товар').add('Удалить товар').add('Сделать рассылку')

catalog_list = InlineKeyboardMarkup(row_width=2)
catalog_list.add(InlineKeyboardButton(text='Хлеб 1', callback_data='hleb1'),
                 InlineKeyboardButton(text='Хлеб 2', callback_data='hleb2'),
                 InlineKeyboardButton(text='Кулич', callback_data='kooleach'))

cancel = ReplyKeyboardMarkup(resize_keyboard=True)
cancel.add('Отмена')
