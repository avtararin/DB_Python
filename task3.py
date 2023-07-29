# Import Library
import sqlite3
# Connecting to DataBase
con = sqlite3.connect("hotels.db")
# Creating cursor
cur = con.cursor()
# Creating tables
cur.execute('''CREATE TABLE IF NOT EXISTS Hotels
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT,
                   description TEXT,
                   stars INTEGER,
                   minimal_price INTEGER)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Rooms
                  (hotel_id INTEGER,
                   count_of_persons INTEGER,
                   price INTEGER,
                   FOREIGN KEY (hotel_id) REFERENCES Hotels(id))''')
cur.execute('''CREATE TABLE IF NOT EXISTS Clients
                  (room_id INTEGER,
                   full_name TEXT,
                   phone_number TEXT,
                   date_start TEXT,
                   date_end TEXT,
                   FOREIGN KEY (room_id) REFERENCES Rooms(hotel_id))''')
# Entering data in tables
# Hotels
cur.execute("INSERT INTO Hotels (name, description, stars, minimal_price) VALUES ('Отель 1', 'Описание отеля 1', 4, 1000), ('Отель 2', 'Описание отеля 2', 5, 2000)")

# Rooms
cur.execute('''INSERT INTO Rooms (hotel_id, count_of_persons, price) VALUES (1, 2, 800),
            (1, 3, 1000),
            (1, 4, 1200),
            (2, 2, 1800),
            (2, 3, 2200),
            (2, 4, 2500)''')

# Clients
cur.execute('''INSERT INTO Clients (room_id, full_name, phone_number, date_start, date_end) VALUES (1, 'Иванов Иван', '1234567890', '2022-01-01', '2022-01-10'),
            (1, 'Петров Петр', '0987654321', '2022-01-05', '2022-01-15'),
            (2, 'Сидоров Сидор', '1111111111', '2022-02-01', '2022-02-10'),
            (3, 'Алексеев Алексей', '2222222222', '2022-03-01', '2022-03-10'),
            (4, 'Иванов Иван', '3333333333', '2022-02-05', '2022-02-15'),
            (5, 'Петров Петр', '4444444444', '2022-03-05', '2022-03-15'),
            (6, 'Сидоров Сидор', '5555555555', '2022-04-01', '2022-04-10')''')

# The cheapes Room
min_price = cur.execute('''SELECT min(price) FROM Rooms''')

print("--- The cheapes Room ---\n\n")

for elem in min_price:
    print(elem)

# The list of hotels sorted by descending prices

sorted_hotels = cur.execute('''SELECT * FROM Hotels
                            ORDER BY minimal_price DESC''')

print("--- The list of hotels sorted by descending prices ---\n\n")

for elem in sorted_hotels:
    print(elem)
print("\n\n")
# A list of clients sorted by room price, where instead of room_id the name of the hotel

sorted_clients = cur.execute('''SELECT h.name, c.full_name, c.phone_number
                  FROM Hotels h
                  INNER JOIN Rooms r ON h.id = r.hotel_id
                  INNER JOIN Clients c ON r.hotel_id = c.room_id
                  ORDER BY r.price''')

print("--- A list of clients sorted by room price, where instead of room_id the name of the hotel ---\n\n")

for elem in sorted_clients:
    print(elem)


con.close()