import threading
import requests
import time
from datetime import datetime, timedelta

from custom_modules.constant.APIkey import *

class Gameinfo():
    def __init__(self):
        self.raw_gameinfo = []
        self.gameinfo_lock = threading.Lock()

    def _request_gameinfo(self, matchID):
        """request API method. This method use in thread"""
        current_time = datetime.utcnow()
        two_weeks_ago = current_time - timedelta(weeks=2)

        try:
            match_url = "https://asia.api.riotgames.com/lol/match/v5/matches/" + matchID + "?api_key=" + APIkey.PRODUCTION_KEY.str_key
            mat_info = requests.get(match_url).json()

            # 최근 2주 전 경기인지 확인
            gameStartTimestamp = int(mat_info['info']['gameStartTimestamp']) / 1000.0
            if two_weeks_ago.timestamp() > gameStartTimestamp:
                return

            # 최근 2주 전 경기일시 추가 정보(timeline 정보까지 수집)
            timeline_url = "https://asia.api.riotgames.com/lol/match/v5/matches/" + matchID + "/timeline?api_key=" + APIkey.PRODUCTION_KEY.str_key
            mat_timeline = requests.get(timeline_url).json()

            # 데이터 병합하여 append
            with self.gameinfo_lock:
                total_json = {"mat_info": mat_info,
                              "mat_timeline": mat_timeline}
                self.raw_gameinfo.append(total_json)
        except:
            return


    def collect_gameinfo(self, matchIDs):
        """collect specific tier's gameinfo unsing by multi thread"""
        gameinfo_threads = []
        ### 100개만 테스트
        for i in range(len(matchIDs)):
            if i % 50 == 0 and i > 0:
                time.sleep(10)

            thread = threading.Thread(target=self._request_gameinfo, args=(matchIDs[i],))
            gameinfo_threads.append(thread)
            thread.start()

        for thread in gameinfo_threads:
            thread.join()

        print("수집한 raw_gameinfo 개수: ", len(self.raw_gameinfo))
        return self.raw_gameinfo

# mat_list = ['KR_6891642892', 'KR_6891604836', 'KR_6890811189', 'KR_6890721360', 'KR_6890649872', 'KR_6878612389', 'KR_6878576404', 'KR_6877013410', 'KR_6876976720', 'KR_6876934231', 'KR_6876888413', 'KR_6871937117', 'KR_6871899054', 'KR_6871854189', 'KR_6871808994', 'KR_6871792616', 'KR_6866684106', 'KR_6866355101', 'KR_6866307327', 'KR_6864740000', 'KR_6864709673', 'KR_6864470038', 'KR_6859892549', 'KR_6859869622', 'KR_6859836450', 'KR_6892924782', 'KR_6890485731', 'KR_6890447545', 'KR_6890416576', 'KR_6890385384', 'KR_6890355688', 'KR_6890329183', 'KR_6890279646', 'KR_6890235331', 'KR_6890202100', 'KR_6890157240', 'KR_6890122220', 'KR_6890084441', 'KR_6890051094', 'KR_6889362066', 'KR_6887687377', 'KR_6886281160', 'KR_6859104994', 'KR_6858880422', 'KR_6858798921', 'KR_6892757640', 'KR_6892633370', 'KR_6892584122', 'KR_6892517700', 'KR_6892073566', 'KR_6892038432', 'KR_6891978053', 'KR_6891909596', 'KR_6891288388', 'KR_6890931888', 'KR_6890894177', 'KR_6888242698', 'KR_6888063957', 'KR_6887574090', 'KR_6885912046', 'KR_6885874828', 'KR_6885827854', 'KR_6885797434', 'KR_6884644493', 'KR_6884630221', 'KR_6891793139', 'KR_6891763438', 'KR_6891743420', 'KR_6891707282', 'KR_6891674954', 'KR_6891661408', 'KR_6891635624', 'KR_6891623098', 'KR_6891601111', 'KR_6888213189', 'KR_6888176554', 'KR_6888150003', 'KR_6888116368', 'KR_6888084198', 'KR_6888049918', 'KR_6888015712', 'KR_6887999559', 'KR_6887584233', 'KR_6887545870', 'KR_6887497551', 'KR_6871897679', 'KR_6871846165', 'KR_6871788152', 'KR_6871728793', 'KR_6857237278']
# gameinfo_instance = Gameinfo()
# gameinfo_instance.collect_gameinfo(mat_list)