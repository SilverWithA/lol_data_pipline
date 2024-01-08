from dags.custom_modules.constant.tiers import *
from dags.custom_modules.constant.APIkey import *
import requests

class SummonerName():
    def requeset_summonerNames(tier):
        summonerNames = []

        """request summoner API and collect summoner Names in specific tier"""
        summoner_url = tier.summoner_url + str(APIkey.PRODUCION_KEY.str_key)
        summoner_r = requests.get(summoner_url)

        summonerName_count = len(summoner_r.json()["entries"])

        for i in range(summonerName_count):
            summonerNames.append(summoner_r.json()["entries"][i]["summonerName"])

        return summonerNames



# 사용 예시
# print(SummonerName.requeset_summonerNames(Tier.CHALLENGER)[:10])  # 챌린저
# print(SummonerName.requeset_summonerNames(Tier.GRANDMASTER)[:10])  # 그마
# print(SummonerName.requeset_summonerNames(Tier.MASTER)[:10])  # 마스터

# ------------- 한 페이지에 대략 200명
u = "https://kr.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/DIAMOND/I?page=1&api_key=RGAPI-82d303c3-356f-4cbe-83b6-6ac2ca16567c"
r = requests.get(u)
print(len(r.json()))