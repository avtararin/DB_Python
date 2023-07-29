Для выполнения задания была использована библиотека sqlite3. Были созданы три таблицы:
- Hotels (id, name, descriptions, stars, minimalprice)
- Rooms (hotelid, countofpersons, price) с внешним ключом, относящимся к полю id таблицы Hotels
- Clients (roomid, fullname, phonenumber, datestart, dateend) с внешним ключом, относящимся к полю hotelid таблицы Rooms

Все таблицы были успешно заполнены данными.

Также были созданы запросы и результаты запросов были выведены на экран.