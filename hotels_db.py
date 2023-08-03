from tortoise import Tortoise, fields, run_async
from tortoise.models import Model

class Client(Model):
    id = fields.IntField(pk=True)
    room = fields.ForeignKeyField("models.Room", related_name="clients")
    full_name = fields.CharField(max_length=255)
    phone_number = fields.CharField(max_length=15)
    date_start = fields.DateField()
    date_end = fields.DateField()

    class Meta:
        table = "clients"
        table_description = "This table contains a list of all the example clients"

    def str(self):
        return self.name


class Room(Model):
    id = fields.IntField(pk=True)
    hotel = fields.ForeignKeyField("models.Hotel", related_name="rooms")
    count_of_persons = fields.IntField()
    price = fields.IntField()

    clients: fields.ReverseRelation["Client"]

    class Meta:
        table = "rooms"
        table_description = "This table contains a list of all the example rooms"

    def str(self):
        return self.name


class Hotel(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField()
    stars = fields.IntField()
    minimal_price = fields.IntField()

    rooms: fields.ReverseRelation["Room"]

    class Meta:
        table = "hotels"
        table_description = "This table contains a list of all the example hotels"

    def str(self):
        return self.name


async def init():
    await Tortoise.init(
        db_url='sqlite://hotels.db',
        modules={"models": ["__main__"]}
    )
    await Tortoise.generate_schemas()

async def populate_data():
    hotel1 = await Hotel.create(
        name='Отель 1',
        description='Описание отеля 1',
        stars=4,
        minimal_price=1000
    )
    hotel2 = await Hotel.create(
        name='Отель 2',
        description='Описание отеля 2',
        stars=5,
        minimal_price=2000
    )

    room11 = await Room.create(
        hotel=hotel1,
        count_of_persons=2,
        price=800
    )
    room12 = await Room.create(
        hotel=hotel1,
        count_of_persons=3,
        price=1000
    )
    room13 = await Room.create(
        hotel=hotel1,
        count_of_persons=4,
        price=1200
    )

    room21 = await Room.create(
        hotel=hotel2,
        count_of_persons=2,
        price=1800
    )
    room22 = await Room.create(
        hotel=hotel2,
        count_of_persons=3,
        price=2200
    )
    room23 = await Room.create(
        hotel=hotel2,
        count_of_persons=4,
        price=2500
    )

    client1 = await Client.create(
        room=room11,
        full_name='Иванов Иван',
        phone_number='1234567890',
        date_start='2022-01-01',
        date_end='2022-01-10'
    )
    client2 = await Client.create(
        room=room11,
        full_name='Петров Петр',
        phone_number='0987654321',
        date_start='2022-01-05',
        date_end='2022-01-15'
    )
    client3 = await Client.create(
        room=room12,
        full_name='Сидоров Сидор',
        phone_number='1111111111',
        date_start='2022-02-01',
        date_end='2022-02-10'
    )
    client4 = await Client.create(
        room=room13,
        full_name='Алексеев Алексей',
        phone_number='2222222222',
        date_start='2022-03-01',
        date_end='2022-03-10'
    )
    client5 = await Client.create(
        room=room21,
        full_name='Иванов Иван',
        phone_number='3333333333',
        date_start='2022-02-05',
        date_end='2022-02-15'
    )
    client6 = await Client.create(
        room=room22,
        full_name='Петров Петр',
        phone_number='4444444444',
        date_start='2022-03-05',
        date_end='2022-03-15'
    )
    client7 = await Client.create(
        room=room23,
        full_name='Сидоров Сидор',
        phone_number='5555555555',
        date_start='2022-04-01',
        date_end='2022-04-10'
    )

async def print_cheapest_room():
    min_price = await Hotel.all().values_list('minimal_price')
    print(f"The cheapest room price: {min_price[0]}")

async def print_sorted_hotels():
    sorted_list = await Hotel.all().order_by('-minimal_price')
    print("Hotels sorted by descending prices:")
    for item in sorted_list:
        print(item.id, item.name, item.description, item.minimal_price)

async def print_sorted_clients():
    sorted_clients = await Client.all().order_by('room__price').values('room__hotel__name', 'full_name', 'phone_number')
    print("Clients sorted by room price, with hotel name instead of room_id:")
    for client in sorted_clients:
        print(client['room__hotel__name'], client['full_name'], client['phone_number'])

async def print_first_clients():
    sorted_clients = await Client.filter().order_by('date_start').group_by('room__hotel__name').values('room__hotel__name', 'full_name', 'phone_number', 'date_start')
    print("First client for each hotel:")
    for client in sorted_clients:
        print(client['room__hotel__name'], client['full_name'], client['phone_number'], client['date_start'])
async def run():
    await init()
    await populate_data()
    await print_cheapest_room()
    await print_sorted_hotels()
    await print_sorted_clients()
    await print_first_clients()


if __name__ == "__main__":
    run_async(run())
