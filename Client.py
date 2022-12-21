import discord
from Bot import Bot
from dotenv import load_dotenv
import os

load_dotenv("shhh.env")
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

clients = {}
application = discord.Client(intents=intents)

for song in os.listdir("tmp"):
    os.remove("tmp/" + song)


@application.event
async def on_ready():
    print(f"{application.user} ready!")
    guilds = application.guilds
    for i in guilds:
        clients[i] = Bot(application)
        print(i)


@application.event
async def on_message(message):
    if message.author == application.user:
        return
    parsed = message.content.split()
    if ".join" == parsed[0]:
        await clients[message.guild].join(message)

    if ".p" == parsed[0] or ".play" == parsed[0]:
        if "&list" in parsed[1] or "?list" in parsed[1]:
            await clients[message.guild].list_play(message, parsed[1])
        else:
            query = message.content.replace(parsed[0], "")
            await clients[message.guild].play(message, query)

    if ".skip" == parsed[0] or ".fs" == parsed[0] or ".s" == parsed[0]:
        await clients[message.guild].skip(message)

    if ".queue" == parsed[0]:
        await clients[message.guild].music_list(message)

    if ".disconnect" == parsed[0] or ".dc" == parsed[0] or ".leave" == parsed[0] or ".stop" == parsed[0]:
        await clients[message.guild].leave(message)

    if ".shuffle" == parsed[0]:
        await clients[message.guild].shuffle(message)

    if ".pause" == parsed[0]:
        await clients[message.guild].pause(message)

    if ".clear" == parsed[0]:
        await clients[message.guild].clear(message)

    if ".resume" == parsed[0]:
        await clients[message.guild].resume(message)

    if ".loop" == parsed[0]:
        await clients[message.guild].set_loop(message)



if __name__ == "__main__":
    application.run(TOKEN)
