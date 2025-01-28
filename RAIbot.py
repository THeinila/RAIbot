import discord
import dotenv
import os
import datetime
from datetime import time, datetime, timedelta
import asyncio

from urllib.request import urlopen

dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))
URL = "https://www.hs.fi/paakirjoitukset/"

bot = discord.Bot()
WHEN = time(18,59,00)
channel_id = str(os.getenv("CHANNEL_ID"))

def get_VR():
    page = urlopen(URL)
    html = page.read().decode("utf-8").split()

    for i in html:
        if i.find("978.webp") != -1:
            return i
  
    return False

async def called_once_a_day():
    await bot.wait_until_ready()
    weekday = datetime.today().weekday() 
    if weekday in [1,4]:
        channel = bot.get_channel(channel_id)
        vr = get_VR()
        if vr == 0:
            print("Virhe VR:n hakemisessa")
        else:
            await channel.send(vr)

async def background_task():
    now = datetime.now()
    if now.time() > WHEN:
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
        await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start 
    while True:
        now = datetime.now() 
        target_time = datetime.combine(now.date(), WHEN) 
        seconds_until_target = (target_time - now).total_seconds()
        await asyncio.sleep(seconds_until_target)  # Sleep until we hit the target time
        await called_once_a_day()  # Call the helper function that sends the message
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
        await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start a new iteration

@bot.event
async def on_ready():
    bot.loop.create_task(background_task())
    print(f"{bot.user} is ready and online!")
    
@bot.slash_command(name="uusin", description="Botti postaa uusimman VRn")
async def uusin(ctx: discord.ApplicationContext):
    vr = get_VR()
    if vr == False:
        await ctx.respond("Virhe VR:n hakemisessa")
    else:
        await ctx.respond(vr)

bot.run(os.getenv('TOKEN'))
