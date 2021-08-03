from os import read
import requests
# LeagueClient:14884:60391:-JVG48vOqzW5Ry92hQ_k-Q:https
import asyncio
import config
import music
async def client_watcher(bot,music : music.music_cog):
    lockfile_loc = config.LOL_CLIENT_LOCKFILE
    bol = True
    while bol: #OH GOD IT DOESNT EVEN WORK
        try:
            port,password = await read_lockfile(lockfile_loc)
            bol = False
        except:
            pass
    # verify_file = 'riotgames.pem'
    print('Startowanie client watchera')
    current_stage = 'None'
    guild = bot.get_guild(config.ESPORT_GUILD)
    channel = guild.get_channel(config.ESPORT_VOICE_CHANNEL)
    text_channel = guild.get_channel(config.ESPORT_TEXT_CHANNEL)
    while True:
        if music.esport_mode:
            await asyncio.sleep(5)
            continue
            
        if current_stage == 'Game':
            await asyncio.sleep(60)
        else:
            await asyncio.sleep(2)
        try:
            # a = requests.get('https://127.0.0.1:'+port+'/lol-champ-select/v1/session', verify=False ,auth=('riot',password))
            b = requests.get('https://127.0.0.1:'+port+'/lol-gameflow/v1/session', verify=False ,auth=('riot',password))
            # a = requests.get('https://127.0.0.1:'+port+'/lol-champ-select/v1/session', verify=verify_file ,auth=('riot',password))
            # data = a.json()
            datb = b.json()
            # print(data)
            # print(test)
            # try:
            isInChampionSelect = False
            isInGame = False
            isInEndOfGame = False
            if 'httpStatus' not in datb:
                if datb['phase'] == 'InProgress':
                    isInGame = True
                elif datb['phase'] == 'ChampSelect':
                    isInChampionSelect = True
                elif datb['phase'] == 'EndOfGame':
                    isInEndOfGame = True
            else:
                current_stage = 'None'
            
            # print(isInGame)
            # print(isInChampionSelect)
            # print(current_stage)

            if not isInChampionSelect and not isInGame:
                current_stage = 'None' #Jeszcze trzeba sprawdzic czy w grze i odpalzzic worldsfm jesli tak
                # print('no champion select')
                await music.clear()
            elif isInChampionSelect and current_stage != 'ChampionSelect':
                current_stage = 'ChampionSelect'
                await music.p("https://www.youtube.com/watch?v=ek-672uRnhQ",channel,text_channel,False)
            elif isInGame and current_stage != 'Game':
                current_stage = 'Game'
                await music.clear()
                await music.worldsfm(channel,text_channel,False)
                # await music.p("https://www.youtube.com/watch?v=nCFiVxCADEY",channel,text_channel,False)
            elif isInEndOfGame and current_stage != 'EndOfGame':
                current_stage = 'EndOfGame'
                await music.clear()
                # await music.worldsfm(channel,text_channel,False)
                # await music.p("https://www.youtube.com/watch?v=3suGfhnT2Sg",channel,text_channel,False)

        except FileNotFoundError:
            port,password = await read_lockfile()

async def read_lockfile(lockfile_loc):
    f = open(lockfile_loc, "r")
    lockfile = f.read()
    lockfile = lockfile.split(':')
    # print(lockfile)
    port = lockfile[2]
    password = lockfile[3]
    return port,password