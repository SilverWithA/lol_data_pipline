from airflow import DAG
from airflow.utils.db import provide_session
from airflow.models import XCom
from airflow.operators.python import PythonOperator

from datetime import datetime
from custom_modules.constant.SummonerAPI import SummonerAPI
from custom_modules.model.summonerCollector import SummonerName
from custom_modules.model.puuidCollector import Puuid
from custom_modules.model.matchIDCollector import MatchID
from custom_modules.model.gameinfoCollector import Gameinfo

@provide_session
def cleanup_xcom(session=None, **context):
    session.query(XCom).delete()

def _summoner_task(ti):
    summonerNames = SummonerName.requeset_summonerNames(SummonerAPI.CHALLENGER)
    ti.xcom_push(key="summonersChallenger", value = summonerNames)


def _puuid_task(ti):
    puuid_instance = Puuid()
    summonerNames = ti.xcom_pull(key="summonersChallenger", task_ids='summoner_task')
    puuids = puuid_instance.collect_puuids(summonerNames)
    ti.xcom_push(key="puuidsChallenger", value=puuids)

def _matchID_task(ti):
    matchID_instance = MatchID()
    matchIDs = matchID_instance.collect_matchIDs(ti.xcom_pull(key="puuidsChallenger"))
    ti.xcom_push(key="matchIDsChallenger", value=matchIDs)


def _gameinfo_task(ti):
    gameinfo_instance = Gameinfo()
    gameinfo_instance.collect_gameinfo(key_name="CHALLENGER",
                                                  matchIDs = ti.xcom_pull(key="matchIDsChallenger"))



with DAG("CHALLENGER_gameinfo", start_date=datetime(2024, 1, 1),
    schedule_interval='@daily', catchup=False) as dag:


    clean_xcom = PythonOperator(
        task_id="clean_xcom",
        python_callable=cleanup_xcom,
        provide_context=True
    )

    summoner_task = PythonOperator(
        task_id="summoner_task",
        python_callable=_summoner_task
    )

    puuid_task = PythonOperator(
        task_id="puuid_task",
        python_callable=_puuid_task
    )

    matchID_task = PythonOperator(
        task_id="matchID_task",
        python_callable=_matchID_task
    )

    gameinfo_challenger = PythonOperator(
        task_id="gameinfo_challenger",
        python_callable=_gameinfo_task
    )





    clean_xcom >> summoner_task >> puuid_task >> matchID_task >> gameinfo_challenger
