from lib import *
import config

class lol_db():
    def __init__(self):
        self.connection = mysql.connector.connect(user=config.DB_USER, password=config.DB_PASSWORD,
                              host=config.DB_HOST,
                              database=config.DB_DATABASE)
    
    def query(self):
        cursor = self.connection.cursor()
        query = ("SELECT * FROM czygpoddaje")
        cursor.execute(query)
        for (a,b) in cursor:
            print(a,b)
        cursor.close()

    def updateProPlayer(self,id,division,tier):
        cursor = self.connection.cursor()
        sql = " UPDATE pro_gracze SET division = '" + division + "', tier = '" + tier + "' WHERE id = '" + id + "'"
        #val = (id,division,tier)
        cursor.execute(sql)
        
        self.connection.commit()

        cursor.close()

    def addProPlayer(self,id,discordid,playerName,division,tier):
        cursor = self.connection.cursor()

        sql = "INSERT INTO pro_gracze (id,discordid,playerName,division,tier) VALUES (%s, %s, %s, %s, %s)"
        val = (id,discordid,playerName,division,tier)
        cursor.execute(sql, val)
        
        self.connection.commit()

        cursor.close()

    def addMusic(self,url,userName):
        cursor = self.connection.cursor()
        print(url)
        sql = "INSERT INTO worldsfm (url,user_who_added) VALUES (%s, %s)"
        val = (url,userName)
        cursor.execute(sql, val)
        self.connection.commit()
        cursor.close()

    def addMusicNostalgic(self,url,userName):
        cursor = self.connection.cursor()
        print(url)
        sql = "INSERT INTO nostalgic (nazwa,who_added) VALUES (%s, %s)"
        val = (url,userName)
        cursor.execute(sql, val)
        self.connection.commit()
        cursor.close()

    def getDiscordIds(self):
        cursor = self.connection.cursor()
        query = ("SELECT * FROM pro_gracze")
        cursor.execute(query)
        columns = cursor.description 
        result = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
        cursor.close()
        return result

    def addSubChannel(self,guildId,guildName,channelId,channelName):
        cursor = self.connection.cursor()
        sql = "INSERT INTO esport_channels (nazwa_kanalu,nazwa_gildii,id_kanalu,id_gildii) VALUES (%s, %s, %s, %s)"
        val = (channelName,guildName,channelId,guildId)
        cursor.execute(sql, val)
        self.connection.commit()
        cursor.close()

    def getSubChannel(self):
        tab = []
        cursor = self.connection.cursor()
        query = ("SELECT * FROM esport_channels")
        cursor.execute(query)
        for a in cursor:
            tab.append(a)
        cursor.close()
        return tab

    def getWorldsFM(self):
        tab = []
        cursor = self.connection.cursor()
        query = ("SELECT * FROM worldsfm")
        cursor.execute(query)
        for a in cursor:
            tab.append(a)
        cursor.close()
        return tab

    def getAllPlayers(self):
        cursor = self.connection.cursor()
        query = ("SELECT * FROM pro_gracze")
        cursor.execute(query)
        columns = cursor.description 
        result = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
        cursor.close()
        return result

