import threading
import requests
import time
from custom_modules.constant.APIkey import *

class Puuid():
    def __init__(self):
        # 인스턴스 변수로 선언
        self.puuids = []
        self.puuid_lock = threading.Lock()

    def _request_puuid(self, summonerName):
        """request puuid API and collect summoner Names in specific tier"""
        try:
            puuid_url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + str(
                summonerName) + "?api_key=" + APIkey.PRODUCTION_KEY.str_key
            puuid = requests.get(puuid_url).json()["puuid"]
            with self.puuid_lock:
                self.puuids.append(puuid)
            return

        except Exception as e:
            return

    def collect_puuids(self, summonerNames):
        """collect specific tier's puuids using by multi-thread"""
        puuid_threads = []

        for i in range(len(summonerNames)):
            if i % 50 == 0 and i > 0:
                time.sleep(10)

            thread = threading.Thread(target=self._request_puuid, args=(summonerNames[i],))
            puuid_threads.append(thread)
            thread.start()

        # 모든 스레드가 종료될 때까지 대기
        for thread in puuid_threads:
            thread.join()

        print("수집한 puuid 개수: ", len(self.puuids))
        return self.puuids

# 테스트를 위해 summonerNames 리스트를 임의로 생성
# summonerNames = ["두루 주 빛날 희", "아니 나 킬 좀 줘", "G0d Thunder"]
# puuid_instance = Puuid()
# print(puuid_instance.collect_puuids(summonerNames))