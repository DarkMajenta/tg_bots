import sqlite3

# Создание базы данных
conn = sqlite3.connect('call_control.db')

# Создание таблицы "Звонки"
conn.execute('''CREATE TABLE IF NOT EXISTS calls
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 caller TEXT NOT NULL,
                 receiver TEXT NOT NULL,
                 date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                 duration INTEGER)''')

# Создание таблицы "Заказы"
conn.execute('''CREATE TABLE IF NOT EXISTS orders
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 customer TEXT NOT NULL,
                 item TEXT NOT NULL,
                 price REAL,
                 date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

# Создание таблицы "Приход и расход денег"
conn.execute('''CREATE TABLE IF NOT EXISTS financial_transactions
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 description TEXT NOT NULL,
                 amount REAL,
                 date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

# Создание таблицы "Контрагенты"
conn.execute('''CREATE TABLE IF NOT EXISTS counterparts
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 type TEXT CHECK(type IN ('client', 'performer')))''')

# Закрытие соединения с базой данных
conn.close()

print("База данных успешно создана!")
