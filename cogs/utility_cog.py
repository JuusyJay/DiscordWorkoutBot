import discord
from discord.ext import commands
from random import randint


class UtilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def flip(self, ctx):
        if randint(0,100) <= 50: 
            fc = f'You Rolled: Heads!'
        else:
            fc = f'You Rolled: Tails!'
        await ctx.send(fc)

    @commands.command()
    async def roll(self, ctx):
        dr = f'You Rolled: {randint(1,6)}'
        await ctx.send(dr)

    @commands.command()
    async def help(self, ctx):
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

async def setup(bot):
    await bot.add_cog(UtilityCog(bot))
