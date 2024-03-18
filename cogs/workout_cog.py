import discord
from discord.ext import commands
import pymongo
from database import collection, URI
from utils import create_account

class WorkoutButtons(discord.ui.View):
    def __init__(self, up: str, low: str, push: str, pull: str, leg: str, user_id: int, log_immediately: bool = True):
        super().__init__()
        self.up = up
        self.low = low
        self.push = push
        self.pull = pull
        self.leg = leg
        self.user_id = user_id
        self.log_immediately = log_immediately

    async def log_workout(self, category: str):
        try:
            find = collection.find_one({"_id": self.user_id})
        except Exception as e:
            print("An error occurred while querying the database:", e)
            return

        if find is None:
            print("User document not found.")
            return

        # Update the workout count based on the category
        updated_count = find.get(category, 0) + 1

        try:
            result = collection.update_one({"_id": self.user_id}, {"$set": {category: updated_count}})
            if result.modified_count == 0:
                print("Failed to update workout count.")
            else:
                print(f"Updated {category} workout count for user {self.user_id}.")
        except Exception as e:
            print("An error occurred while updating workout count:", e)

    @discord.ui.button(label="Upper Body", style=discord.ButtonStyle.blurple)
    async def Btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You Added:" + self.up, ephemeral=False)
        if self.log_immediately:
            await self.log_workout("upper")

    @discord.ui.button(label="Lower Body", style=discord.ButtonStyle.blurple)
    async def Btn1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You Added:" + self.low, ephemeral=False)
        if self.log_immediately:
            await self.log_workout("lower")

    @discord.ui.button(label="Push", style=discord.ButtonStyle.blurple)
    async def Btn2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You Added:" + self.push, ephemeral=False)
        if self.log_immediately:
            await self.log_workout("push")

    @discord.ui.button(label="Pull", style=discord.ButtonStyle.blurple)
    async def Btn3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You Added:" + self.pull, ephemeral=False)
        if self.log_immediately:
            await self.log_workout("pull")

    @discord.ui.button(label="Legs", style=discord.ButtonStyle.blurple)
    async def Btn4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You Added:" + self.leg, ephemeral=False)
        if self.log_immediately:
            await self.log_workout("legs")

class WorkoutCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = pymongo.MongoClient(URI)
        self.db = self.client['workoutDB']
        self.collection = self.db['user_accounts']

    @commands.command()
    async def workout(self, ctx):
        low = f'**__LOWER WORKOUT:__**\n\n```Squat: 3 Sets, 8-10 Reps!\nQuad Extension: 3 Sets, 8-12 Reps!\nSplit Squat: 3 Sets, 8-10 Reps!\nHamstring Machine: 3 Sets, 12-15 Reps!```'
        push = f'**__PUSH WORKOUT:__**\n\n```Bench Press: 3 Sets, 8-10 Reps!\nShoulder Press: 3 Sets, 8-12 Reps!\nSkull Crushers: 3 Sets, 8-10 Reps!\nCable Fly: 3 Sets, 12-15 Reps!```'
        pull = f'**__PULL WORKOUT:__**\n\n```Pull Ups: 3 Sets, 8-10 Reps!\nCable Pulldown: 3 Sets, 8-12 Reps!\nCurls: 3 Sets, 8-10 Reps!\nReverse Fly: 3 Sets, 12-15 Reps!```'
        leg = f'**__LEG WORKOUT:__**\n\n```Squats: 3 Sets, 8-10 Reps!\nSplit Squat: 3 Sets, 8-12 Reps!\nQuad Extensions: 3 Sets, 8-10 Reps!\nDead Lift: 3 Sets, 6-10 Reps!```'
        up = f'**__UPPER WORKOUT:__**\n\n```Bench Press: 3 Sets, 8-10 Reps!\nOverhead Press: 3 Sets, 8-12 Reps!\nSkull Crushers: 3 Sets, 8-10 Reps!\nCable Fly: 3 Sets, 12-15 Reps!```'
        view = WorkoutButtons(str(up), str(low), str(push), str(pull), str(leg), ctx.author.id, log_immediately=False)
        await ctx.send("Click the buttons below to Select a Workout:", view=view)
        # THE await ctx.send SENDS THE MESSAGE AND EACH BUTTON
        # **_text here__** is bold and underlined in discord ```text_here``` is boxed text in disc

    @commands.command()
    async def log(self, ctx):
        user_id = ctx.author.id
        view = WorkoutButtons("Upper Body Workout", "Lower Body Workout", "Push Workout", "Pull Workout", "Legs Workout", user_id)
        await ctx.send("Select the workout you want to log:", view=view)

    @commands.command()
    async def progress(self, ctx):
        user_id = ctx.author.id

        try:
            user_data = collection.find_one({"_id": user_id})
        except Exception as e:
            print("An error occurred while querying the database:", e)
            await ctx.send("Failed to fetch progress.")
            return

        if user_data is None:
            await ctx.send("User data not found.")
            return

        # Retrieve workout counts for different categories
        upper_count = user_data.get("upper", 0)
        lower_count = user_data.get("lower", 0)
        push_count = user_data.get("push", 0)
        pull_count = user_data.get("pull", 0)
        legs_count = user_data.get("legs", 0)

        # Format the progress message
        progress_message = f"**Workout Progress for {ctx.author.name}:**\n\n" \
                        f"Upper Body Workouts: {upper_count}\n" \
                        f"Lower Body Workouts: {lower_count}\n" \
                        f"Push Workouts: {push_count}\n" \
                        f"Pull Workouts: {pull_count}\n" \
                        f"Legs Workouts: {legs_count}"

        # Send the progress message
        await ctx.send(progress_message)

    @commands.command()
    async def resetlog(self, ctx):
        user_id = ctx.author.id

        try:
            result = collection.update_one({"_id": user_id}, {"$set": {
                "upper": 0,
                "lower": 0,
                "push": 0,
                "pull": 0,
                "legs": 0
            }})
            if result.modified_count > 0:
                await ctx.send("Workout logs reset successfully.")
            else:
                await ctx.send("No workout logs found for reset.")
        except Exception as e:
            print("An error occurred while resetting workout logs:", e)
            await ctx.send("Failed to reset workout logs.")

async def setup(bot):
    await bot.add_cog(WorkoutCog(bot))