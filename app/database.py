import psycopg
from .keyboards import catalogue, exact_product
from aiogram.types import InlineKeyboardButton

PSQL_HOST = 'localhost'
PSQL_PORT = 5432
PSQL_USER = 'postgres'
PSQL_PASSWORD = 'Augustrush_24'
DATABASE_NAME = 'breadshop'


class DatabaseManager:
    def __init__(self):
        self.connection = None

    async def connect_to_db(self):

        self.connection = await psycopg.AsyncConnection.connect(  # это надо запихнуть в асинхронную функцию
            host=PSQL_HOST,
            port=PSQL_PORT,
            user=PSQL_USER,
            password=PSQL_PASSWORD,
            database=DATABASE_NAME
        )

    async def add_user(self, user_id, first_name):  # запись нового пользователя в список пользователей
        async with self.connection.cursor() as acur:
            await acur.execute("INSERT INTO accounts(tg_id, name) VALUES (%s, %s)", (user_id, first_name))

    async def add_to_cart(self, user_id, product_id):  # занесение данных в таблицу "юзер-продукт"
        async with self.connection.cursor() as acur:
            await acur.execute("INSERT INTO cart_product(user_id, product_id) VALUES (%s, %s)", (user_id, product_id))

    async def check_cart(self, user_id):  # посмотреть корзину конкретного пользователя
        cart_dict = {}
        async with self.connection.cursor() as acur:
            await acur.execute("SELECT product.name FROM users "
                               "LEFT JOIN cart_product ON users.tg_id = cart_product.user_id "
                               "LEFT JOIN product ON cart_product.product_id = product.id "
                               f"WHERE users.tg_id = %s", user_id)
            for name, _ in await acur.fetchall():
                if name not in cart_dict.keys():
                    cart_dict[name] = 1
                else:
                    cart_dict[name] += 1

            return cart_dict

    async def get_products(self):
        async with self.connection.cursor() as acur:
            await acur.execute("SELECT id, name FROM product")
            return await acur.fetchall()

    async def check_catalogue(self):
        products = await self.get_products()
        catalogue_message = ""
        for product_id, product_name in products:
            catalogue_message += f"{product_id}. {product_name}\n"
            catalogue.add(InlineKeyboardButton(text=product_name,
                                               callback_data=product_id))  # как этот product_id Отсюда вытащить и передать дальше?
            return catalogue_message, catalogue, product_id  # непонятно

    async def get_exact_product(self, product_id):
        async with self.connection.cursor() as acur:
            await acur.execute("SELECT name, desc FROM product WHERE id = %s", product_id)
            product_name, product_desc = await acur.fetchall()[0]
            return f"{product_name} \n {product_desc}"

    async def admin_add_product(self, state):  # добавить продукт в каталог
        async with state.proxy() as data:
            async with self.connection.cursor() as acur:
                acur.execute("INSERT INTO product(name, desc, price, photo, brand) VALUES (%s, %s, %s, %s, %s)",
                             (data['name'], data['desc'], data['price'], data['photo'], data['type']))
