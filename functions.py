import discord
import urllib.request
import json
from discordToken import get_wolfram
from playhouse.shortcuts import model_to_dict
from peewee import *
from models import GameRecord, Petition, Stock, create_tables
from urllib.error import HTTPError
from googlefinance import getQuotes
import yfinance as yf

db = SqliteDatabase('content.db')
stock_db = SqliteDatabase('stocks.db')
def get_game_data(id, currency):
    contents = urllib.request.urlopen("https://store.steampowered.com/api/appdetails?appids=" + id + "&cc="+ currency).read()
    body = contents.decode('utf-8')
    data = json.loads(body)[id]['data']
    return data

async def call_out_for_muting(memb, before, after):
    targets = ['Goldmember']
    guild = memb.guild
    if guild.system_channel is not None and memb.name in targets:
        if after.self_mute == True and before.self_mute == False and before.channel == after.channel:
            await guild.system_channel.send('{0.mention} desmutea oe '.format(memb))
            was_muted = True
    return

async def check_game(game_id, currency_code):
    data = get_game_data(game_id, 'pen')
    name = data['name']
    discount = data['price_overview']['discount_percent']
    price = data['price_overview']['final_formatted']
    link = "https://store.steampowered.com/" + game_id
    img = data['header_image']
    return(name, price, discount, img, link)

'''
async def add_tracking(user_id, game_id, percent):
    create_tables()
    name, price, discount, img, link = await check_game(game_id, 'pen')
    if discount > percent:
        return (True, name, discount)
    #check if game already recorded, update if so, add record if not
    query = GameRecord.select().where(GameRecord.game_id == game_id)

    try:
        with db.atomic():
            record = GameRecord.create(game_id = game_id, last_discount = discount)
            record.save()
            print('not poop tho')
    except IntegrityError:

            return (False, name, discount)
            query = GameRecord.update(game_id = game_id).where(GameRecord.game_id == game_id)
    #add Petition
    petition = Petition.create(user_id = user_id, game_id = game_id, target = discount)
    petition.save()

    return(False, name, discount)

def check_petitions():
    for petition in Petition.select():
        print(model_to_dict(petition))

def check_records():
    for records in GameRecord.select():
        print(model_to_dict(records))
'''

async def wolfram(query):
    if query == "who+is+opacho+":
        return "I am. :frog:"
    url = "https://api.wolframalpha.com/v1/result?i="
    url += query + "%3F&appid=" + get_wolfram()
    try:
        contents = urllib.request.urlopen(url)
        result = contents.read().decode('utf-8')
    except HTTPError:
        result = "Couldn't find that. Blame Wolfram. :poo:"
    return(result)

async def stonk(stock):
    stock_name = stock
    try:
        stock = yf.Ticker(stock)
        stock = stock.info
    except:
        return (1, 1, "error")
    ask = stock['ask']
    bid = stock['bid']
    try:
        with stock_db.atomic():
            stock = Stock.create(name = stock_name, last_bid = bid)
            stock.save()
            trend = 'new'
    except IntegrityError:
        element = Stock.select().where(Stock.name == stock_name)
        last_bid = bid
        for i in element:
            last_bid = model_to_dict(i)['last_bid']
        query = Stock.update(last_bid = bid).where(Stock.name==stock_name)
        query.execute()
        if last_bid > bid:
            trend = 'down'
        else:
            trend = 'up'
    return (ask, bid, trend)
