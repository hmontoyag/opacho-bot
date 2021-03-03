import discord
import urllib.request
import json

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
    if discount == 0:
        discount = "None"
    else:
        discount = str(discount)+"%"
    return(name, price, discount, img, link)
