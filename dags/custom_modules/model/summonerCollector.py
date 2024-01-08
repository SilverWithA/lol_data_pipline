from dags.custom_modules.constant.tiers import *

class SummonerName():
    def __init__(self):
        self.summonerNames = []

    def requeset_summonerNames(self, tier):
        """request summoner API and collect summoner Names in specific tier"""


print(Tier.CHALLENGER.first)