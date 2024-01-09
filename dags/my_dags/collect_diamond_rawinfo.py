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
from custom_modules.model.gameinfoCollector import Gameinfo
from custom_modules.model.gameinfo_IO import FileIoSupporter


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

def _gameinfo_task(ti):
    diamond_gameinfo = Gameinfo()
    gameinfo = diamond_gameinfo.collect_gameinfo(ti.xcom_pull(key="matchIDsDiamond"))
    # mat_list = ['KR_6891642892', 'KR_6891604836', 'KR_6890811189', 'KR_6890721360', 'KR_6890649872', 'KR_6878612389', 'KR_6878576404', 'KR_6877013410', 'KR_6876976720', 'KR_6876934231', 'KR_6876888413', 'KR_6871937117', 'KR_6871899054', 'KR_6871854189', 'KR_6871808994', 'KR_6871792616', 'KR_6866684106', 'KR_6866355101', 'KR_6866307327', 'KR_6864740000', 'KR_6864709673', 'KR_6864470038', 'KR_6859892549', 'KR_6859869622', 'KR_6859836450', 'KR_6892924782', 'KR_6890485731', 'KR_6890447545', 'KR_6890416576', 'KR_6890385384', 'KR_6890355688', 'KR_6890329183', 'KR_6890279646', 'KR_6890235331', 'KR_6890202100', 'KR_6890157240', 'KR_6890122220', 'KR_6890084441', 'KR_6890051094', 'KR_6889362066', 'KR_6887687377', 'KR_6886281160', 'KR_6859104994', 'KR_6858880422', 'KR_6858798921', 'KR_6892757640', 'KR_6892633370', 'KR_6892584122', 'KR_6892517700', 'KR_6892073566', 'KR_6892038432', 'KR_6891978053', 'KR_6891909596', 'KR_6891288388', 'KR_6890931888', 'KR_6890894177', 'KR_6888242698', 'KR_6888063957', 'KR_6887574090', 'KR_6885912046', 'KR_6885874828', 'KR_6885827854', 'KR_6885797434', 'KR_6884644493', 'KR_6884630221', 'KR_6891793139', 'KR_6891763438', 'KR_6891743420', 'KR_6891707282', 'KR_6891674954', 'KR_6891661408', 'KR_6891635624', 'KR_6891623098', 'KR_6891601111', 'KR_6888213189', 'KR_6888176554', 'KR_6888150003', 'KR_6888116368', 'KR_6888084198', 'KR_6888049918', 'KR_6888015712', 'KR_6887999559', 'KR_6887584233', 'KR_6887545870', 'KR_6887497551', 'KR_6871897679', 'KR_6871846165', 'KR_6871788152', 'KR_6871728793', 'KR_6857237278']
    # gameinfo = diamond_gameinfo.collect_gameinfo(mat_list)

    hook = S3Hook('aws_default')
    json_file_obj = FileIoSupporter.make_json_file_object(gameinfo)
    hook.load_file_obj(file_obj=json_file_obj, key='diamond', bucket_name='lol-raw-gameinfo', replace=False,
                       encrypt=False)


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

    gameinfo_task = PythonOperator(
        task_id="gameinfo_task",
        python_callable=_gameinfo_task
    )

    clean_xcom >> summoner_task >> puuid_task >> matchID_task >> gameinfo_task

