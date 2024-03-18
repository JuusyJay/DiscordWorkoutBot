import discord
from discord.ext import commands
import pymongo
from database import collection, URI


class MacrosCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = pymongo.MongoClient(URI)
        self.db = self.client['workoutDB']
        self.collection = self.db['user_accounts']

    @commands.command()
    async def macros(self, ctx):
        user_id = ctx.author.id

        find = collection.find_one({"_id": user_id})  # Remove the 'await' keyword
        if find is None:
            await ctx.send("User document not found.")
            return

        # Retrieve the user's macros from the database
        protein = find.get("protein", 0)
        fat = find.get("fat", 0)
        carbohydrates = find.get("carbohydrates", 0)
        total_calories = find.get("total_calories", 0)

        # Format the message with the user's macros
        message = f"**__Your daily macronutrient goals:__**\n\n```Protein: {protein:.2f}g\nFat: {fat:.2f}g\nCarbohydrates: {carbohydrates:.2f}g\nTotal Calories: {total_calories:.2f}```"

        # Send the message to the user
        await ctx.send(message)

async def setup(bot):
    await bot.add_cog(MacrosCog(bot))
