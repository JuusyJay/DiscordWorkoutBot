import discord
from discord.ext import commands
import pymongo
from database import URI
from utils import store_macros, calculate_macronutrient_goals



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


#OPTIONS TO SELECT WEIGHT IN SURVEY
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



class SurveyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = pymongo.MongoClient(URI)
        self.db = self.client['workoutDB']
        self.collection = self.db['user_accounts']

    @commands.command()
    async def survey(self, ctx):
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

async def setup(bot):
    await bot.add_cog(SurveyCog(bot))
