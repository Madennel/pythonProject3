import sqlite3


def initiate_db():
    # Создание соединения с базой данных
    conn = sqlite3.connect("not_telegram.db")
    cursor = conn.cursor()

    # Создание таблицы Products, если она не существует
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL,
        file_id TEXT
    )
    """)

    # Создание таблицы Users, если она не существует
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL DEFAULT 1000
    )
    """)

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()


def add_user(username, email, age):
    conn = sqlite3.connect("not_telegram.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, 1000)",
                   (username, email, age))
    conn.commit()
    conn.close()


def is_included(username):
    conn = sqlite3.connect("not_telegram.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user is not None


def get_all_products():
    conn = sqlite3.connect("not_telegram.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()  # Получаем все записи из таблицы
    conn.close()
    return products


def add_product(title, description, price, file_id):
    conn = sqlite3.connect("not_telegram.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Products (title, description, price, file_id) VALUES (?, ?, ?, ?)",
                   (title, description, price, file_id))
    conn.commit()
    conn.close()
