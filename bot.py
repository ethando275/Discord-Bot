import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import requests

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
HUGGING = os.getenv('HUGGING')

if TOKEN is None:
    raise ValueError('No token found. Please set the DISCORD_TOKEN environment variable.')

# Set up the bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    if bot.user is not None:
        print(f'Logged in as {bot.user.name} - {bot.user.id}')
    else:
        print('Bot user is not available.')

@bot.command()
async def pomodoro(ctx):
    await ctx.send('Starting Pomodoro timer for 25 minutes!')
    
    for minutes_left in range(25, 0, -1):
        await asyncio.sleep(60)  # Wait for 1 minute
        await ctx.send(f'{minutes_left} minutes remaining!')

    await ctx.send('Time for a 5-minute break!')
    await asyncio.sleep(300)  # Wait for 5 minutes
    await ctx.send('Pomodoro session ended!')

@bot.command()
async def ask(ctx, *, question):
    await ctx.send('Processing your question...')  # Processing message
    headers = {'Authorization': f'Bearer {HUGGING}'}
    
    # Using a more suitable model for question answering
    model_name = 'distilbert-base-uncased-distilled-squad'  # Example model
    payload = {
        'inputs': f"Answer the following question: {question}",
        'parameters': {
            'temperature': 0.5,
            'max_length': 50
        }
    }
    
    response = requests.post(f'https://api-inference.huggingface.co/models/{model_name}', headers=headers, json=payload)
    if response.status_code == 200:
        answer = response.json()[0]['generated_text']
        # Check length and truncate if necessary
        if len(answer) > 2000:
            for i in range(0, len(answer), 2000):
                await ctx.send(answer[i:i+2000])  # Send in chunks
        else:
            await ctx.send(answer)  # Send the answer
    else:
        await ctx.send('Error communicating with GPT model.')  # Error message

@bot.command()
@commands.has_permissions(manage_messages=True)  # Ensure the user has permission to manage messages
async def clear(ctx, amount: int):
    if amount < 1:
        await ctx.send("Please specify a number greater than 0.")
        return
    
    def is_bot_message(message):
        return message.author == ctx.bot.user  # Check if the message is from the bot

    deleted = await ctx.channel.purge(limit=amount, check=is_bot_message)
    await ctx.send(f'Deleted {len(deleted)} of my messages.', delete_after=5)  # Message will delete after 5 seconds

# Run the bot
bot.run(TOKEN)