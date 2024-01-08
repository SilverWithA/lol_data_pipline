from enum import Enum

class Tier(Enum):
    CHALLENGER = ("asdf","qwer")
    # GRANDMASTER= (),
    # MASTER = (),
    # DIAMOND = (),
    # EMERALD = (),
    # PLATINUM = (),
    # GOLD = (),
    # SILVER = (),
    # BRONZE = ()

    @property
    def summoner_url(self):
        return self.value[0]

    @property
    def puuid_url(self):
        return self.value[0]






