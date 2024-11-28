import os
import requests
from dotenv import load_dotenv
import time

#Carregar os dados do arquivo .env
load_dotenv() 
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
REGION_URL = os.getenv("AMERICAS_URL")
HEADERS = {"X-Riot-Token": API_KEY}
AMOUNT_PLAYERS = 100
AMOUNT_MATCHES = 40

def getTopPlayers():
    url = f"{BASE_URL}/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        players = data["entries"]
        top_players = sorted(players, key=lambda x: x["leaguePoints"], reverse=True)[:AMOUNT_PLAYERS]
        return [player["summonerId"] for player in top_players]
    else:
        print(f"Erro ao buscar jogadores: {response.status_code}")
        return []

def getPUUID(summonerId):
    url = f"{BASE_URL}/lol/summoner/v4/summoners/{summonerId}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        return data["puuid"]
    else:
        print(f"Erro ao buscar PUUID: {response.status_code}")
        return None

def getNick(puuid):
    url = f"{REGION_URL}/riot/account/v1/accounts/by-puuid/{puuid}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        return data["gameName"]
    else:
        print(f"Erro ao buscar Nicks: {response.status_code}")
        return None

def getMatchIds(puuid):
    url = f"{REGION_URL}/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={AMOUNT_MATCHES}&type=ranked"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Erro ao buscar partidas: {response.status_code}")
        return None

def getMatchData(matchId):
    url = f"{REGION_URL}/lol/match/v5/matches/{matchId}"
    time.sleep(0.1)
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Erro ao buscar dados da partida: {response.status_code}")
        return None

#Salvar em arquivo .csv
#gameid, totalGold, destroyedTowers, destroyedNexusTowers, destroyedInhibitors, dragons, barons, winTeam
def saveData(data, filename):
    with open(filename, "w") as file:
        file.write("gameid,totalGoldA,totalGoldB,destroyedTowersA,destroyedTowersB,destroyedNexusTowersA,destroyedNexusTowersB,destroyedInhibitorsA,destroyedInhibitorsB,dragonsA,dragonsB,baronsA,baronsB,winTeam\n")
        for match in data:
          gameid = match["info"]["gameId"]
          # Inicializar variáveis
          #100 -> A, 200 -> B
          totalGold = {100: 0, 200: 0}
          destroyedTowers = {100: 0, 200: 0}
          destroyedNexusTowers = {100: 0, 200: 0}
          destroyedInhibitors = {100: 0, 200: 0}
          dragons = {100: 0, 200: 0}
          barons = {100: 0, 200: 0}
          winTeam = None
          
          # Calcular o total de gold por time
          for participant in match["info"]["participants"]:
              team_id = participant["teamId"]
              totalGold[team_id] += participant["goldEarned"]
              destroyedNexusTowers[team_id] = participant["challenges"]["hadOpenNexus"]
          
          # Obter informações de objetivos destruídos
          for team in match["info"]["teams"]:
              team_id = team["teamId"]
              destroyedTowers[team_id] = team["objectives"]["tower"]["kills"]
              destroyedInhibitors[team_id] = team["objectives"]["inhibitor"]["kills"]
              dragons[team_id] = team["objectives"]["dragon"]["kills"]
              barons[team_id] = team["objectives"]["baron"]["kills"]
              if team["win"]:
                  winTeam = team_id
          file.write(
            f"{gameid},{totalGold[100]},{totalGold[200]},{destroyedTowers[100]},{destroyedTowers[200]},"
            f"{destroyedNexusTowers[100]},{destroyedNexusTowers[200]},{destroyedInhibitors[100]},{destroyedInhibitors[200]},"
            f"{dragons[100]},{dragons[200]},{barons[100]},{barons[100]},{0 if winTeam == 200 else 1}\n")

def main():
  # Buscar os summonerIds dos top players do servidor
  print("Buscando os top players...")
  topPlayersSummIds = getTopPlayers()

  # Buscar os puuids dos top players
  print("Buscando os puuids dos top players...")
  puuids = [getPUUID(player) for player in topPlayersSummIds]

  # Aguadar 1 segundo para não estourar o limite de requests
  time.sleep(1)

  #Buscando as partidas dos top players
  print("Buscando as partidas dos top players...")
  matchIdsNested = [getMatchIds(puuid) for puuid in puuids]
  matchIds = [matchId for sublist in matchIdsNested for matchId in sublist]
  # Aguardar 1 segundo para não estourar o limite de requests
  time.sleep(1)

  # Buscar os dados das partidas matchsids= [[matchId1, matchId2, ...], [matchId1, matchId2, ...], ...]
  print("Buscando os dados das partidas...")
  matchData = [getMatchData(match) for match in matchIds]

  # Salvar os dados em um arquivo .csv
  print("Salvando os dados em um arquivo .csv...")
  saveData(matchData, "matches.csv")


if __name__ == "__main__":
    main()