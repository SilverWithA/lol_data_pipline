from dags.custom_modules.constant.tiers import *
from dags.custom_modules.constant.APIkey import *
import requests

class SummonerName():
    def requeset_summonerNames(tier):
        """request summoner API and collect summoner Names in specific tier"""
        summonerNames = []
        if tier not in [Tier.CHALLENGER, Tier.GRANDMASTER, Tier.MASTER]:
            for division in ["I","II","III","IV"]:
                summoner_url = tier.summoner_url + division + "?page=1&api_key=" + str(APIkey.PRODUCTION_KEY.str_key)
                summoner_r = requests.get(summoner_url)

                summonerName_count = len(summoner_r.json())

                for i in range(summonerName_count):
                    summonerNames.append(summoner_r.json()[i]['summonerName'])

            return summonerNames
        else:
            summoner_url = tier.summoner_url + str(APIkey.PRODUCTION_KEY.str_key)
            summoner_r = requests.get(summoner_url)

            summonerName_count = len(summoner_r.json()["entries"])

            for i in range(summonerName_count):
                summonerNames.append(summoner_r.json()["entries"][i]["summonerName"])

            return summonerNames




# 사용 예시
# print(SummonerName.requeset_summonerNames(Tier.CHALLENGER)[:10])  # 챌린저
# print(SummonerName.requeset_summonerNames(Tier.GRANDMASTER)[:10])  # 그마
# print(SummonerName.requeset_summonerNames(Tier.MASTER)[:10])  # 마스터
# print(len(SummonerName.requeset_summonerNames(Tier.DIAMOND))) # 다이아 이하


# ------------- 한 페이지에 대략 200명
# u = "https://kr.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/DIAMOND/I?page=1&api_key=RGAPI-82d303c3-356f-4cbe-83b6-6ac2ca16567c"
# r = requests.get(u)
# for i in range(10):
#     print(r.json()[i]['summonerName'])

# print(len(SummonerName.requeset_summonerNames(Tier.DIAMOND)))