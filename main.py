from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from app import keyboards as kb
from app.database import DatabaseManager
from dotenv import load_dotenv
import os

storage = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot, storage=storage)
database = DatabaseManager()


async def on_startup(_):
    # await db.db_start()
    print('Бот успешно запущен')


class NewProduct(StatesGroup):
    type = State()
    name = State()
    desc = State()
    price = State()
    photo = State()


#      -------------- Хэндлеры для команд покупателя ------------
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await database.add_user(database, message.from_user.id)
    await message.answer(f'{message.from_user.first_name}, добро пожаловать в магазин домашнего хлеба и выпечки!',
                         reply_markup=kb.main_customer)

    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Вы авторизовались как администратор', reply_markup=kb.main_admin)
    else:
        await message.reply('К сожалению, я Вас не понял.')


@dp.message_handler(text='Контакты')
async def contacts(message: types.Message):
    await message.answer(f'По всем вопросам: @rks998')


@dp.message_handler(text='Каталог')
async def catalog(message: types.Message):
    answer_message, keyboard = await database.check_catalogue()
    await message.answer(answer_message, reply_markup=keyboard)


@dp.message_handler(text='Корзина')
async def cart(message: types.Message):
    await message.answer(f'Корзина пуста')  # тут должен вызываться метод check_cart из database.py


#      -------------- Хэндлеры для команд администратора ------------

@dp.message_handler(text='Админ-панель')
async def admin_panel(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Вы вошли в админ-панель', reply_markup=kb.admin_panel)
    else:
        await message.reply('К сожалению, я Вас не понял.')


@dp.message_handler(text='Добавить товар')
async def add_item(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await NewProduct.type.set()  # вызываем set для type
        await message.answer('Выберите тип товара', reply_markup=kb.catalog_list)
    else:
        await message.reply('К сожалению, я Вас не понял.')


@dp.callback_query_handler(state=NewProduct.type)
async def add_item_type(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:  # state.proxy это хранилище данных состояний (типа словаря)
        data['type'] = call.data
    await call.message.answer('Напишите название товара', reply_markup=kb.cancel)
    await NewProduct.next()


@dp.message_handler(state=NewProduct.name)
async def add_item_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('Напишите описание товара')
    await NewProduct.next()


@dp.message_handler(state=NewProduct.desc)
async def add_item_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
    await message.answer('Напишите цену товара')
    await NewProduct.next()


@dp.message_handler(state=NewProduct.price)
async def add_item_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer('Отправьте фотографию товара')
    await NewProduct.next()


@dp.message_handler(lambda message: not message.photo, state=NewProduct.photo)
async def add_item_photo_check(message: types.Message):
    await message.answer('Это не фотография!')


@dp.message_handler(content_types=['photo'], state=NewProduct.photo)
async def add_item_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[
            0].file_id  # сохраняется не само фото, а присваиваемый ему телеграмом айдишник, его же можно сохранить в бд
    #   await db.add_item(state)
    await message.answer('Товар успешно создан!', reply_markup=kb.admin_panel)
    await state.finish()
    # тут должно быть занесение всех данных нового товара в бд


#      -------------- Любые неизвестные боту сообщения ------------
@dp.message_handler()
async def answer(message: types.Message):
    await message.reply(
        'К сожалению, я Вас не понял.')


# -------------- Хэндлеры callback-data из Inline кнопок ------------



@dp.callback_query_handler()
async def callback_query_keyboard(callback_query: types.CallbackQuery):
    if callback_query.data == 'hleb1':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Вы выбрали хлеб №1')
    elif callback_query.data == 'hleb2':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Вы выбрали хлеб №2')
    elif callback_query.data == 'kooleach':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Вы выбрали кулич')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
