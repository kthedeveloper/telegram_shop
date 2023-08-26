import psycopg
from .keyboards import catalogue

PSQL_HOST = 'localhost'
PSQL_PORT = 5432
PSQL_USER = 'postgres'
PSQL_PASSWORD = 'Augustrush_24'
DATABASE_NAME = 'breadshop'


class DatabaseManager:
    def __init__(self):  # проверить насчет отдельного канала подключения к бд для каждого пользователя

        self.connection = await psycopg.AsyncConnection.connect(
            host=PSQL_HOST,
            port=PSQL_PORT,
            user=PSQL_USER,
            password=PSQL_PASSWORD,
            database=DATABASE_NAME
        )

    async def add_user(self, user_id, first_name):  # запись нового пользователя в список пользователей
        async with self.connection.cursor() as acur:
            await acur.execute("INSERT INTO accounts(tg_id, name) VALUES (%s, %s)", (user_id, first_name))

    async def add_to_cart(self, user_id, product_id):  # занесение данных в таблицу "юзер-корзина"
        async with self.connection.cursor() as acur:
            await acur.execute("INSERT INTO cart_product(user_id, product_id) VALUES (%s, %s)", (user_id, product_id))

    async def check_cart(self, user_id):  # посмотреть корзину конкретного пользователя
        async with self.connection.cursor() as acur:
            await acur.execute("")  # Доделать
            cart_result = await acur.fetchall()
            print(cart_result)

    async def check_catalogue(self):
        async with self.connection.cursor() as acur:
            await acur.execute("SELECT id, name FROM product")
            catalogue_message = ""
            catalogue_result = await acur.fetchall()
            for product_id, product_name in catalogue_result:
                catalogue_message += f"{product_id}. {product_name}\n"
                catalogue.add(text=product_name, callback_data=product_id)
        return catalogue_message, catalogue

    async def admin_add_product(self, state):  # добавить продукт
        async with state.proxy() as data:
            async with self.connection.cursor() as acur:
                acur.execute("INSERT INTO product(name, desc, price, photo, brand) VALUES (%s, %s, %s, %s, %s)",
                             (data['name'], data['desc'], data['price'], data['photo'], data['type']))
