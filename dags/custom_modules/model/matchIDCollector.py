from custom_modules.constant.tiers import *
from custom_modules.constant.APIkey import *
import requests

class SummonerName():
    def requeset_summonerNames(tier):
        """request summoner API and collect summoner Names in specific tier"""
        summonerNames = []
        errors = []
        try:
            if tier in [Tier.CHALLENGER, Tier.GRANDMASTER, Tier.MASTER]:
                summoner_url = tier.summoner_url + str(APIkey.PRODUCTION_KEY.str_key)
                summoner_r = requests.get(summoner_url)

                summonerName_count = len(summoner_r.json()["entries"])

                for i in range(summonerName_count):
                    summonerNames.append(summoner_r.json()["entries"][i]["summonerName"])

                return summonerNames
            # under master ranking = diamond ~ bronze
            else:
                for division in Tier.DIVISIONS.summoner_url:
                    print(division)
                    summoner_url = tier.summoner_url + division + "?page=1&api_key=" + str(APIkey.PRODUCTION_KEY.str_key)
                    summoner_r = requests.get(summoner_url)

                    summonerName_count = len(summoner_r.json())

                    for i in range(summonerName_count):
                        summonerNames.append(summoner_r.json()[i]['summonerName'])

                ############################
                print(len(summonerNames))
                return summonerNames

        except Exception as e:
            errors.append(e)




# 사용 예시 및 테스트 코드
# print(SummonerName.requeset_summonerNames(Tier.CHALLENGER)[:10])  # 챌린저
# print(SummonerName.requeset_summonerNames(Tier.GRANDMASTER)[:10])  # 그마
# print(SummonerName.requeset_summonerNames(Tier.MASTER)[:10])  # 마스터
# print(len(SummonerName.requeset_summonerNames(Tier.DIAMOND))) # 다이아 이하
