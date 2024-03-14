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

#took buttons out of gamble commands for now
'''class GambleButtons(discord.ui.View):
    def __init__(self, rd: str, fc: str):
        super().__init__()
        self.rd = rd
        self.fc = fc

    @discord.ui.button(label="Roll Die", style=discord.ButtonStyle.blurple)
    async def Btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(self.rd, ephemeral=False)
    @discord.ui.button(label="Flip Coin", style=discord.ButtonStyle.blurple)
    async def Btn1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(self.fc, ephemeral=False)'''

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

    


# MAIN ENTRY POINT/ RUN BOT
bot.run(TOKEN)





