from peewee import *
db = SqliteDatabase('content.db')
stock_db = SqliteDatabase('stocks.db')
KEY = 'MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAkgDUAAjZUpWw9z'

class BaseModel(Model):

    class Meta:
        database = db

class GameRecord(BaseModel):
    game_id = CharField(primary_key = True)
    last_discount = IntegerField(default=0)

class Petition(BaseModel):
    user_id = CharField(null=False)
    game_id = CharField(null=False)
    target = IntegerField(default = 0)

    class Meta:
        primary_key = CompositeKey('user_id', 'game_id')

class Stock(Model):
    name = CharField(primary_key = True)
    last_bid = IntegerField(default = 0)
    class Meta:
        database = stock_db

def create_tables():
    """creates tables if not created
    """
    with db:
        db.create_tables([GameRecord, Petition, Stock])
    with stock_db:
        stock_db.create_tables([Stock])


create_tables()
