from liveClientApi import getLiveGameData
import requests
import os
import pandas as pd
import dotenv

dotenv.load_dotenv()
APIKEY = os.getenv('APIKEY')
REGION = 'br1'

versionLatest = requests.get(f"https://ddragon.leagueoflegends.com/api/versions.json").json()[0]
allItems = requests.get(f"http://ddragon.leagueoflegends.com/cdn/{versionLatest}/data/pt_BR/item.json").json()['data']

# totalGoldA,totalGoldB,destroyedTowersA,destroyedTowersB,destroyedNexusTowersA,destroyedNexusTowersB,
# destroyedInhibitorsA,destroyedInhibitorsB,dragonsA,dragonsB,baronsA,baronsB

def getGoldTeam(realTimeData):
  allPlayers = realTimeData['allPlayers']
  AllEvents = realTimeData['events']['Events']
  goldTeams = {100: 0, 200: 0}
  for player in allPlayers:
    items = player['items']
    for item in items:
      itemId = item['itemID']
      if player['team'] == 'ORDER':
        goldTeams[100] += allItems[str(itemId)]['gold']['total']
      else:
        goldTeams[200] += allItems[str(itemId)]['gold']['total']
  return (goldTeams[100],goldTeams[200])

def getTowersDestroyed(realTimeData):
  allPlayers = realTimeData['allPlayers']
  AllEvents = realTimeData['events']['Events']
  towersDestroyed = {100: 0, 200: 0}
  for event in AllEvents:
    if event['EventName'] == 'TurretKilled':
      #Turret_<EQUIPE>_<FAIXA>_<NUMERO>_<SUFIXO>
      if event['TurretKilled'][7:9] == 'T2':
        towersDestroyed[100] += 1
      else:
        towersDestroyed[200] += 1
  return (towersDestroyed[100],towersDestroyed[200])

def getInhibitorsDestroyed(realTimeData):
  allPlayers = realTimeData['allPlayers']
  AllEvents = realTimeData['events']['Events']
  inhibitorsDestroyed = {100: 0, 200: 0}
  for event in AllEvents:
    if event['EventName'] == 'InhibKilled':
      #Barracks_T2_R1
      team = event['InhibKilled'][9:11] # T1 / T2
      if team == 'T2':
        inhibitorsDestroyed[100] += 1
      else:
        inhibitorsDestroyed[200] += 1
  return (inhibitorsDestroyed[100],inhibitorsDestroyed[200])

def getDragonsKilled(realTimeData):
  allPlayers = realTimeData['allPlayers']
  AllEvents = realTimeData['events']['Events']
  dragonsKilled = {100: 0, 200: 0}
  for event in AllEvents:
    if event['EventName'] == 'DragonKill':
      playerName = event['KillerName']
      for player in allPlayers:
        if player['riotIdGameName'] == playerName or player['summonerName'] == playerName:
          if player['team'] == 'ORDER':
            dragonsKilled[100] += 1
          else:
            dragonsKilled[200] += 1
  return (dragonsKilled[100],dragonsKilled[200])

def getBaronsKilled(realTimeData):
  allPlayers = realTimeData['allPlayers']
  AllEvents = realTimeData['events']['Events']
  baronsKilled = {100: 0, 200: 0}
  for event in AllEvents:
    if event['EventName'] == 'BaronKill':
      playerName = event['KillerName']
      for player in allPlayers:
        if player['riotIdGameName'] == playerName or player['summonerName'] == playerName:
          if player['team'] == 'ORDER':
            baronsKilled[100] += 1
          else:
            baronsKilled[200] += 1
  return (baronsKilled[100],baronsKilled[200])

def getAllData():
  realTimeData = getLiveGameData()
  
  totalGold = getGoldTeam(realTimeData)
  towersDestroyed = getTowersDestroyed(realTimeData)
  inhibitorsDestroyed = getInhibitorsDestroyed(realTimeData)
  dragonsKilled = getDragonsKilled(realTimeData)
  baronsKilled = getBaronsKilled(realTimeData)

  data = {
    "totalGoldA": totalGold[0],
    "totalGoldB": totalGold[1],
    "destroyedTowersA": towersDestroyed[0],
    "destroyedTowersB": towersDestroyed[1],
    "destroyedInhibitorsA": inhibitorsDestroyed[0],
    "destroyedInhibitorsB": inhibitorsDestroyed[1],
    "dragonsA": dragonsKilled[0],
    "dragonsB": dragonsKilled[1],
    "baronsA": baronsKilled[0],
    "baronsB": baronsKilled[1]
  }
  df = pd.DataFrame(data, index=[0])
  return df

    

print(getAllData())