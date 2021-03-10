import discord
from discord.ext.commands import Bot
import functions as opacho
from discordToken import get_token
import random

TOKEN = get_token()

intents = discord.Intents.default()
intents.voice_states = True

bot = Bot(command_prefix=['opacho, ', 'Opacho, '], intents = intents, description = 'hair in oversoul.')


@bot.command()
async def steam(ctx, id):
    '''Gets link and some basic info on a steam game by game_id
    '''
    name, price, discount, img, link = await opacho.check_game(id,'pen')
    embed=discord.Embed(title=name, url=link, color=0x9600db)
    embed.set_image(url=img)
    embed.add_field(name="Price: ", value=price, inline=True)
    embed.add_field(name="Sale: ", value=discount, inline=True)
    embed.add_field(name="Alarm:",value="Off", inline=True)
    #embed.add_field(name="author:", value=ctx.author.name, inline=True)
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def info(ctx):
    '''testing command to print user id
    '''
    await check_record_list()

# 6 W's

@bot.command(pass_context=True)
async def what(ctx, *args):
    result = await wolfram_builder(args,'what')
    await ctx.send(result)
@bot.command(pass_context=True)
async def why(ctx, *args):
    result = await wolfram_builder(args,'why')
    await ctx.send(result)
@bot.command(pass_context=True)
async def who(ctx, *args):
    result = await wolfram_builder(args,'who')
    await ctx.send(result)
@bot.command(pass_context=True)
async def when(ctx, *args):
    result = await wolfram_builder(args,'when')
    await ctx.send(result)
@bot.command(pass_context=True)
async def where(ctx, *args):
    result = await wolfram_builder(args,'where')
    await ctx.send(result)
@bot.command(pass_context=True)
async def how(ctx, *args):
    result = await wolfram_builder(args,'how')
    await ctx.send(result)
async def wolfram_builder(args, word):
    query = word+'+'
    for arg in args:
        query+=arg+"+"
    result =  await opacho.wolfram(query)
    return result

@bot.command(pass_context=True)
async def value(ctx, stock):
    await ctx.send('Getting the tendies... ')
    ask, bid, trend = await opacho.stonk(stock)
    tendies = random.randint(1,1000)
    if trend == 'new':
        image = "https://www.best-buy-flags.co.uk/media/catalog/product/cache/2/small_image/265x/b0f61e07f65d897fb166b07707887ded/1/4/unicolor-red-headband-sweatband-6-x-21cm.png"
        desc = 'Welcome, you late-to-the-party crayon eating homunculus. :crayon:'
    elif trend == 'up':
        image = "https://upload.wikimedia.org/wikipedia/commons/2/21/Crispy_Chicken_Strips_-_FotoosVanRobin.jpg"
        desc = 'to the muuuuuuuuuuuun. :rocket:'
    elif trend == 'down':
        desc = "SELL SELL SELL SELL :roll_of_paper:"
        image = "https://i.imgur.com/XBZSzJo.png"
    else:
        await ctx.send("Something's off somewhere idk. :poo:")
        return
    link = "https://finance.yahoo.com/quote/"+ stock + "?p="+stock
    embed=discord.Embed(title="Data for " + stock, url=link, color=0x9600db, description=desc)
    embed.set_image(url=image)
    embed.add_field(name = "Ask: ", value=ask, inline=True)
    embed.add_field(name="Bid: ", value=bid, inline=True)
    await ctx.send(embed=embed)

'''
@bot.command(pass_context=True)
async def track(ctx, id, percent=0):
    user_id = ctx.message.author.id
    member = await bot.fetch_user(user_id)
    key, name, discount = await opacho.add_tracking(user_id, id, percent)
    if key:
        await ctx.send('**oo {0.mention}, {1} is currently at {2}% off!** So it wont be tracked.'.format(member, name, discount))
        await opacho.steam(ctx, id)
    else:

        await ctx.send('Got it.  Will let you know when {0} is at least over {1}% off.'.format(name,percent))
'''

@bot.event
async def on_ready():
    print('logged in as {0.user}'.format(bot))



@bot.event
async def on_voice_state_update(memb, before, after):
    await opacho.call_out_for_muting(memb, before, after)

bot.run(TOKEN)
