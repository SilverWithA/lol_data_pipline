from enum import Enum

class Tier(Enum):
    CHALLENGER = ("https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key=")
    GRANDMASTER = ("https://kr.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5?api_key=")
    MASTER = ("https://kr.api.riotgames.com/lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5?api_key=")



    @property
    def summoner_url(self):
        return self.value






