import discord
from typing import Final
import os
from dotenv import load_dotenv
from discord.ext import commands
from random import choice, randint
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import asyncio
import pymongo


# Set the event loop explicitly
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

#TELLS BOT THAT COMMANDS START WITH "!" AND GIVES INTENT/PERMISSIONS TO ALL FOR BOT
bot = commands.Bot(command_prefix="!", intents = discord.Intents.all(), help_command=None)


#LOAD OUR TOKEN FROM SAFE PLACE :D uwu poosy ALSO LOAD DATABASE URI
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
URI: Final[str] = os.getenv('MONGODB_URI')


#CALLS BOT EVENT TO DISPLAY IN CONSOLE THAT BOT IS CONNECTED
@bot.event
async def on_ready():
    print("Jotaro has connected to Discord!")

#DATABASE CONNECTION
#create a new client and connect to the MONGODB ATLAS server
client = pymongo.MongoClient(URI)
db = client['workoutDB']  
collection = db['user_accounts']  


#try to send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)    


#TESTING  WORKOUT BUTTONS:
class WorkoutButtons(discord.ui.View):
    def __init__(self, up: str, low: str, push: str, pull: str, leg: str, user_id: int):
        super().__init__()
        self.up = up
        self.low = low
        self.push = push
        self.pull = pull
        self.leg = leg
        self.user_id = user_id

    @discord.ui.button(label="Upper Body", style=discord.ButtonStyle.blurple)
    async def Btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You Added:" + self.up, ephemeral=False)
        await self.log_workout("upper")

    @discord.ui.button(label="Lower Body", style=discord.ButtonStyle.blurple)
    async def Btn1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You Added:" + self.low, ephemeral=False)
        await self.log_workout("lower")

    @discord.ui.button(label="Push", style=discord.ButtonStyle.blurple)
    async def Btn2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You Added:" + self.push, ephemeral=False)
        await self.log_workout("push")

    @discord.ui.button(label="Pull", style=discord.ButtonStyle.blurple)
    async def Btn3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You Added:" + self.pull, ephemeral=False)
        await self.log_workout("pull")

    @discord.ui.button(label="Legs", style=discord.ButtonStyle.blurple)
    async def Btn4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You Added:" + self.leg, ephemeral=False)
        await self.log_workout("legs")

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


#DEFINES THE COMMAND AS "!workout" AND SETS MESSAGES FOR EACH BUTTON LABEL
@bot.command()
async def workout(ctx: commands.Context):
    low = f'**__LOWER WORKOUT:__**\n\n```Squat: 3 Sets, 8-10 Reps!\nQuad Extension: 3 Sets, 8-12 Reps!\nSplit Squat: 3 Sets, 8-10 Reps!\nHamstring Machine: 3 Sets, 12-15 Reps!```'
    push = f'**__PUSH WORKOUT:__**\n\n```Bench Press: 3 Sets, 8-10 Reps!\nShoulder Press: 3 Sets, 8-12 Reps!\nSkull Crushers: 3 Sets, 8-10 Reps!\nCable Fly: 3 Sets, 12-15 Reps!```'
    pull = f'**__PULL WORKOUT:__**\n\n```Pull Ups: 3 Sets, 8-10 Reps!\nCable Pulldown: 3 Sets, 8-12 Reps!\nCurls: 3 Sets, 8-10 Reps!\nReverse Fly: 3 Sets, 12-15 Reps!```'
    leg = f'**__LEG WORKOUT:__**\n\n```Squats: 3 Sets, 8-10 Reps!\nSplit Squat: 3 Sets, 8-12 Reps!\nQuad Extensions: 3 Sets, 8-10 Reps!\nDead Lift: 3 Sets, 6-10 Reps!```'
    up = f'**__UPPER WORKOUT:__**\n\n```Bench Press: 3 Sets, 8-10 Reps!\nOverhead Press: 3 Sets, 8-12 Reps!\nSkull Crushers: 3 Sets, 8-10 Reps!\nCable Fly: 3 Sets, 12-15 Reps!```'
    await ctx.send("Click the buttons below to Select a Workout:", view=WorkoutButtons(str(up), str(low), str(push), str(pull), str(leg)))
    #THE await ctx.send SENDS THE MESSAGE AND EACH BUTTON
    #    **_text here__**     is bold and underlined in discord     ```text_here```    is boxed text in disc


#!FLIP COIN COMMAND
@bot.command()
async def flip(ctx: commands.Context):
    if randint(0,100) <= 50: 
        fc = f'You Rolled: Heads!'
    else:
        fc = f'You Rolled: Tails!'
    await ctx.send(fc)


#!ROLL COMMAND TO ROLL DICE
@bot.command()
async def roll(ctx: commands.Context):
    dr = f'You Rolled: {randint(1,6)}'
    await ctx.send(dr)


#IMPLEMENTING BODY SURVEY
class HeightSelect(discord.ui.Select):
    def __init__(self):
        options = [
                    discord.SelectOption(label="5'3 in.", value="53"),            
                    discord.SelectOption(label="5'4 in.", value="54"),
                    discord.SelectOption(label="5'5 in.", value="55"),
                    discord.SelectOption(label="5'6 in.", value="56"),
                    discord.SelectOption(label="5'7 in.", value="57"),
                    discord.SelectOption(label="5'8 in.", value="58"),
                    discord.SelectOption(label="5'9 in.", value="59"),
                    discord.SelectOption(label="5'10 in.", value="510"),
                    discord.SelectOption(label="5'11 in.", value="511"),
                    discord.SelectOption(label="6'0 in.", value="60"),
                    discord.SelectOption(label="6'1 in.", value="61"),
                    discord.SelectOption(label="6'2 in.", value="62"),
                    discord.SelectOption(label="6'3 in.", value="63"),
                    discord.SelectOption(label="6'5 in.", value="64"),
                    discord.SelectOption(label="6'6 in.", value="65"),
        ]
        super().__init__(options=options, placeholder="What is your height?", max_values=1)

    async def callback(self, interaction:discord.Interaction):
        await self.view.respond_to_answer2(interaction, self.values)


class WeightSelect(discord.ui.Select):
    def __init__(self):
        options = [
                    discord.SelectOption(label="110-119 lb.", value="110"),
                    discord.SelectOption(label="120-129 lb.", value="120"), 
                    discord.SelectOption(label="130-139 lb.", value="130"), 
                    discord.SelectOption(label="140-149 lb.", value="140"), 
                    discord.SelectOption(label="150-159 lb.", value="150"), 
                    discord.SelectOption(label="160-169 lb.", value="160"), 
                    discord.SelectOption(label="170-179 lb.", value="170"), 
                    discord.SelectOption(label="180-189 lb.", value="180"), 
                    discord.SelectOption(label="190-199 lb.", value="190"), 
                    discord.SelectOption(label="200-209 lb.", value="200"), 
                    discord.SelectOption(label="210-219 lb.", value="210"),
                    discord.SelectOption(label="220-229 lb.", value="220"), 
                    discord.SelectOption(label="230-239 lb.", value="230"),              
                   
        ]
        super().__init__(options=options, placeholder="What is your Weight?", max_values=1)

    async def callback(self, interaction:discord.Interaction):
        await self.view.respond_to_answer3(interaction, self.values)


#GAIN LOSE OR MAINTAIN WEIGHT QUESTION
class WorkoutGoal(discord.ui.Select):
    def __init__(self):
        options = [
                    discord.SelectOption(label="Gain Weight, Build Muscle", value="11"),            
                    discord.SelectOption(label="Maintain Weight, Build Muscle", value="22"),
                    discord.SelectOption(label="Lose Weight, Build Muscle", value="33"),
        ]
        super().__init__(options=options, placeholder="What is your training goal?", max_values=1)

    async def callback(self, interaction:discord.Interaction):
        await self.view.respond_to_answer4(interaction, self.values)


#AMOUNT OF WEIGHT TO GAIN OR LOSE QUESTION
class WeightAmount(discord.ui.Select):
    def __init__(self):
        options = [ 
                    discord.SelectOption(label="0 lb.", value="0"),
                    discord.SelectOption(label="5 lb.", value="5"),
                    discord.SelectOption(label="7.5 lb.", value="7"),
                    discord.SelectOption(label="10 lb.", value="10"),
                    discord.SelectOption(label="12.5 lb.", value="12"), 
                    discord.SelectOption(label="15 lb.", value="15"), 
                    discord.SelectOption(label="17.5 lb.", value="17"), 
                    discord.SelectOption(label="20 lb.", value="20"),
                    discord.SelectOption(label="22.5 lb.", value="22"),
                    discord.SelectOption(label="25 lb.", value="25"),         
                    
        ]
        super().__init__(options=options, placeholder="How much weight would you like to gain or lose?", max_values=1)

    async def callback(self, interaction:discord.Interaction):
        await self.view.respond_to_answer5(interaction, self.values)


#CREATE THE VIEW OF THE SURVEY AND THE ORDER OF QUESTIONS + HOW THEY WILL WORK
class SurveyView(discord.ui.View):
    answer1 = None 
    answer2 = None
    answer3 = None 
    answer4 = None
    answer5 = None 
    
    @discord.ui.select(
        placeholder="What is your age?",
        options=[
            discord.SelectOption(label="13 - 17", value="13"),
            discord.SelectOption(label="18 - 23", value="18"),
            discord.SelectOption(label="24 - 30", value="24"),
            discord.SelectOption(label="31 - 45", value="31")
        ]        
    )
    async def select_age(self, interaction: discord.Interaction, select_item : discord.ui.Select):   #dropdown for age
        self.answer1 = select_item.values           #set answer 1 to items value
        self.children[0].disabled= True             #disables changing answer
        height_select = HeightSelect()              #call height select next
        self.add_item(height_select)                #add height item to self
        await interaction.message.edit(view=self)   #wait for the message interact
        await interaction.response.defer()          #defer response until after survey

    async def respond_to_answer2(self, interaction : discord.Interaction, choices): #height
        self.answer2 = choices 
        self.children[1].disabled= True
        weight_select = WeightSelect()          #add next dropdown call
        self.add_item(weight_select)
        await interaction.message.edit(view=self)
        await interaction.response.defer()

    async def respond_to_answer3(self, interaction : discord.Interaction, choices):  #weight
        self.answer3 = choices 
        self.children[2].disabled= True
        workout_goal = WorkoutGoal()
        self.add_item(workout_goal)
        await interaction.message.edit(view=self)
        await interaction.response.defer()
    
    async def respond_to_answer4(self, interaction : discord.Interaction, choices): #goal
        self.answer4 = choices 
        self.children[3].disabled= True
        weight_goal = WeightAmount()
        self.add_item(weight_goal)
        await interaction.message.edit(view=self)
        await interaction.response.defer()

    async def respond_to_answer5(self, interaction: discord.Interaction, choices):  #how much gain or lose
        self.answer5 = choices 
        self.children[4].disabled = True
        await interaction.message.edit(view=self)
        await interaction.response.defer()
        self.stop()
        

#CALCULATE MACROS FOR RESULT
def calculate_macronutrient_goals(weight_goal: float, height: float, weight: int, age: int):
    # calculate Total Daily Energy Expenditure [TDEE]
    if age <= 30:
        bmr = 10 * weight + 6.25 * height - 5 * age + 5  # BMR for ages <= 30
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161  # BMR for ages > 30

    if weight_goal == 11:  # gain weight
        tdee = bmr * 1.2  # activity level
        calories = tdee + 1100  # add surplus calories for weight gain
    elif weight_goal == 33:  # lose weight
        tdee = bmr * 1.2  # activity level
        calories = tdee - 400  # subtract deficit calories for weight loss
    else:  # maintain weight
        tdee = bmr * 1.375  # activity level
        calories = tdee + 400

    # calculate macronutrient amounts
    protein = weight * 1.3  # Protein intake in grams
    fat = (calories * 0.25) / 9  # Fat intake in grams

    # ensure carbohydrates are not negative
    carbohydrates = max((calories - (protein * 4) - (fat * 9)) / 4, 0)  # Carbs in grams

    # calculate total recommended calories for macros
    total_recommended_calories = protein * 4 + fat * 9 + carbohydrates * 4

    return protein, fat, carbohydrates, total_recommended_calories


# class for logging workouts
class LogWorkoutView(discord.ui.View):
    async def log_workout(self, interaction: discord.Interaction, workout_type: str):
        user_id = interaction.user.id
        try:
            result = collection.update_one({"_id": user_id}, {"$inc": {f"{workout_type}_count": 1}})
            if result.modified_count == 0:
                print("User document not found. Creating account...")
                await create_account(user_id)  # Call create_account if the user document doesn't exist
            else:
                print(f"Updated {workout_type} count:", result.modified_count)
            await interaction.response.edit_message(content=f"Workout logged: {workout_type}")
        except Exception as e:
            print("An error occurred while logging workout:", e)


# implement !log command
@bot.command()
async def log(ctx):
    user_id = ctx.author.id
    view = WorkoutButtons("Upper Body Workout", "Lower Body Workout", "Push Workout", "Pull Workout", "Legs Workout", user_id)
    await ctx.send("Select the workout you want to log:", view=view)


# Implement the !progress Command
@bot.command()
async def progress(ctx):
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

# implement !resetlog command
@bot.command()
async def resetlog(ctx):
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


#!MACROS COMMAND
@bot.command()
async def macros(ctx):
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


async def create_account(user_id):
    try:
        find = collection.find_one({"_id": user_id})
    except Exception as e:
        print("An error occurred while querying the database:", e)
        return

    if find is not None:
        print("User already exists.")
        return

    print("Creating account for user:", user_id)
    try:
        result = collection.insert_one({
            "_id": user_id,
            "protein": 0,
            "fat": 0,
            "carbohydrates": 0,
            "total_calories": 0,
            "upper_count": 0,
            "lower_count": 0,
            "push_count": 0,
            "pull_count": 0,
            "legs_count": 0,
        })
        print("Inserted new document:", result.inserted_id)
    except Exception as e:
        print("An error occurred while creating an account:", e)


# STORE MACROS ACCOUNT FUNCTION
async def store_macros(user_id, protein, fat, carbohydrates, total_calories):
    try:
        result = collection.update_one({"_id": user_id}, {"$set": {
            "protein": protein,
            "fat": fat,
            "carbohydrates": carbohydrates,
            "total_calories": total_calories
        }})
        if result.modified_count == 0:
            print("User document not found. Creating account...")
            await create_account(user_id)  # Call create_account if the user document doesn't exist
        else:
            print("Updated document:", result.modified_count)
    except Exception as e:
        print("An error occurred while storing macros:", e)


# SURVEY COMMAND
@bot.command()
async def survey(ctx):

    user_id = ctx.author.id  # Get the user's ID

    view = SurveyView()  # set to view the above class
    message = await ctx.send("**__Please complete the survey:__**", view=view)
    await view.wait()

    # retrieve the selected values from users answer choices
    age = int(view.answer1[0])
    height = float(view.answer2[0])
    weight = int(view.answer3[0])
    weight_goal = float(view.answer4[0])

    # calculate macros
    protein, fat, carbohydrates, total_calories = calculate_macronutrient_goals(weight_goal, height, weight, age)

    # STORE MACROS IN THE DATABASE
    await store_macros(user_id, protein, fat, carbohydrates, total_calories)

    # format the result message
    result_message = f"**__Here are your daily macronutrient goals:__**\n\n```Protein: {protein:.2f}g\nFat: {fat:.2f}g\nCarbohydrates: {carbohydrates:.2f}g\nTotal Calories: {total_calories:.2f}```"

    # send the result message below the survey
    await ctx.send(result_message)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="**__Command List__**", description="```List of available commands:```", color=discord.Color.blue())
    embed.add_field(name="**__!workout__**", value=" - Display workout options.", inline=False)
    embed.add_field(name="**__!flip__**", value=" - Flip a coin.", inline=False)
    embed.add_field(name="**__!roll__**", value=" - Roll a dice.", inline=False)
    embed.add_field(name="**__!log__**", value=" - Log a workout.", inline=False)
    embed.add_field(name="**__!progress__**", value=" - Show workout progress.", inline=False)
    embed.add_field(name="**__!resetlog__**", value=" - Reset all workout logs.", inline=False)
    embed.add_field(name="**__!macros__**", value=" - Display daily macronutrient goals.", inline=False)
    embed.add_field(name="**__!survey__**", value=" - Complete a survey to calculate macronutrient goals.", inline=False)
    await ctx.send(embed=embed)


# MAIN ENTRY POINT/ RUN BOT
bot.run(TOKEN)





