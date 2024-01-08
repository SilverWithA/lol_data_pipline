from airflow import DAG
from airflow.utils.db import provide_session
from airflow.models import XCom
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

from datetime import datetime
from custom_modules.collect_summners import collect_challenger_summoner
from custom_modules.collecting_modules import *


def _summoner_task(ti):
    summonerNames = collect_challenger_summoner()
    ti.xcom_push(key="summnoerChallenger", value = summonerNames)

def _puuid_task(ti):
    puuids = collect_puuids(ti.xcom_pull(key="summnoerChallenger", task_ids ='summoner_task'))
    ti.xcom_push(key="puuidsChallenger", value=puuids)

def _matchID_task(ti):
    matchIDs = collect_matchIDs(ti.xcom_pull(key="puuidsChallenger"))
    ti.xcom_push(key="matchIDsChallenger", value=matchIDs)

def _gameinfo_task(ti):
    gameinfo = collect_gameinfo(ti.xcom_pull(key="matchIDsChallenger"))
    ti.xcom_push(key="gameinfoChallenger", value=gameinfo)



@provide_session
def cleanup_xcom(session=None, **context):
    dag = context["dag"]
    dag_id = dag._dag_id
    session.query(XCom).filter(XCom.dag_id == dag_id).delete()

def _upload_to_S3(ti):
    hook = S3Hook('aws_default')
    # 업로드할 파일 객체 생성
    json_file_obj = make_file_obj(ti.xcom_pull(key="gameinfoChallenger"))
    hook.load_file_obj(file_obj=json_file_obj, key='challenger_0108', bucket_name='lol-raw-gameinfo.ap-northeast-2', replace=False, encrypt=False)


with DAG("collect_challenger_Gameinfo", start_date=datetime(2024, 1, 1),
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

    gameinfo_task = PythonOperator(
        task_id="gameinfo_task",
        python_callable=_gameinfo_task
    )

    upload_task = PythonOperator(
        task_id='upload_task',
        python_callable=_upload_to_S3
    )



    clean_xcom >> summoner_task >> puuid_task >> matchID_task >> gameinfo_task >> upload_task

