import threading
import requests
import time
from custom_modules.constant.APIkey import *

class MatchID():
    def __init__(self):
        # 인스턴스 변수로 선언
        self.matchIDs = []
        self.matchID_lock = threading.Lock()

    def _request_matchID(self, puuid):
        """request API to collecting matchID(game code) corresponse user's puuid"""
        try:
            matchID_url = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/" + str(puuid) + "/ids?start=0&count=20&api_key=" + APIkey.PRODUCTION_KEY.str_key
            each_usr_matchIDs = requests.get(matchID_url).json()

            with self.matchID_lock:
                for matchID in each_usr_matchIDs:
                    self.matchIDs.append(matchID)
            return
        except Exception as e:
            return

    def collect_matchIDs(self, puuids):
        """collect specific tier's puuids using by multi-thread"""
        puuid_threads = []
        for i in range(len(puuids)):
            if i % 50 == 0 and i > 0:
                time.sleep(10)

            thread = threading.Thread(target=self._request_matchID, args=(puuids[i],))
            puuid_threads.append(thread)
            thread.start()

        for thread in puuid_threads:
            thread.join()

        # 중복 경기 코드 제거
        self.matchIDs = list(set(self.matchIDs))
        print("수집한 matchID 개수: ", len(self.matchIDs))
        return self.matchIDs

# 테스트를 위해 puuid 리스트를 임의로 생성
# p = ['oM0iKcQ3-4Zl18QMkWh7mcJbhR6MKs8Vx4xDZC4tZ-R0QsZjNXxtUUInmz1rY12MZScOrKKb79zJrg', 'iWnomvEF_MmA75CnmNZQERNMzJtxvQplqsGdcoAvaFVNCasVAtxd82eeIG7EuxsZ2ftVQ9LGP85GsQ', 'Sz8X8aI5rxudPXlK4o22B4H1WT1HNOBtrCZagRWs85XKqU4Bs4UTuvWeEKDpNYdq5uIWv2fuECzBHA']
# machid_instace = MatchID()
# print(machid_instace.collect_matchIDs(p))