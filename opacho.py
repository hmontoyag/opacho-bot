import discord
from discord.ext.commands import Bot
from functions import call_out_for_muting, check_game



TOKEN = 'ODE1NzUzNTc2MTYwMTY1OTA4.YDw_uA.G7RqZFSkbJ9RlMS5P3VKEP0RWjY'

intents = discord.Intents.default()
intents.voice_states = True

bot = Bot(command_prefix='&', intents = intents, description = 'hair in oversoul.')


@bot.command()
async def steam(ctx, id):
    name, price, discount, img, link = await check_game(id,'pen')
    embed=discord.Embed(title=name, url=link, color=0x9600db)
    embed.set_image(url=img)
    embed.add_field(name="Price: ", value=price, inline=True)
    embed.add_field(name="Sale: ", value=discount, inline=True)
    embed.add_field(name="Alarm:",value="Off", inline=True)
    #embed.add_field(name="author:", value=ctx.author.name, inline=True)
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print('logged in as {0.user}'.format(bot))




@bot.event
async def on_voice_state_update(memb, before, after):
    await call_out_for_muting(memb, before, after)

bot.run(TOKEN)
