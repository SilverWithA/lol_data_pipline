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
    summonerNames = SummonerName.requeset_summonerNames(SummonerAPI.PLATINUM)
    ti.xcom_push(key="summonersPLATINUM", value = summonerNames)

def _puuid_task(ti):
    puuid_instance = Puuid()
    summonerNames = ti.xcom_pull(key="summonersPLATINUM")
    puuids = puuid_instance.collect_puuids(summonerNames)
    ti.xcom_push(key="puuidsPLATINUM", value=puuids)

def _matchID_task(ti):
    matchID_instance = MatchID()
    matchIDs = matchID_instance.collect_matchIDs(ti.xcom_pull(key="puuidsPLATINUM"))
    ti.xcom_push(key="matchIDsPLATINUM", value=matchIDs)

def _gameinfo_task(ti):
    gameinfo_instance = Gameinfo()
    gameinfo_instance.collect_gameinfo(key_name="PLATINUM",
                                       matchIDs=ti.xcom_pull(key="matchIDsPLATINUM"))


with DAG("PLATINUM_gameinfo", start_date=datetime(2024, 1, 1),
    schedule_interval='@daily', catchup=False) as dag:

    clean_xcom = PythonOperator(
        task_id="clean_xcom",
        python_callable=cleanup_xcom,
        provide_context=True
    )

    collect_summonerNames = PythonOperator(
        task_id="collect_summonerNames",
        python_callable=_summoner_task
    )

    collect_puuid = PythonOperator(
        task_id="collect_puuid",
        python_callable=_puuid_task
    )

    collect_matchID = PythonOperator(
        task_id="collect_matchID",
        python_callable=_matchID_task
    )

    collect_gameinfo = PythonOperator(
        task_id="collect_gameinfo",
        python_callable=_gameinfo_task
    )

    clean_xcom >> collect_summonerNames >> collect_puuid >> collect_matchID >> collect_gameinfo