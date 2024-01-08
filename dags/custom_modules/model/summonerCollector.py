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
print(SummonerName.requeset_summonerNames(Tier.CHALLENGER)[:10])
# print(SummonerName.requeset_summonerNames(Tier.GRANDMASTER)[:10])

