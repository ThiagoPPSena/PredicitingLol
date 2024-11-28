import requests
import json
import os
from dotenv import load_dotenv
import time
import urllib3

# Desativar avisos de segurança do urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Carregar a chave da API do arquivo .env
load_dotenv()
API_KEY = os.getenv('RIOT_API_KEY')
BASE_URL = "https://127.0.0.1:2999/liveclientdata/allgamedata"

# Função para pegar os dados da partida em tempo real
def getLiveGameData():
  try:
    response = requests.get(BASE_URL, verify=False)
    if response.status_code == 200:
      return response.json()  # Retorna os dados no formato JSON
    else:
      print(f"Erro ao acessar a API: {response.status_code}")
      return None
  except Exception as e:
    print(f"Erro na requisição: {e}")
    return None



def main():
  # Testar a função
  numberRepeat = 20
  for _ in range(numberRepeat):
    gameData = getLiveGameData()
    print(json.dumps(gameData, indent=2))
    time.sleep(5)

if __name__ == "__main__":
    main()