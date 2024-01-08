import threading
import requests
import time
import json

from datetime import datetime, timedelta

api_key = "RGAPI-82d303c3-356f-4cbe-83b6-6ac2ca16567c"
result_data_lock = threading.Lock()
start_time = time.time()




# 2. 티어별 puuid 조회
temp_puuids = []
def fetch_puuid(summonerName):
    try:
        puuid_url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + str(summonerName) + "?api_key=" + api_key
        puuid = requests.get(puuid_url).json()["puuid"]

        with result_data_lock:
            temp_puuids.append(puuid)
        return
    except Exception as e:
        return

def collect_puuids(summonerNames):
    puuid_threads = []
    for i in range(len(summonerNames)):

        if i % 50 == 0 and i > 0:
            time.sleep(10)

        thread = threading.Thread(target=fetch_puuid, args=(summonerNames[i],))
        puuid_threads.append(thread)
        thread.start()

    # 모든 스레드가 종료될 때까지 대기
    for thread in puuid_threads:
        thread.join()
    puuid_list = temp_puuids
    print("수집한 puuid 개수: ", len(puuid_list))
    return puuid_list



# 3. 유저 별 최근 20개 경기코드 조회 - challenger -----------------------

temp_matchIDs = []
def fetch_matchId(puuid):
    match_url = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/" + str(puuid) + "/ids?start=0&count=20&api_key=" + api_key
    each_usr_matchIDs = requests.get(match_url).json()

    with result_data_lock:
        for matchID in each_usr_matchIDs:
            temp_matchIDs.append(matchID)
        return
def collect_matchIDs(puuids):
    matchID_threads = []
    for i in range(len(puuids)):
        if i % 50 == 0 and i > 0:
            # print("i = ",i)
            # print("수집한 matchIDs의 개수: ", len(matchIDs))
            # print("스레드 개수: ", len(matchID_threads))
            time.sleep(10)
        thread = threading.Thread(target=fetch_matchId, args=(puuids[i],))
        matchID_threads.append(thread)
        thread.start()

    for thread in matchID_threads:
        thread.join()
    matchID_list = temp_matchIDs
    print("수집한 matchID 개수: ", len(matchID_list))
    return matchID_list

current_time = datetime.utcnow()
two_weeks_ago = current_time - timedelta(weeks=2)
temp_gameinfo = []

def fetch_matchID(matchID):
    """collect lately gameinfo"""
    try:
        match_url = "https://asia.api.riotgames.com/lol/match/v5/matches/" + matchID + "?api_key=" + api_key
        mat_info = requests.get(match_url).json()
        gameStartTimestamp = int(mat_info['info']['gameStartTimestamp']) / 1000.0

        if two_weeks_ago.timestamp() > gameStartTimestamp:
            return


        # time라인 api까지 조회
        timeline_url = "https://asia.api.riotgames.com/lol/match/v5/matches/" + matchID + "/timeline?api_key=" + api_key
        mat_timeline = requests.get(timeline_url).json()

        # 데이터 병합하여 append
        with result_data_lock:
            total_json = {"mat_info": mat_info,
                        "mat_timeline": mat_timeline}
            temp_gameinfo.append(total_json)


    except:
        return
def collect_gameinfo(matchIDs):
    gameinfo_threads = []
    # 100개만 테스트
    for i in range(100):
        if i % 50 == 0 and i > 0:
            # print("i: ", i)
            # print("수집한 정보 개수: ",len(raw_gameinfo))
            time.sleep(10)

        thread = threading.Thread(target=fetch_matchID, args=(matchIDs[i],))
        gameinfo_threads.append(thread)
        thread.start()

    for thread in gameinfo_threads:
        thread.join()
    raw_gameinfo = temp_gameinfo
    print("수집한 raw_gameinfo 개수: ", len(raw_gameinfo))
    return raw_gameinfo

def make_jsonfile(raw_gameinfo):
    return json.dumps(raw_gameinfo, indent=4)


