#plik ze stringami i pare ustawien

# division_img = {}
# positions_img = {}


division_dict = 'resources/Ranked_Emblems/'
positions_dict = 'resources/Ranked_Positions/'

divs = ['Iron','Bronze','Silver','Gold','Platinum','Diamond','Master','Grandmaster','Challenger']
poss = ['Bot','Jungle','Mid','Support','Top']

def getDivisionEmblem(division: str):
    try:
        divs.index(division)
    except:
        return None
    if division == 'Platinum':
        division = 'Plat'
    return division_dict + "Emblem_" + division + ".png" 

def getPositionEmblem(division: str, position: str):
    try:
        divs.index(division)
        poss.index(position)
    except:
        return None
    if division == 'Platinum':
        division = 'Plat'
    return positions_dict + "Position_" + division + "-" + position + ".png" 

# print(getDivisionEmblem('Platinum'))
# print(getPositionEmblem('Platinum','Bot'))