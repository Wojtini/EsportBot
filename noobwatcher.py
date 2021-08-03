import asyncio
import config
from lol_db_connector import lol_db
from riot_lol import lol_cog
import discord

class noob_watcher():
    def __init__(self, bot, lc: lol_cog, db: lol_db):
        self.bot = bot
        self.lc = lc
        self.db = db
        self.running = True

        # założenie: im mniejszy index tym mniejsza ranga
        self.tiers = ['IV','III','II','I']
        self.divisions = ['IRON','BRONZE','SILVER','GOLD','PLATINUM','DIAMOND','MASTER','GRANDMASTER','CHALLENGER']

    async def watch(self):
        while True:
            # print('Petla NoobWatchera')
            # await asyncio.sleep(60*1)
            # wez wszystkich graczy
            players = self.db.getAllPlayers()
            for player in players:
                await asyncio.sleep(60*5)
                rankedStats = self.lc.get_ranked_stats(player['id'])
                soloQStats = self.lc.getSoloQStats(rankedStats)
                curr_division = soloQStats['tier']
                curr_tier = soloQStats['rank']
                try:
                    result = self.compare(player['division'],player['tier'],curr_division,curr_tier)
                except:
                    result = "Error"
                # print(result)
                #sprawdz aktualna range
                #jesli inna zaktualizuj i jesli nizsza to zrob beke z type
                if result != "NONE":
                    print('aktdddddd: ' + player['playerName'])
                    await self.notify(player['discordid'],player['playerName'],result,curr_division,curr_tier,player['division'],player['tier'])
                    self.db.updateProPlayer(player['id'],curr_division,curr_tier)
            await asyncio.sleep(60*10)

    async def notify(self,dsc_id,dsc_name,reason,curr_division,curr_tier,old_division,old_tier):
        guild = self.bot.get_guild(config.NW_GUILD)
        channel = guild.get_channel(config.NW_TEXT_CHANNEL)
        if(reason == 'TIER_DOWN' or reason == 'DIV_DOWN'):
            print("notification " + dsc_id + " " + reason)
            embed=discord.Embed(title='League of Legends', description='Gracz ' + dsc_name + ' spadł z ' + old_division + ' ' + old_tier + ' do ' + curr_division + ' ' + curr_tier, color=0xff0000)
            embed.set_author(name='Teraz Drużyna', icon_url='https://img.rankedboost.com/wp-content/uploads/2020/10/Challenger-Summoner-Icon-Season-10-Reward.jpg')
            embed.set_thumbnail(url='https://blog.cdn.own3d.tv/resize=fit:crop,height:400,width:600/pKwIyI8RyGtPW35ZFg2m')
            embed.add_field(name='Nie poddawaj się', value='to tylko kilka gier w których twoja losowa drużyna przegrała, ale TY wygrałeś bo dzięki niej stałeś się lepszy', inline=False)
            embed.set_footer(text='Bo jeśli nie ty to kto?')
            await channel.send(embed=embed)
        if(reason == 'TIER_UP' or reason == 'DIV_UP'):
            print("notification " + dsc_id + " " + reason)
            embed=discord.Embed(title='League of Legends', description='Gracz ' + dsc_name + ' awansował z ' + old_division + ' ' + old_tier + ' do ' + curr_division + ' ' + curr_tier, color=0xff0000)
            embed.set_author(name='Teraz Drużyna', icon_url='https://img.rankedboost.com/wp-content/uploads/2020/10/Challenger-Summoner-Icon-Season-10-Reward.jpg')
            embed.set_thumbnail(url='https://blog.cdn.own3d.tv/resize=fit:crop,height:400,width:600/pKwIyI8RyGtPW35ZFg2m')
            embed.add_field(name='GRATULACJE', value='ale nie spoczywaj na laurach, to dopiero początek twojej esportowej przygody', inline=False)
            embed.set_footer(text='Bo jeśli nie ty to kto?')
            await channel.send(embed=embed)
            

    def compare(self,old_div,old_tier,curr_div,curr_tier):
        if self.divisions.index(curr_div) < self.divisions.index(old_div):
            return "DIV_DOWN"
        if self.divisions.index(curr_div) > self.divisions.index(old_div):
            return "DIV_UP"
        if self.tiers.index(curr_tier) < self.tiers.index(old_tier):
            return "TIER_DOWN"
        if self.tiers.index(curr_tier) > self.tiers.index(old_tier):
            return "TIER_UP"
        return "NONE"
