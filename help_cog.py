import discord
from discord.ext import commands

class helpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = """
```
General commands:
&help - DISPLAYS ALL MY SHIT.
&p <search or url> - PLAYS YOUR SHITTY HUMAN "MUSIC".
&q - SHOWS ALL TAINTCHAFING EAR-ASSAULTING GRUBFUCK TRACKS.
&skip - SKIPS YOUR CURRENT SONG. THANK FUCK.
&clear - REMOVES ALL YOUR SHIT. AGAIN, THANK FUCK.
&leave - I LEAVE. FUCKING FINALLY.
&pause - HALTS YOUR BARAGE OF NOISE. HOPEFULLY FOREVER.
&resume - I DON'T REALLY THINK I HAVE TO SAY WHAT THIS DOES, I'M KIND OF TIRED OF DOING THAT.
```
"""

    @commands.command(name="help", help="Displays all the available commands")
    async def help(self, ctx):
        await ctx.send(self.help_message)
