from abc import *

# 추상 클래스(1)
class SummonerName(metaclass=ABCMeta):

    def __init__(self):
        self.summonerNames = []
    @abstractmethod  # 추상 클래스의 메소드 선언
    def requeset_summonerNames(self):
        """request API method."""
        pass

class Puuid(metaclass=ABCMeta):

    def __init__(self):
        self.puuids = []
    @abstractmethod
    def fetch_puuid(self, summonerName):
        """request API method. This method use in thread"""
        pass

    @abstractmethod
    def collect_puuids(self, summonerNames):
        """collect specific tier's puuids unsing by multi thread"""
        pass

class MatchID(metaclass=ABCMeta):
    def __init__(self):
        self.matchIDs = []
    @abstractmethod
    def fetch_matchId(self, puuid):
        """request API method. This method use in thread"""
        pass

    @abstractmethod
    def collect_matchIDs(self, puuids):
        """collect specific tier's matchIDs unsing by multi thread"""
        pass

class Gameinfo(metaclass=ABCMeta):
    def __init__(self):
        self.raw_gameinfo = []
    @abstractmethod
    def fetch_gameinfo(self, matchID):
        """request API method. This method use in thread"""
        pass

    @abstractmethod
    def collect_gameinfo(self, matchIDs):
        """collect specific tier's gameinfo unsing by multi thread"""
        pass