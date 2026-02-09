from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

import requests
import pandas as pd
import sqlite3
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

default_args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="cotacao_dolar_diaria",
    start_date=datetime(2026, 2, 4),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
    tags=["api", "dolar"],
) as dag:

    def get_dollar_price(**context):
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url)
        response = response.json()
        logging.info(f"Response from API: {response}")
        valor = response["rates"]["BRL"]
        context["ti"].xcom_push(key="cotacao", value=valor)

    def save_to_csv(**context):
        valor = context["ti"].xcom_pull(key="cotacao", task_ids="buscar_cotacao")
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        df = pd.DataFrame([[data, valor]], columns=["data", "cotacao"])
        df.to_csv(
            "/opt/airflow/dags/cotacao_dolar.csv",
            mode="a",
            header=False,
            index=False,
        )

    def insert_into_db(**context):
        valor = context["ti"].xcom_pull(key="cotacao", task_ids="buscar_cotacao")
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect("/opt/airflow/dags/cotacoes.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cotacao_dolar (
                data TEXT,
                valor DECIMAL(10, 4)
            )
            """
        )

        cursor.execute(
            "INSERT INTO cotacao_dolar VALUES (?, ?)",
            (data, valor)
        )

        conn.commit()
        conn.close()

    def notify():
        print("Pipeline executado com sucesso!")

    taskOne = PythonOperator(
        task_id="buscar_cotacao",
        python_callable=get_dollar_price,
    )

    taskTwo = PythonOperator(
        task_id="salvar_csv",
        python_callable=save_to_csv,
    )

    taskThree = PythonOperator(
        task_id="inserir_banco",
        python_callable=insert_into_db,
    )

    taskFour = PythonOperator(
        task_id="notificar",
        python_callable=notify,
    )

    taskOne >> taskTwo >> taskThree >> taskFour
