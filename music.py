import discord
from discord.ext import commands
from lol_db_connector import lol_db
from youtube_dl import YoutubeDL
import random
import config
class music_cog(commands.Cog):
    def __init__(self, bot, db: lol_db):
        self.bot = bot
        self.db = db
        #all the music related stuff
        self.is_playing = False
        self.loop = False

        # 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn', 'executable':config.FFMPEG_EXE}

        self.vc = ""
        self.esport_mode = False

     #searching the item on youtube
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            #get the first url
            m_url = self.music_queue[0][0]['source']

            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    # infinite loop checking 
    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            
            #try to connect to voice channel if you are not already connected

            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            print(self.music_queue)
            #remove the first element as you are currently playing it
            if self.loop:
                self.music_queue.append(self.music_queue[0])
            self.music_queue.pop(0)

            #self.vc.play(discord.FFmpegPCMAudio(executable="C:/path/ffmpeg.exe", source="mp3.mp3"))
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command(name="esportMode", help="Toggle esport mode")
    async def esportModeToggle(self, ctx, *args):
        self.esport_mode = not self.esport_mode
        await ctx.send('ESPORTMODE: ' + self.esport_mode)

    @commands.command(name="play", help="Plays a selected song from youtube")
    async def p_helper(self, ctx, *args):
        query = " ".join(args)
        text_channel = ctx.channel
        voice_channel = ctx.author.voice.channel
        await self.p(query,voice_channel,text_channel, True)

    async def p(self, query, voice_channel, text_channel, do_print):
        if voice_channel is None:
            #you need to be connected so that the bot knows where to go
            if do_print:
                await text_channel.send("Connect to a voice channel!")
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                if do_print:
                    await text_channel.send("Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.")
            else:
                if do_print:
                    await text_channel.send("Song added to the queue")
                self.music_queue.append([song, voice_channel])
                
                if self.is_playing == False:
                    await self.play_music()


    @commands.command(name="worldsFM", help="HERE WE ARRRREEEE DONT TURN AWAYY NOW")
    async def worldsfm_helper(self, ctx, *args):
        voice_channel = ctx.author.voice.channel
        text_channel = ctx.channel
        self.worldsfm(voice_channel,text_channel,True)

    async def worldsfm(self,voice_channel,text_channel,send_text):
        musicList = self.db.getWorldsFM()
        random.shuffle(musicList)
        if voice_channel is None:
            #you need to be connected so that the bot knows where to go
            if send_text:
                await text_channel.send("Connect to a voice channel!")
        else:
            for song in musicList:
                song = self.search_yt(song[1])
                if type(song) == type(True):
                    if send_text:
                        await text_channel.send("Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.")
                else:
                    self.music_queue.append([song, voice_channel])
                    
                    if self.is_playing == False:
                        await self.play_music()
            if send_text:
                await text_channel.send("To dopiero początek drogi na szczyt")

    @commands.command(name="queue", help="Displays the current songs in queue")
    async def q(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += self.music_queue[i][0]['title'] + "\n"

        print(retval)
        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue")

    @commands.command(name="skip", help="Skips the current song being played")
    async def skip_helper(self, ctx):
        self.skip()

    async def skip(self):
        if self.vc != "" and self.vc:
            self.vc.stop()
            #try to play next in the queue if it exists
            await self.play_music()

    async def clear(self):
        #try to play next in the queue if it exists
        while len(self.music_queue) > 0:
            self.music_queue.pop()
        await self.skip()

    @commands.command(name="loop", help="Toggles loop")
    async def switch_loop(self, ctx):
        self.loop = not self.loop
        await ctx.send("Looping songs: " + str(self.loop))
