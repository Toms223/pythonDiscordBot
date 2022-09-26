import asyncio
import os
from discord import FFmpegOpusAudio, Embed
from random import shuffle
from pytube import YouTube, Search, Playlist


class Bot:
    def __init__(self, client):
        self.client = client
        self.channel = None
        self.voice = None
        self.queue: list[YouTube] = []

    async def join(self, message):
        text_channel = message.channel
        self.channel = message.author.voice.channel
        self.voice = await self.channel.connect()
        await text_channel.send("Connected to " + "`" + self.channel.name + "`")

    async def shuffle(self, message):
        text_channel = message.channel
        shuffle(self.queue)
        await text_channel.send("**Shuffled the queue**")

    async def leave(self, message):
        text_channel = message.channel
        if self.channel:
            self.queue = []
            await self.voice.disconnect()
            self.voice = None
            await text_channel.send("**Disconnected ** :airplane_departure:")
            for song in os.listdir("tmp"):
                os.remove("tmp/" + song)
        else:
            await text_channel.send("**You are not connected to any voice chat**")

    async def play(self, message, link):
        text_channel = message.channel
        try:
            song = YouTube(link)
        except:
            song = search(link)
        await text_channel.send("**Successfully added: **" + "`" + song.title + "`" + "** to queue.**")
        self.queue.append(song)
        if self.voice is None:
            await self.join(message)
            await self.music_play(message)

    async def pause(self, message):
        text_channel = message.channel
        if self.voice is not None:
            if self.voice.is_playing():
                self.voice.pause()
        await text_channel.send("**Player paused :pause_button:**")

    async def clear(self, message):
        text_channel = message.channel
        self.queue = []
        await text_channel.send("Queue cleared")

    async def resume(self, message):
        text_channel = message.channel
        if self.voice is not None:
            if self.voice.is_paused():
                self.voice.resume()
        await text_channel.send("**Player resumed :arrow_forward:**")

    async def list_play(self, message, link):
        text_channel = message.channel
        playlist = Playlist(link).videos
        await text_channel.send(f"Added **{len(playlist)}** songs to the queue.")
        if self.voice is None:
            self.queue.extend(playlist)
            await self.join(message)
            await self.music_play(message)
        else:
            self.queue.extend(playlist)

    async def music_play(self, message):
        text_channel = message.channel
        song = self.queue[0]
        file = song.streams.filter(only_audio=True).first().download("tmp")
        await text_channel.send("**Now playing: ** \n" + "`" + song.title + "`")
        self.voice.play(FFmpegOpusAudio(file), after=lambda e: self.next(message, file))

    def next(self, message, file):
        try:
            print(len(self.queue))
            if len(self.queue) > 1:
                self.queue.pop(0)
                fut = asyncio.run_coroutine_threadsafe(self.music_play(message), self.client.loop)
                fut.result()
            else:
                fut = asyncio.run_coroutine_threadsafe(self.leave(message), self.client.loop)
                fut.result()
        except Exception as e:
            print(e)

    async def music_list(self, message):
        text_channel = message.channel
        string = "**The songs in the queue are:**"
        if len(self.queue) > 10:
            max_range = 9
        else:
            max_range = len(self.queue)
        for i in range(1, max_range):
            string = string + "\n" + str(i) + "." + self.queue[i].title
        embed = Embed(title="🎶 Currently in queue: 🎶", colour=0x2cf267)
        embed.add_field(name=f"Currently playing: 🎧 {self.queue[0].title} 🎧", value=string, inline=False)
        await text_channel.send(embed=embed)

    async def skip(self, message):
        text_channel = message.channel
        self.voice.stop()
        await text_channel.send(f"**Skipped {self.queue[0].title} successfully!**")


def search(query) -> YouTube:
    result = Search(query).results[0]
    return result
