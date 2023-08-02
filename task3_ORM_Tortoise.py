from tortoise.models import Model
from tortoise import fields

class Hotels(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    description = fields.TextField()
    stars = fields.IntField()
    minimal_price = fields.IntFields()
    def __str__(self):
        return self.name
    
class Rooms(Model):
    # id = fields.IntField(pk=True)
    count_of_persons = fields.IntField()
    price = fields.IntField()
    hotel = fields.ForeignKeyField('models.Hotels', related_name='rooms') (pk=True)
    participants = fields.ManyToManyField('models.Team', related_name='events', through='event_team')

    def __str__(self):
        return self.name

class Clients(Model):
    # id = fields.IntField(pk=True)
    name = fields.TextField()
    full_name = fields.TextField()
    phone_number = fields.TextField()
    date_start = fields.TextField()
    date_end = fields.TextField()
    room_id = fields.ForeignKeyField('models.Rooms', related_name='clients') (pk=True)

    def __str__(self):
        return self.name
    
    
from tortoise import Tortoise, run_async

async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['app.models']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()

# run_async is a helper function to run simple async Tortoise scripts.
run_async(init())


# Create instance by save
async def main():
    hotel1 = Hotels(name='Hotel 1', description = 'Description hotel 1', stars = 4, minimal_price = 1000)
    await hotel1.save()
    hotel2 = Hotels(name='Hotel 2', description = 'Description hotel 2', stars = 5, minimal_price = 2000)
    await hotel2.save()
    # Or by .create()
    await Rooms.create(hotel = hotel1, count_of_persons = 3, price = 1000)
    await Rooms.create(hotel = hotel1, count_of_persons = 4, price = 1200)
    await Rooms.create(hotel = hotel2, count_of_persons = 2, price = 1800)
    await Rooms.create(hotel = hotel2, count_of_persons = 3, price = 2200)
    await Rooms.create(hotel = hotel2, count_of_persons = 4, price = 2500)

    await Clients.create(room_id = 1, full_name = 'Petrov Peter', phone_number = '0987654321', date_start = '2022-01-05', date_end = '2022-01-15')
    await Clients.create(room_id = 2, full_name = 'Sidorov Sidr', phone_number = '2222222222', date_start = '2022-02-01', date_end = '2022-02-10')
    await Clients.create(room_id = 3, full_name = 'Alekseev Aleksei', phone_number = '3333333333', date_start = '2022-03-01', date_end = '2022-03-10')
    await Clients.create(room_id = 1, full_name = 'Ivanov Ivan', phone_number = '4444444444', date_start = '2022-02-05', date_end = '2022-02-15')
    await Clients.create(room_id = 1, full_name = 'Petrov Peter', phone_number = '555555555', date_start = '2022-03-05', date_end = '2022-03-15')
    await Clients.create(room_id = 1, full_name = 'Sidorov Sidr', phone_number = '666666666', date_start = '2022-04-01', date_end = '2022-04-10')

run_async(main())

event = await Event.create(name='Test', tournament=tournament)

participants = []
for i in range(2):
    team = await Team.create(name='Team {}'.format(i + 1))
    participants.append(team)

# M2M Relationship management is quite straightforward
# (also look for methods .remove(...) and .clear())
await event.participants.add(*participants)

# You can query a related entity with async for
async for team in event.participants:
    pass

# After making a related query you can iterate with regular for,
# which can be extremely convenient when using it with other packages,
# for example some kind of serializers with nested support
for team in event.participants:
    pass


# Or you can make a preemptive call to fetch related objects
selected_events = await Event.filter(
    participants=participants[0].id
).prefetch_related('participants', 'tournament')

# Tortoise supports variable depth of prefetching related entities
# This will fetch all events for Team and in those events tournaments will be prefetched
await Team.all().prefetch_related('events__tournament')

# You can filter and order by related models too
await Tournament.filter(
    events__name__in=['Test', 'Prod']
).order_by('-events__participants__name').distinct()