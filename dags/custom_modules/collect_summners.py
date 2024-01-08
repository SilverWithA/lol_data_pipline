import requests


api_key = ""



def collect_challenger_summoner():
    summonerNames = []
    # # 1. 티어별 닉네임 조회 - challenger  -----------------------
    summoner_url = "https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key=" + api_key
    summoner_r = requests.get(summoner_url)
    callen_count = len(summoner_r.json()["entries"])

    for i in range(callen_count):
        summonerNames.append(summoner_r.json()["entries"][i]["summonerName"])
    return summonerNames