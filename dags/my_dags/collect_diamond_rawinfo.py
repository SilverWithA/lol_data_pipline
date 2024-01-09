from airflow import DAG
from airflow.utils.db import provide_session
from airflow.models import XCom
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

from datetime import datetime
from custom_modules.model.matchIDCollector import SummonerName
from custom_modules.constant.tiers import Tier

def _summoner_task(ti):
    summonerNames = SummonerName.requeset_summonerNames(Tier.DIAMOND)
    ti.xcom_push(key="summnoerChallenger", value = summonerNames)

with DAG("collect_diamond_gameinfo", start_date=datetime(2024, 1, 1),
    schedule_interval='@daily', catchup=False) as dag:

    summoner_task = PythonOperator(
        task_id="summoner_task",
        python_callable=_summoner_task
    )

    summoner_task

