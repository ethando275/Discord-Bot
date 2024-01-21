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

client.run('MTE5ODcwMDU4MTk1NTU2NzYzNw.GvpzH_.GyF5QReIeAUMO8fhHETzGvHMdU0Fz7leOqe7-Y')
