from lib import *
import discord
from discord.ext import commands
import config

class lol_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.watcher = riot.LolWatcher(config.RIOT_API_KEY)
        self.region = 'EUN1'
        self.region2 = 'EUROPE' #rozne metody wymagaja roznych nazewnictw... (jesli wykorzystujesz puuid to bierzesz region2)


    #@commands.command(name="summinfo", help="Display summoners info")
    #async def summoners_info(self, context, *arguments):
    #    query = " ".join(arguments)
    #    print(query)
    #    summoner = self.watcher.summoner.by_name(self.region, query)
    #    print(summoner)
    #    stats = self.watcher.league.by_summoner(self.region, summoner['id'])
    #    print(stats)

    def get_puuid(self,name):
        summ = self.watcher.summoner.by_name(self.region, name)
        id = summ['id']
        return id

    def get_ranked_stats(self,id):
        ranked_stats = self.watcher.league.by_summoner(self.region, id)
        return ranked_stats

    def test(self):
        summ = self.watcher.summoner.by_name(self.region, 'Ruby SuperStar')
        id = summ['puuid']
        gp_gold = 0
        sum_gold = 0
        number_of_matches = 0
        licz = 0
        matches = self.watcher.match_v5.matchlist_by_puuid(self.region2,id,0,100,'ranked')
        for match in matches:
            licz += 1
            print(licz)
            detail = self.watcher.match_v5.by_id(self.region2,match)
            info = detail['info']
            if(info['gameMode'] != 'CLASSIC'):
                continue
            parts = info['participants']
            # print(match)
            for i in parts:
                if(i['puuid']==id):
                    # print(i['championName'], i['kills'], i['deaths'], i['assists'])
                    gp_gold += int(i['goldEarned'])
                    # print(gp_gold)
                sum_gold += int(i['goldEarned'])
            number_of_matches += 1
            # print(info['gameType'],info['gameMode'])
            # print('____________________')
        print('test')
        print(f'Zloto pro gracza: {gp_gold/number_of_matches}')
        print(f'Zloto reszty graczy: {sum_gold/(number_of_matches*10)}')

    def getSoloQStats(self,allQueuesStats):
        for queue in allQueuesStats:
            if queue['queueType'] == 'RANKED_SOLO_5x5':
                return queue
        return None
        



        
