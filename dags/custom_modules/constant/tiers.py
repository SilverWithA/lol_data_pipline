from enum import Enum


class ComplexEnumValue:
    def __init__(self, *value):
        self.value = value

    # 호출 예시: Tier.CHALLENGER.value.get_summoner_url()
    def get_summoner_url(self):
        return self.value[0]

    def get_puuid_url(self):
        return self.value[1]

class Tier(Enum):
    CHALLENGER = ComplexEnumValue("asdf","qwer")
    # GRANDMASTER= (),
    # MASTER = (),
    # DIAMOND = (),
    # EMERALD = (),
    # PLATINUM = (),
    # GOLD = (),
    # SILVER = (),
    # BRONZE = ()




