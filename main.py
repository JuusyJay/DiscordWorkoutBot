import discord
from typing import Final
import os
from dotenv import load_dotenv
from discord.ext import commands
from random import choice, randint


#TELLS BOT THAT COMMANDS START WITH "!" AND GIVES INTENT/PERMISSIONS TO ALL FOR BOT
bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())


#LOAD OUR TOKEN FROM SAFE PLACE :D uwu poosy
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')


# ALSO CALLS BOT EVENT TO DISPLAY IN CONSOLE THAT BOT IS CONNECTED
@bot.event
async def on_ready():
    print("Jotaro has connected to Discord!")


#TESTING  WORKOUT BUTTONS:
class WorkoutButtons(discord.ui.View):
    def __init__(self, up: str, low: str, push: str, pull: str, leg: str): #Str intake for each button to display when pressed
        super().__init__()
        self.up = up
        self.low = low
        self.push = push
        self.pull = pull
        self.leg = leg

    #CREATES ALL THE BUTTONS TO DISPLAY AND LABELS THEM, STYLES THEM TOO
    @discord.ui.button(label="Upper Body", style=discord.ButtonStyle.blurple)
    async def Btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(self.up, ephemeral=False) # ephemeral means if others can see the button output response or only person who clicks
    @discord.ui.button(label="Lower Body", style=discord.ButtonStyle.blurple)
    async def Btn1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(self.low, ephemeral=False)
    @discord.ui.button(label="Push", style=discord.ButtonStyle.blurple)
    async def Btn2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(self.push, ephemeral=False)
    @discord.ui.button(label="Pull", style=discord.ButtonStyle.blurple)
    async def Btn3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(self.pull, ephemeral=False)
    @discord.ui.button(label="Legs", style=discord.ButtonStyle.blurple)
    async def Btn4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(self.leg, ephemeral=False)



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


#  IMPLEMENTING BODY SURVEY
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
    async def select_age(self, interaction:discord.Interaction, select_item : discord.ui.Select):   #dropdown for age
        self.answer1 = select_item.values   #set answer 1 to items value
        self.children[0].disabled= True   #disables changing answer
        height_select = HeightSelect()  #call height select next
        self.add_item(height_select)    #add height item to self
        await interaction.message.edit(view=self)   #wait for the message interact
        await interaction.response.defer()      #defer response until after survey
             
    async def respond_to_answer2(self, interaction : discord.Interaction, choices):
        self.answer2 = choices 
        self.children[1].disabled= True
        weight_select = WeightSelect()          #add next dropdown call
        self.add_item(weight_select)
        await interaction.message.edit(view=self)
        await interaction.response.defer()

    async def respond_to_answer3(self, interaction : discord.Interaction, choices):
        self.answer3 = choices 
        self.children[2].disabled= True
        workout_goal = WorkoutGoal()
        self.add_item(workout_goal)
        await interaction.message.edit(view=self)
        await interaction.response.defer()
    
    async def respond_to_answer4(self, interaction : discord.Interaction, choices):
        self.answer4 = choices 
        self.children[3].disabled= True
        weight_goal = WeightAmount()
        self.add_item(weight_goal)
        await interaction.message.edit(view=self)
        await interaction.response.defer()

    async def respond_to_answer5(self, interaction: discord.Interaction, choices):
        self.answer5 = choices 
        self.children[4].disabled = True
        await interaction.message.edit(view=self)
        await interaction.response.defer()
        self.stop()
        

# CALCULATE MACROS FOR RESULT
def calculate_macronutrient_goals(weight_goal: float, height: float, weight: int, age: int):

    # Calculate Total Daily Energy Expenditure (TDEE)
    if age <= 30:
        bmr = 10 * weight + 6.25 * height - 5 * age + 5     # Basal Metabolic Rate (BMR) for ages <= 30
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161   # BMR for ages > 30


    
    if weight_goal == 11:               # Gain weight
        tdee = bmr * 1.2                # activity level
        calories = tdee + 1100          # Add surplus calories for weight gain

    elif weight_goal == 33:             # Lose weight
        tdee = bmr * 1.2                # activity level
        calories = tdee - 400           # Subtract deficit calories for weight loss

    else:                               # Maintain weight
        tdee = bmr * 1.375              # activity level
        calories = tdee + 400

    
    # Calculate macronutrient amounts
    protein = weight * 1.3          # Protein intake (in grams)
    fat = (calories * 0.25) / 9     # Fat intake (in grams)


    # Ensure carbohydrates are not negative
    carbohydrates = max((calories - (protein * 4) - (fat * 9)) / 4, 0)  # Carbohydrate intake (in grams)

    # Calculate total recommended calories for macros
    total_recommended_calories = protein * 4 + fat * 9 + carbohydrates * 4

    return protein, fat, carbohydrates, total_recommended_calories



#!SURVEY COMMAND
@bot.command()
async def survey(ctx):
    view = SurveyView()    # Set to view the above class 
    message = await ctx.send("**__Please complete the survey:__**", view=view)
        
    await view.wait()

    # Retrieve the selected values from users answer choices
    age = int(view.answer1[0])
    height = float(view.answer2[0])
    weight = int(view.answer3[0])
    weight_goal = float(view.answer4[0])
    

    # Calculate macros
    protein, fat, carbohydrates, total_calories = calculate_macronutrient_goals(weight_goal, height, weight, age)

    # Format the result message 
    result_message = f"**__Here are your daily macronutrient goals:__**\n\n```Protein: {protein:.2f}g\nFat: {fat:.2f}g\nCarbohydrates: {carbohydrates:.2f}g\nTotal Calories: {total_calories:.2f}```"

    # Send the result message below the survey
    await ctx.send(result_message)


# MAIN ENTRY POINT/ RUN BOT
bot.run(TOKEN)





