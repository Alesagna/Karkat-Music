import discord
from discord.ext import commands
import time
from help_cog import helpCog
from music_cog import musicCog


bot = commands.Bot(command_prefix='&')
token = " " #Add your own parameters here

bot.remove_command('help')

bot.add_cog(helpCog(bot))
bot.add_cog(musicCog(bot))

@bot.event
async def on_ready():
    activity = discord.Game(name="SGRUB", type=3)
    await bot.change_presence(activity=activity)
    print("Bot is running!")

@bot.event
async def on_voice_state_update(member, before, after):
    voice_state = member.guild.voice_client
    if voice_state is None:
        return 

    if len(voice_state.channel.members) == 1:
        time.sleep(5)
        await voice_state.disconnect()
        musicCog(bot).musicQueue =[]

bot.run(token)
