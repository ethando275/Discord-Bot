#required dependencies
import discord
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix = '!', intents = intents)

@client.event
async def on_ready():
    print('Bot is ready.')
    print('---------------')

@client.command()
async def hello(ctx):
    await ctx.send('Hello! I am a test bot')

client.run('MTE5ODcwMDU4MTk1NTU2NzYzNw.G9Uqfd.Wca4vjRgC4vRS0h2PUFoHG3VqN9_0FmsbZ-e5g')
