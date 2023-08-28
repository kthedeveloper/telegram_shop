from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

# Reply клавиатуры:

main_customer = ReplyKeyboardMarkup(resize_keyboard=True)
main_customer.add('Каталог').add('Корзина').add('Контакты')

main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add('Каталог').add('Корзина').add('Контакты').add('Админ-панель')

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add('Добавить товар').add('Удалить товар')  # .add('Сделать рассылку')

add_or_back = ReplyKeyboardMarkup(resize_keyboard=True)  #Выводить на страничке конкретного товара
add_or_back.add('Добавить в корзину').add('В каталог')



# Нужно еще придумать куда вставить кнопку "Оформить заказ", после нажатия на которую юзера будут просить ввести его
# контактные данные и данные для доставки, а после подтверждения его корзина и введенные данные будут улетать оператору
# магазина.


# Inline клавиатуры:

exact_product = InlineKeyboardMarkup(row_width=2)
exact_product.add(InlineKeyboardButton(text='Добавить в корзину'), InlineKeyboardButton(text='В каталог'))

catalogue = InlineKeyboardMarkup(row_width=2)


catalog_list = InlineKeyboardMarkup(row_width=2)
catalog_list.add(InlineKeyboardButton(text='Хлеб 1', callback_data='hleb1'),
                 InlineKeyboardButton(text='Хлеб 2', callback_data='hleb2'),
                 InlineKeyboardButton(text='Кулич', callback_data='kooleach'))

cancel = ReplyKeyboardMarkup(resize_keyboard=True)
cancel.add('Отмена')
