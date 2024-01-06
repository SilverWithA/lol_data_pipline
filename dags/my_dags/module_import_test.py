from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator

from datetime import datetime
from custom_modules.module_test1 import funct1, funct2

def _push_val(ti):
    data = funct1()
    ti.xcom_push(key='test', value= data)

def _pull_val(ti):
    data = ti.xcom_pull(key="test", task_ids ='push_val')
    data2 = funct2(data)
    ti.xcom_push(key='another_key', value=data2)

with DAG("module_import_test", start_date=datetime(2022, 1, 1),
    schedule_interval='@daily', catchup=False) as dag:

    push_val = PythonOperator(
        task_id = "push_val",
        python_callable = _push_val
    )

    pull_val = PythonOperator(
        task_id="pull_val",
        python_callable=_pull_val
    )

    push_val >> pull_val

