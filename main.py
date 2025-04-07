import discord
from discord.ext import commands
import yt_dlp
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def play(ctx, url):
    if ctx.author.voice is None:
        await ctx.send("Você precisa estar em um canal de voz primeiro!")
        return

    voice_channel = ctx.author.voice.channel

    if ctx.voice_client is None:
        await voice_channel.connect()

    vc = ctx.voice_client

    # Puxa o áudio do YouTube com yt_dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'extract_flat': False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        stream_url = info['url']

    # Reproduz com FFmpeg
    vc.play(discord.FFmpegPCMAudio(stream_url), after=lambda e: print(f"Erro: {e}" if e else "Terminado"))
    await ctx.send(f"Tocando agora: {info['title']}")

@bot.command()
async def stop(ctx):
    await ctx.voice_client.disconnect()

bot.run(os.getenv("TOKEN"))
