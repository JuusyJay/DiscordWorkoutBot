import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), help_command=None)

# Load cogs
initial_extensions = [
    'cogs.workout_cog',
    'cogs.survey_cog',
    'cogs.macros_cog',
    'cogs.utility_cog',
]

async def load_cogs():
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)  # Await the coroutine properly
            print(f"Loaded extension: {extension}")
        except Exception as e:
            print(f"Failed to load extension {extension}. Error: {e}")

if __name__ == '__main__':
    asyncio.run(load_cogs())  # Use asyncio.run() to create a new event loop and run the coroutine

TOKEN = os.getenv('DISCORD_TOKEN')

# Set the event loop explicitly
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Run the bot
bot.run(TOKEN)