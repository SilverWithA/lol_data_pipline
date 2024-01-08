import threading
import requests
import time

from dags.custom_modules.constant.APIkey import *


class Puuid():
    def __init__(self):
        self.puuids = []
    def _request_puuid(self, summonerName):
        """request puuid API and collect summoner Names in specific tier"""
        result_data_lock = threading.Lock()
        try:
            puuid_url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + str(
                summonerName) + "?api_key=" + APIkey.PRODUCION_KEY.str_key
            puuid = requests.get(puuid_url).json()["puuid"]

            with result_data_lock:
                self.puuids.append(puuid)
            return
        except Exception as e:
            return

    def collect_puuids(self, summonerNames):
        """collect specific tier's puuids unsing by multi-thread"""
        puuid_threads = []
        for i in range(len(summonerNames)):

            if i % 50 == 0 and i > 0:
                time.sleep(10)

            thread = threading.Thread(target=_request_puuid, args=(summonerNames[i],))
            puuid_threads.append(thread)
            thread.start()

        # 모든 스레드가 종료될 때까지 대기
        for thread in puuid_threads:
            thread.join()

        print("수집한 puuid 개수: ", len(self.puuids))
        return self.puuids