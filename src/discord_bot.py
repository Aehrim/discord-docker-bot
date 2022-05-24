import discord
from discord.ext import commands
from requests import get 
import json
import youtube_dl
import os
import asyncio


TOKEN = "OTc3MzY1MTY3NDc2MTkxMjUy.GaLUob.4z5oxPox8YMC_8s5PpcGRYNSG9-NVQIHtuyL3Y"

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="!")

@bot.command()
async def play(ctx, url:str):
    song_there = os.path.isfile("song.mp3")
    try: 
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Warte bis der Song zuende ist oder benutze das stop Command")
        return

    voice_channel = discord.utils.get(ctx.guild.voice_channels, name='General 2')
    await voice_channel.connect()
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.45

@bot.command()
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
       await voice.disconnect()
       await ctx.send ("Bot hat den Voicechannel Verlassen")

@bot.command()
async def duration(ctx):
    global is_playing
    is_playing = True
    await asyncio.sleep(500)
    is_playing = False
    await ctx.send ("Song Spielt Schon {duration}%")

@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.send("Song wurde Pausiert")
    else:
        await ctx.send("Es wird gerade nichts Abgespielt")

@bot.command()
async def resume(ctx):  
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.ispaused():
        voice.resume()
        await ctx.send("Song wird fortgesetzt")
    else:
        await ctx.send("Nichts ist gerade pausiert")

@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()
    await ctx.send("Song wurde Beendet")

@bot.command(pass_context=True)
async def guide(ctx):
    embed = discord.Embed(
        colour = discord.Colour.blue()
    )
    embed.set_author(name='Verfügbare Commands')
    embed.add_field(name='!play [URL]', value='spielt ein ausgesuchtes Youtube Video', inline='false')
    embed.add_field(name='!volume 1-200', value='Bestimmt die Lautstärke des Bots', inline='false')
    embed.add_field(name='!pause', value='pausiert den Song', inline='false')
    embed.add_field(name='!resume', value='Spielt den Song wieder ab', inline='false')
    embed.add_field(name='!stop', value='Stoppt den Aktuellen Song', inline='false')
    embed.add_field(name='!leave', value='Disconnected den Bot aus den Aktuellen Voice Channel', inline='false')
    embed.add_field(name='!guide', value='Zeigt alle verfügbaren Commands an', inline='false')
    embed.add_field(name='!meme', value='posted ein Random Meme von Reddit', inline='false')

    await ctx.send(embed=embed)

@bot.command()
async def meme(ctx):
    content = get("https://meme-api.herokuapp.com/gimme").text
    data = json.loads(content,)
    meme = discord.Embed(title=f"{data['title']}", Color = discord.Color.random()).set_image(url=f"{data['url']}")
    await ctx.reply(embed=meme)

@bot.command()
async def volume(ctx, volume: int):
    if ctx.voice_client is None:
        return await ctx.send("Ich bin auf keinem Voicechannel Connected")
    ctx.voice_client.source.volume = volume / 100
    await ctx.send(f"Meine Lautstärke ist jetzt {volume}%")

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='!guide für Hilfe'))
    print('Successfully Connected to Discord {0.user}'.format(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() == 'hello':
        await message.channel.send(f'Hello, {message.author.display_name}!')

    if message.content.lower() == 'bye':
        await message.channel.send(f'See you later, {message.author.display_name}!')
    else: 
        await bot.process_commands(message)

bot.run(TOKEN)