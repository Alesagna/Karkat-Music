from ast import alias
from turtle import title
import discord
from discord.ext import commands

from youtube_dl import YoutubeDL

class musicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.isPlaying = False
        self.isPaused = False

        self.musicQueue = []
        self.ydlOptions = {'format': 'bestaudio', 'noplaylist':'True'}
        self.ffmpegOptions = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None

    def searchYT(self, item):
        with YoutubeDL(self.ydlOptions) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def playNext(self):
        if len(self.musicQueue) > 0:
            self.isPlaying = True

            m_url = self.musicQueue[0][0]['source']

            self.musicQueue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.ffmpegOptions), after=lambda e: self.playNext())
        else:
            self.isPlaying = False

    async def playSong(self, ctx):
        if len(self.musicQueue) > 0:
            self.isPlaying = True

            m_url = self.musicQueue[0][0]['source']
            
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.musicQueue[0][1].connect()

                if self.vc == None:
                    await ctx.send("I CAN'T JOIN, ASSHOLE.")
                    return
            else:
                await self.vc.move_to(self.musicQueue[0][1])
            
            self.musicQueue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.ffmpegOptions), after=lambda e: self.playNext())
        else:
            self.isPlaying = False

    @commands.command(name="play", aliases=["p","playing"])
    async def play(self, ctx, *args):
        query = " ".join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel is False:
            await ctx.send("COULD YOU USE YOUR THINKING FLESH MOUND AND JOIN A CHANNEL FIRST?")
        elif self.isPaused:
            self.vc.resume()
        else:
            song = self.searchYT(query)
            if type(song) == type(True):
                await ctx.send("COULDN'T GET WHATEVER THE FUCK THAT WAS. REMEMBER: NO PLAYLISTS AND YOUTUBE ONLY, ASSCLOWN.")
            else:
                await ctx.send("ADDED THAT SHIT TO THE QUEUE.")
                self.musicQueue.append([song, voice_channel])

                if self.isPlaying == False:
                    await self.playSong(ctx)
            
    @commands.command(name="pause")
    async def pause(self, ctx, *args):
        if self.isPlaying:
            self.isPlaying = False
            self.isPaused = True
            await ctx.send("PAUSING, OR WHATEVER THE FUCK.")
            self.vc.pause()
        elif self.isPaused:
            self.isPaused = False
            self.isPlaying = True
            self.vc.resume()

    @commands.command(name = "resume", aliases=["r"])
    async def resume(self, ctx, *args):
        if self.isPaused:
            self.isPaused = False
            self.isPlaying = True
            await ctx.send("RESUMING, OR SOMETHING. I DON'T CARE.")
            self.vc.resume()

    @commands.command(name="skip", aliases=["s"])
    async def skip(self, ctx):
        if self.vc != None and self.vc:
            await ctx.send("DON'T CARE, NEXT.")
            self.vc.stop()

            await self.playSong(ctx)


    @commands.command(name="queue", aliases=["q"])
    async def queue(self, ctx):
        queue = ""
        await ctx.send("UP NEXT ON THE PRIMITIVE, SHAMEFUL RAZZMATAZZ OF GO FUCK YOURSELF IS: \n")
        for i in range(0, len(self.musicQueue)):
            queue += f"{i+1}. {self.musicQueue[i][0]['title']} \n"

        if queue != "":
            await ctx.send(queue)
        else:
            await ctx.send("NOTHING. NO UPCOMING SONGS.")

    @commands.command(name="clear", aliases=["c", "bin"])
    async def clear(self, ctx):
        self.musicQueue = []
        await ctx.send("HOLY SHIT. THANK FUCK.")

    @commands.command(name="leave", aliases=["disconnect", "l", "d"])
    async def dc(self, ctx):
        self.isPlaying = False
        self.isPaused = False
        await ctx.send("WHATEVER.")
        await self.vc.disconnect()
        self.vc = None
        self.musicQueue = []
