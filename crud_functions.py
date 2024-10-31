import sqlite3


def alter_table_add_file_id():
    conn = sqlite3.connect("not_telegram.db")
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE Products ADD COLUMN file_id TEXT")
    conn.commit()
    conn.close()

alter_table_add_file_id()


# Функция для инициализации базы данных и создания таблицы Products
def initiate_db():
    conn = sqlite3.connect("not_telegram.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# Функция для получения всех продуктов
def get_all_products():
    conn = sqlite3.connect("not_telegram.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, price FROM Products")
    products = cursor.fetchall()
    conn.close()
    return products


# Функция для добавления продуктов в таблицу
def add_product(title, description, price):
    conn = sqlite3.connect("not_telegram.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)", (title, description, price))
    conn.commit()
    conn.close()


# Инициализация базы данных при первом запуске
initiate_db()


# Функция для получения всех продуктов
def get_all_products():
    conn = sqlite3.connect("not_telegram.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, price FROM Products")
    products = cursor.fetchall()
    conn.close()
    return products
