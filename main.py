

#'NzE4MDk2MjYyNzkyMjE2NTc2.Xtj5Qg.jdGCYQgyRboC4InyiY0tcEPUgJg' -- discord api
from lib import *
from music import music_cog
from riot_lol import lol_cog
from discord_std import dsc_std_cog
from lol_db_connector import lol_db
from noobwatcher import noob_watcher
import lol_client_connector
import urllib3
import config
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# discord bot conf
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)

lolDB = lol_db()
bot.command_prefix = '$'
lc = lol_cog(bot)
mc = music_cog(bot,lolDB)
dsc_cog = dsc_std_cog(bot,lc,lolDB,mc)
bot.add_cog(mc)
bot.add_cog(lc)
bot.add_cog(dsc_cog)

#this runs on bot startup
nw = noob_watcher(bot,lc,lolDB)

@bot.event
async def on_ready():
    print('Running cleanup')
    await dsc_cog.clearChannels()

    botactivity = discord.Activity(type=discord.ActivityType.watching, name="music under maintance")
    await bot.change_presence(activity=botactivity, status=discord.Status.do_not_disturb)

    print('Bot Started')
    bot.loop.create_task(nw.watch())
    bot.loop.create_task(lol_client_connector.client_watcher(bot,mc))

#dodaj taska

#przeniesc do jakiejs klasy
@bot.event
async def on_reaction_add(reaction, user):
    if user.id == 718096262792216576:
        return
    if dsc_cog.listen_msg[str(reaction.message.id)] is None:
        return
    dsc_id = dsc_cog.listen_msg[str(reaction.message.id)]

    print(dsc_id)

    guild = reaction.message.guild
    member = guild.get_member(int(dsc_id))
    print(member)

    embed=discord.Embed(title='League of Legends', description='Twoja drużyna cię potrzebuje', color=0xff0000)
    embed.set_author(name='Teraz Drużyna', icon_url='https://img.rankedboost.com/wp-content/uploads/2020/10/Challenger-Summoner-Icon-Season-10-Reward.jpg')
    embed.set_thumbnail(url='https://blog.cdn.own3d.tv/resize=fit:crop,height:400,width:600/pKwIyI8RyGtPW35ZFg2m')
    embed.set_footer(text='Bo jeśli nie ty to kto?')
    
    await member.send(embed=embed)
    await reaction.message.edit(content = "Wezwano gracza: " + member.mention, embed = None)

    dsc_cog.listen_msg[str(reaction.message.id)] = None

print("Bot Starting")
bot.run(config.DISCORD_TOKEN)