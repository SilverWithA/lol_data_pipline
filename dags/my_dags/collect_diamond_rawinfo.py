from airflow import DAG
from airflow.utils.db import provide_session
from airflow.models import XCom
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

from datetime import datetime
from custom_modules.constant.tiers import Tier
from custom_modules.model.summonerCollector import SummonerName
from custom_modules.model.puuidCollector import Puuid
from custom_modules.model.matchIDCollector import MatchID
@provide_session
def cleanup_xcom(session=None, **context):
    session.query(XCom).delete()

def _summoner_task(ti):
    summonerNames = SummonerName.requeset_summonerNames(Tier.DIAMOND)
    ti.xcom_push(key="summnoerDiamond", value = summonerNames)

def _puuid_task(ti):
    puuid_instance = Puuid()
    summonerNames = ti.xcom_pull(key="summnoerDiamond", task_ids ='summoner_task')
    puuids = puuid_instance.collect_puuids(summonerNames)
    ti.xcom_push(key="puuidsDiamond", value=puuids)

def _matchID_task(ti):
    matchID_instance = MatchID()
    matchIDs = matchID_instance.collect_matchIDs(ti.xcom_pull(key="puuidsDiamond"))
    ti.xcom_push(key="matchIDsDiamond", value=matchIDs)

# def _gameinfo_task(ti):
#     gameinfo = collect_gameinfo(ti.xcom_pull(key="matchIDsDiamond"))
#     ti.xcom_push(key="gameinfoDiamond", value=gameinfo)
#
# def _upload_to_S3(ti):
#     hook = S3Hook('aws_default')
#     # 업로드할 파일 객체 생성
#     json_file_obj = make_file_obj(ti.xcom_pull(key="gameinfoDiamond"))
#     hook.load_file_obj(file_obj=json_file_obj, key='diamond', bucket_name='lol-raw-gameinfo', replace=False, encrypt=False)


with DAG("collect_diamond_gameinfo", start_date=datetime(2024, 1, 1),
    schedule_interval='@daily', catchup=False) as dag:

    clean_xcom = PythonOperator(
        task_id="clean_xcom",
        python_callable=cleanup_xcom,
        provide_context=True,
        # dag=dag
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

    # gameinfo_task = PythonOperator(
    #     task_id="gameinfo_task",
    #     python_callable=_gameinfo_task
    # )
    #
    # upload_task = PythonOperator(
    #     task_id='upload_task',
    #     python_callable=_upload_to_S3
    # )

    clean_xcom >> summoner_task >> puuid_task >> matchID_task

